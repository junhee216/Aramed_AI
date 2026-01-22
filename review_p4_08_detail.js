// review_p4_08_detail.js
// P4 08번 상세 검토

import 'dotenv/config';
import { Client } from '@notionhq/client';
import fs from 'fs';
import path from 'path';
import os from 'os';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

class RateLimiter {
	constructor(maxRequestsPerSecond = 3) {
		this.maxRequests = maxRequestsPerSecond;
		this.requests = [];
	}

	async waitIfNeeded() {
		const now = Date.now();
		this.requests = this.requests.filter((time) => now - time < 1000);
		if (this.requests.length >= this.maxRequests) {
			const oldestRequest = Math.min(...this.requests);
			const waitTime = 1000 - (now - oldestRequest) + 10;
			if (waitTime > 0) {
				await new Promise((resolve) => setTimeout(resolve, waitTime));
			}
		}
		this.requests.push(Date.now());
	}
}

const rateLimiter = new RateLimiter(3);

function getPropertyValue(prop) {
	if (!prop) return '';
	
	switch (prop.type) {
		case 'title':
			return prop.title.map(t => t.plain_text).join('');
		case 'rich_text':
			return prop.rich_text.map(t => t.plain_text).join('');
		case 'number':
			return prop.number !== null ? String(prop.number) : '';
		case 'select':
			return prop.select?.name || '';
		case 'multi_select':
			return prop.multi_select.map(s => s.name).join(', ');
		default:
			return '';
	}
}

function checkJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return { valid: false, error: '빈 필드 또는 빈 객체' };
	}
	try {
		const parsed = JSON.parse(text);
		if (typeof parsed !== 'object' || Array.isArray(parsed)) {
			return { valid: false, error: 'JSON이 객체가 아닙니다' };
		}
		return { valid: true, error: null, parsed };
	} catch (e) {
		return { valid: false, error: e.message };
	}
}

function checkLaTeX(text) {
	if (!text || text.trim() === '') return { valid: true, error: null, issues: [] };
	
	const issues = [];
	const dollarCount = (text.match(/\$/g) || []).length;
	
	if (dollarCount > 0 && dollarCount % 2 !== 0) {
		issues.push(`$ 기호의 짝이 맞지 않습니다 (개수: ${dollarCount}개)`);
	}
	
	if (/\$\s*\$/g.test(text)) {
		issues.push('빈 LaTeX 수식이 있습니다');
	}
	
	// 수식 내부에 닫히지 않은 괄호 확인
	const mathBlocks = text.match(/\$[^$]+\$/g) || [];
	for (const block of mathBlocks) {
		const openParen = (block.match(/\(/g) || []).length;
		const closeParen = (block.match(/\)/g) || []).length;
		const openBrace = (block.match(/\{/g) || []).length;
		const closeBrace = (block.match(/\}/g) || []).length;
		
		if (openParen !== closeParen) {
			issues.push(`수식 내 괄호 불일치: ( ${openParen}개, ) ${closeParen}개`);
		}
		if (openBrace !== closeBrace) {
			issues.push(`수식 내 중괄호 불일치: { ${openBrace}개, } ${closeBrace}개`);
		}
	}
	
	return { valid: issues.length === 0, error: issues.length > 0 ? issues.join('; ') : null, issues };
}

function validateMathLogic(problem) {
	const issues = [];
	const warnings = [];
	
	// 난이도와 예상시간 일관성
	if (problem.난이도 && problem.예상시간) {
		const timeNum = parseInt(problem.예상시간) || 0;
		if (problem.난이도 === '하' && timeNum > 5) {
			warnings.push('난이도 "하"인데 예상시간이 5분 초과 (일반적으로 3-5분)');
		}
		if (problem.난이도 === '중' && (timeNum < 3 || timeNum > 10)) {
			warnings.push(`난이도 "중"인데 예상시간이 ${timeNum}분 (일반적으로 5-8분)`);
		}
		if (problem.난이도 === '상' && timeNum < 5) {
			warnings.push('난이도 "상"인데 예상시간이 5분 미만 (일반적으로 8-12분)');
		}
		if (problem.난이도 === '최상' && timeNum < 10) {
			issues.push('난이도 "최상"인데 예상시간이 10분 미만 (일반적으로 12-20분)');
		}
	}
	
	// 핵심개념과 소단원 일관성
	if (problem.소단원 && problem.핵심개념) {
		if (problem.소단원.includes('등차수열') && !problem.핵심개념.includes('등차') && !problem.핵심개념.includes('수열')) {
			warnings.push('소단원은 등차수열인데 핵심개념에 언급 없음');
		}
		if (problem.소단원.includes('등비수열') && !problem.핵심개념.includes('등비') && !problem.핵심개념.includes('수열')) {
			warnings.push('소단원은 등비수열인데 핵심개념에 언급 없음');
		}
		if (problem.소단원.includes('미분') && !problem.핵심개념.includes('미분')) {
			warnings.push('소단원에 미분이 있는데 핵심개념에 미분 언급 없음');
		}
		if (problem.소단원.includes('적분') && !problem.핵심개념.includes('적분')) {
			warnings.push('소단원에 적분이 있는데 핵심개념에 적분 언급 없음');
		}
	}
	
	// 문제구조 논리성
	if (problem.문제구조) {
		const steps = problem.문제구조.split('→').map(s => s.trim()).filter(s => s);
		if (steps.length < 2) {
			issues.push('문제구조가 1단계만 있음 (최소 2단계 필요)');
		}
		if (steps.length > 6) {
			warnings.push(`문제구조가 ${steps.length}단계로 너무 복잡함 (일반적으로 3-5단계)`);
		}
	}
	
	// LaTeX와 핵심개념 일관성
	if (problem.LaTeX예시 && problem.핵심개념) {
		if (problem.핵심개념.includes('미분') && !problem.LaTeX예시.includes('\\frac') && !problem.LaTeX예시.includes('d') && !problem.LaTeX예시.includes('\\prime') && !problem.LaTeX예시.includes("'")) {
			warnings.push('핵심개념에 미분이 있는데 LaTeX에 미분 기호 없음');
		}
		if (problem.핵심개념.includes('적분') && !problem.LaTeX예시.includes('\\int')) {
			warnings.push('핵심개념에 적분이 있는데 LaTeX에 적분 기호 없음');
		}
	}
	
	// 변형요소 타당성
	if (problem.변형요소) {
		const jsonCheck = checkJSON(problem.변형요소);
		if (jsonCheck.valid && jsonCheck.parsed) {
			const keys = Object.keys(jsonCheck.parsed);
			if (keys.length === 0) {
				issues.push('변형요소가 빈 객체입니다');
			}
		}
	}
	
	// 필수 필드 검증
	const requiredFields = ['문제ID', '출처', '대단원', '중단원', '소단원', '난이도', '핵심개념'];
	for (const field of requiredFields) {
		if (!problem[field] || problem[field].trim() === '') {
			issues.push(`필수 필드 누락: ${field}`);
		}
	}
	
	return { issues, warnings };
}

async function reviewP408Detail() {
	console.log('='.repeat(70));
	console.log('[미적분 P4 08번 상세 검토]');
	console.log('='.repeat(70));
	
	await rateLimiter.waitIfNeeded();
	
	const response = await notion.databases.query({
		database_id: databaseId,
		filter: {
			property: '문제ID',
			title: {
				equals: '미적분_2025학년도_현우진_드릴_P4_08'
			}
		},
		page_size: 1,
	});
	
	if (response.results.length === 0) {
		console.log('\n❌ 해당 항목을 찾을 수 없습니다.');
		return;
	}
	
	const page = response.results[0];
	const props = page.properties;
	
	const problem = {
		문제ID: getPropertyValue(props['문제ID']),
		출처: getPropertyValue(props['출처']),
		대단원: getPropertyValue(props['대단원']),
		중단원: getPropertyValue(props['중단원']),
		소단원: getPropertyValue(props['소단원']),
		난이도: getPropertyValue(props['난이도']),
		핵심개념: getPropertyValue(props['핵심개념']),
		LaTeX예시: getPropertyValue(props['LaTeX예시']),
		문제구조: getPropertyValue(props['문제구조']),
		핵심패턴: getPropertyValue(props['핵심패턴']),
		변형요소: getPropertyValue(props['변형요소']),
		난이도조절: getPropertyValue(props['난이도조절']),
		함정설계: getPropertyValue(props['함정설계']),
		출제의도: getPropertyValue(props['출제의도']),
		예상시간: getPropertyValue(props['예상시간']),
		선행개념: getPropertyValue(props['선행개념']),
		후행개념: getPropertyValue(props['후행개념'])
	};
	
	console.log('\n[항목 정보]');
	console.log('-'.repeat(70));
	console.log(`문제ID: ${problem.문제ID}`);
	console.log(`출처: ${problem.출처}`);
	console.log(`대단원: ${problem.대단원}`);
	console.log(`중단원: ${problem.중단원}`);
	console.log(`소단원: ${problem.소단원}`);
	console.log(`난이도: ${problem.난이도}`);
	console.log(`예상시간: ${problem.예상시간}`);
	console.log(`핵심개념: ${problem.핵심개념}`);
	console.log(`문제구조: ${problem.문제구조}`);
	console.log(`핵심패턴: ${problem.핵심패턴}`);
	console.log(`출제의도: ${problem.출제의도}`);
	
	console.log('\n[변형요소]');
	console.log('-'.repeat(70));
	console.log(problem.변형요소);
	
	console.log('\n[LaTeX예시]');
	console.log('-'.repeat(70));
	console.log(problem.LaTeX예시);
	
	// 검증
	console.log('\n' + '='.repeat(70));
	console.log('[검증 결과]');
	console.log('='.repeat(70));
	
	// JSON 검사
	console.log('\n[1] JSON 형식 검사');
	console.log('-'.repeat(70));
	const jsonCheck = checkJSON(problem.변형요소);
	if (jsonCheck.valid) {
		console.log('✅ JSON 형식 정상');
		if (jsonCheck.parsed) {
			console.log(`   키 개수: ${Object.keys(jsonCheck.parsed).length}`);
			console.log(`   키 목록: ${Object.keys(jsonCheck.parsed).join(', ')}`);
		}
	} else {
		console.log(`❌ JSON 오류: ${jsonCheck.error}`);
	}
	
	// LaTeX 검사
	console.log('\n[2] LaTeX 형식 검사');
	console.log('-'.repeat(70));
	const latexCheck = checkLaTeX(problem.LaTeX예시);
	if (latexCheck.valid) {
		console.log('✅ LaTeX 형식 정상');
		const dollarCount = (problem.LaTeX예시.match(/\$/g) || []).length;
		if (dollarCount > 0) {
			console.log(`   수식 개수: ${dollarCount / 2}개`);
		}
	} else {
		console.log(`❌ LaTeX 오류: ${latexCheck.error}`);
		if (latexCheck.issues && latexCheck.issues.length > 0) {
			latexCheck.issues.forEach(issue => {
				console.log(`   - ${issue}`);
			});
		}
	}
	
	// 수학적 논리 검토
	console.log('\n[3] 수학적 논리 타당성 검토');
	console.log('-'.repeat(70));
	const logicCheck = validateMathLogic(problem);
	
	if (logicCheck.issues.length === 0 && logicCheck.warnings.length === 0) {
		console.log('✅ 수학적 논리 타당성 정상');
	} else {
		if (logicCheck.issues.length > 0) {
			console.log(`❌ 수학적 논리 오류: ${logicCheck.issues.length}개`);
			logicCheck.issues.forEach(issue => {
				console.log(`   - ${issue}`);
			});
		}
		if (logicCheck.warnings.length > 0) {
			console.log(`\n⚠️  경고: ${logicCheck.warnings.length}개`);
			logicCheck.warnings.forEach(warning => {
				console.log(`   - ${warning}`);
			});
		}
	}
	
	// 원본 파일과 대조
	console.log('\n[4] 원본 파일 대조');
	console.log('-'.repeat(70));
	
	const downloadsPath = path.join(os.homedir(), 'Downloads');
	const files = fs.readdirSync(downloadsPath);
	const originalFile = files.find(f => 
		f.includes('미적분') && 
		f.includes('P4') && 
		f.includes('2025') &&
		f.endsWith('.csv')
	);
	
	if (originalFile) {
		console.log(`원본 파일: ${originalFile}`);
		// 원본 파일 읽기 (간단히)
		const filePath = path.join(downloadsPath, originalFile);
		let content = fs.readFileSync(filePath, 'utf-8');
		if (content.charCodeAt(0) === 0xFEFF) {
			content = content.slice(1);
		}
		
		// 08번 찾기
		const lines = content.split('\n');
		const targetLine = lines.find(line => line.includes('P4_08') || line.includes('P4_08'));
		
		if (targetLine) {
			console.log('✅ 원본 파일에서 해당 항목 발견');
			const parts = targetLine.split(',');
			if (parts.length > 0) {
				const originalVariation = parts.find(p => p.includes('{') && p.includes('}')) || '';
				if (originalVariation) {
					console.log(`원본 변형요소: ${originalVariation.substring(0, 100)}...`);
				}
			}
		} else {
			console.log('⚠️  원본 파일에서 해당 항목을 찾을 수 없습니다');
		}
	} else {
		console.log('⚠️  원본 파일을 찾을 수 없습니다');
	}
	
	console.log('\n' + '='.repeat(70));
	console.log('[검토 완료]');
	console.log('='.repeat(70));
}

reviewP408Detail();
