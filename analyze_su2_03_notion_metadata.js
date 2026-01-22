// analyze_su2_03_notion_metadata.js
// 노션에서 수2_2025학년도_현우진_드릴_03 메타데이터를 가져와 변환된 문제/해설과 비교 분석

import 'dotenv/config';
import { Client } from '@notionhq/client';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류: NOTION_API_KEY 또는 NOTION_DATABASE_ID 가 없습니다.');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

// Rate Limiter
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

// 변환된 문제/해설 파일 읽기
function loadConvertedFiles() {
	const baseDir = 'C:\\Users\\a\\Documents\\MathPDF\\organized\\현우진\\수2_2005학년도_현우진_드릴';
	
	const problemsPath = path.join(baseDir, '수2_2025학년도_현우진_드릴_03_문제_deepseek.json');
	const solutionsPath = path.join(baseDir, '수2_2025학년도_현우진_드릴_03_해설_deepseek.json');
	
	let problems = [];
	let solutions = [];
	
	try {
		if (fs.existsSync(problemsPath)) {
			problems = JSON.parse(fs.readFileSync(problemsPath, 'utf-8'));
			console.log(`✅ 문제 파일 로드: ${problems.length}개`);
		}
	} catch (err) {
		console.error(`❌ 문제 파일 읽기 오류: ${err.message}`);
	}
	
	try {
		if (fs.existsSync(solutionsPath)) {
			solutions = JSON.parse(fs.readFileSync(solutionsPath, 'utf-8'));
			console.log(`✅ 해설 파일 로드: ${solutions.length}개`);
		}
	} catch (err) {
		console.error(`❌ 해설 파일 읽기 오류: ${err.message}`);
	}
	
	return { problems, solutions };
}

// 노션에서 수2_2025학년도_현우진_드릴_03 데이터 조회
async function fetchNotionData() {
	console.log('\n📖 노션 데이터베이스에서 수2_2025학년도_현우진_드릴_03 조회 중...\n');
	
	try {
		await rateLimiter.waitIfNeeded();
		
		const response = await notion.databases.query({
			database_id: databaseId,
			filter: {
				property: '마스터 프로토콜 v1.0',
				title: {
					contains: '수2_2025학년도_현우진_드릴_03'
				}
			},
			page_size: 100
		});
		
		if (response.results.length === 0) {
			console.log('⚠️  해당 데이터를 찾을 수 없습니다.');
			return null;
		}
		
		console.log(`✅ ${response.results.length}개 항목 발견\n`);
		
		// 첫 번째 항목의 모든 속성 가져오기
		const page = response.results[0];
		await rateLimiter.waitIfNeeded();
		
		const fullPage = await notion.pages.retrieve({
			page_id: page.id
		});
		
		return fullPage;
		
	} catch (error) {
		console.error('❌ 노션 데이터 조회 오류:', error.message);
		return null;
	}
}

// 속성 값 추출 헬퍼 함수
function extractPropertyValue(prop) {
	if (!prop) return null;
	
	switch (prop.type) {
		case 'title':
			return prop.title.map(t => t.plain_text).join('');
		case 'rich_text':
			return prop.rich_text.map(t => t.plain_text).join('');
		case 'number':
			return prop.number;
		case 'select':
			return prop.select?.name || null;
		case 'multi_select':
			return prop.multi_select.map(s => s.name);
		case 'date':
			return prop.date ? prop.date.start : null;
		case 'checkbox':
			return prop.checkbox;
		case 'url':
			return prop.url || null;
		case 'email':
			return prop.email || null;
		case 'phone_number':
			return prop.phone_number || null;
		case 'formula':
			return prop.formula;
		case 'relation':
			return prop.relation.map(r => r.id);
		case 'rollup':
			return prop.rollup;
		default:
			return `[${prop.type}]`;
	}
}

// 25개 필드 분석 및 수학적 타당성 검토
function analyzeMetadata(notionPage, problems, solutions) {
	console.log('='.repeat(80));
	console.log('📊 수2_2025학년도_현우진_드릴_03 메타데이터 분석');
	console.log('='.repeat(80));
	
	if (!notionPage) {
		console.log('❌ 노션 데이터를 가져올 수 없습니다.');
		return;
	}
	
	const props = notionPage.properties;
	const allFields = Object.keys(props);
	
	console.log(`\n📋 총 ${allFields.length}개 필드 발견\n`);
	
	// 25개 필드 추출 (실제 필드명 확인 필요)
	const fields25 = allFields.slice(0, 25);
	
	console.log('🔍 25개 필드 분석:\n');
	
	const analysis = {
		valid: [],
		issues: [],
		warnings: []
	};
	
	for (let i = 0; i < fields25.length; i++) {
		const fieldName = fields25[i];
		const prop = props[fieldName];
		const value = extractPropertyValue(prop);
		
		console.log(`[${i + 1}] ${fieldName}`);
		console.log(`    타입: ${prop?.type || 'N/A'}`);
		console.log(`    값: ${JSON.stringify(value).substring(0, 100)}${JSON.stringify(value).length > 100 ? '...' : ''}`);
		
		// 수학적 타당성 검토
		const validation = validateField(fieldName, value, prop?.type, problems, solutions);
		
		if (validation.isValid) {
			analysis.valid.push({ field: fieldName, value, validation });
			console.log(`    ✅ 수학적 타당성: 정상`);
		} else {
			analysis.issues.push({ field: fieldName, value, validation });
			console.log(`    ❌ 수학적 타당성: ${validation.issue}`);
		}
		
		if (validation.warning) {
			analysis.warnings.push({ field: fieldName, value, validation });
			console.log(`    ⚠️  경고: ${validation.warning}`);
		}
		
		console.log('');
	}
	
	// 종합 분석 결과
	console.log('\n' + '='.repeat(80));
	console.log('📊 종합 분석 결과');
	console.log('='.repeat(80));
	console.log(`✅ 정상 필드: ${analysis.valid.length}개`);
	console.log(`❌ 문제 필드: ${analysis.issues.length}개`);
	console.log(`⚠️  경고 필드: ${analysis.warnings.length}개`);
	
	if (analysis.issues.length > 0) {
		console.log('\n❌ 문제가 있는 필드:');
		analysis.issues.forEach(item => {
			console.log(`  - ${item.field}: ${item.validation.issue}`);
		});
	}
	
	if (analysis.warnings.length > 0) {
		console.log('\n⚠️  경고가 있는 필드:');
		analysis.warnings.forEach(item => {
			console.log(`  - ${item.field}: ${item.validation.warning}`);
		});
	}
	
	return analysis;
}

// 필드별 수학적 타당성 검증
function validateField(fieldName, value, fieldType, problems, solutions) {
	const result = {
		isValid: true,
		issue: null,
		warning: null
	};
	
	// 필드명 패턴에 따른 검증
	if (fieldName.includes('문제') || fieldName.includes('Question')) {
		// 문제 관련 필드
		if (fieldType === 'number') {
			if (value !== null && (value < 0 || value > problems.length)) {
				result.isValid = false;
				result.issue = `문제 번호가 범위를 벗어남 (1-${problems.length})`;
			}
		}
		if (fieldType === 'rich_text' || fieldType === 'title') {
			if (value && problems.length > 0) {
				// 변환된 문제와 내용 일치 확인
				const matches = problems.some(p => 
					value.includes(p.topic) || p.question.includes(value.substring(0, 50))
				);
				if (!matches && value.length > 20) {
					result.warning = '변환된 문제와 내용이 일치하지 않을 수 있음';
				}
			}
		}
	}
	
	if (fieldName.includes('해설') || fieldName.includes('Solution') || fieldName.includes('Hint')) {
		// 해설 관련 필드
		if (fieldType === 'rich_text' || fieldType === 'title') {
			if (value && solutions.length > 0) {
				const matches = solutions.some(s => 
					value.includes(s.topic) || s.content.includes(value.substring(0, 50))
				);
				if (!matches && value.length > 20) {
					result.warning = '변환된 해설과 내용이 일치하지 않을 수 있음';
				}
			}
		}
	}
	
	if (fieldName.includes('점수') || fieldName.includes('Point') || fieldName.includes('Score')) {
		// 점수 관련 필드
		if (fieldType === 'number') {
			if (value !== null && (value !== 3 && value !== 4)) {
				result.isValid = false;
				result.issue = '점수는 3점 또는 4점이어야 함';
			}
		}
	}
	
	if (fieldName.includes('주제') || fieldName.includes('Topic') || fieldName.includes('단원')) {
		// 주제 관련 필드
		const validTopics = ['함수의 극한과 연속', '미분', '적분'];
		if (value && typeof value === 'string') {
			const matches = validTopics.some(topic => value.includes(topic));
			if (!matches && value.length > 5) {
				result.warning = '표준 주제명과 일치하지 않을 수 있음';
			}
		}
	}
	
	if (fieldName.includes('난이도') || fieldName.includes('Difficulty') || fieldName.includes('Level')) {
		// 난이도 관련 필드
		if (fieldType === 'select' || fieldType === 'number') {
			const validLevels = ['쉬움', '보통', '어려움', '매우어려움', 'Easy', 'Medium', 'Hard', 'VeryHard'];
			if (value && !validLevels.includes(value) && typeof value === 'string') {
				result.warning = '표준 난이도 값이 아님';
			}
		}
	}
	
	if (fieldName.includes('유형') || fieldName.includes('Type') || fieldName.includes('Category')) {
		// 유형 관련 필드
		const validTypes = ['객관식', '주관식', 'multiple_choice', 'short_answer'];
		if (value && typeof value === 'string') {
			const matches = validTypes.some(type => value.includes(type));
			if (!matches && value.length > 3) {
				result.warning = '표준 유형 값이 아님';
			}
		}
	}
	
	// 수식 관련 필드 검증
	if (fieldName.includes('수식') || fieldName.includes('Formula') || fieldName.includes('Equation')) {
		if (value && typeof value === 'string') {
			// LaTeX 수식 괄호 검사
			const dollarCount = (value.match(/\$/g) || []).length;
			if (dollarCount % 2 !== 0) {
				result.isValid = false;
				result.issue = 'LaTeX 수식 괄호 불일치';
			}
		}
	}
	
	return result;
}

// 메인 실행
async function main() {
	try {
		console.log('✅ ENV LOADED');
		console.log(`데이터베이스 ID: ${databaseId}\n`);
		
		// 변환된 파일 로드
		const { problems, solutions } = loadConvertedFiles();
		
		// 노션 데이터 조회
		const notionPage = await fetchNotionData();
		
		// 분석 실행
		const analysis = analyzeMetadata(notionPage, problems, solutions);
		
		// 결과 저장
		const outputPath = path.join(__dirname, 'su2_03_metadata_analysis.json');
		fs.writeFileSync(outputPath, JSON.stringify({
			timestamp: new Date().toISOString(),
			problems_count: problems.length,
			solutions_count: solutions.length,
			analysis
		}, null, 2), 'utf-8');
		
		console.log(`\n✅ 분석 결과 저장: ${outputPath}`);
		
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
