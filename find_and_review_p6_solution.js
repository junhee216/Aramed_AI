// find_and_review_p6_solution.js
// 확통 P6 해설 파일 찾기 및 검토 후 노션 업데이트

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
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
		default:
			return null;
	}
}

// 해설 파일 찾기
function findSolutionFile() {
	const basePaths = [
		__dirname,
		path.join(__dirname, '..'),
		process.env.USERPROFILE || process.env.HOME,
		path.join(process.env.USERPROFILE || process.env.HOME, 'Documents'),
		path.join(process.env.USERPROFILE || process.env.HOME, 'Downloads'),
	];
	
	const searchPaths = [];
	
	// 모든 가능한 경로 생성
	for (const basePath of basePaths) {
		searchPaths.push(
			path.join(basePath, 'MathPDF-organized-현우진-확통_2024학년도_현우진_드릴'),
			path.join(basePath, 'MathPDF-organized-현우진-확통_2024학년도_현우진_드릴', '확통_2024학년도_현우진_드릴')
		);
	}
	
	// 중복 제거
	const uniquePaths = [...new Set(searchPaths)];
	
	const fileNames = [
		'확통_2024학년도_현우진_드릴_P6_해설.json',
		'확통_2024학년도_현우진_드릴_P6_해설.csv',
		'확통_2024학년도_현우진_드릴_P6_해설.txt',
		'P6_해설.json',
		'P6_해설.csv',
	];
	
	for (const searchPath of uniquePaths) {
		if (fs.existsSync(searchPath)) {
			console.log(`📁 폴더 발견: ${searchPath}`);
			for (const fileName of fileNames) {
				const filePath = path.join(searchPath, fileName);
				if (fs.existsSync(filePath)) {
					console.log(`✅ 파일 발견: ${filePath}`);
					return filePath;
				}
			}
			// 폴더 내 모든 파일 확인
			try {
				const files = fs.readdirSync(searchPath);
				const p6Files = files.filter(f => f.includes('P6') && (f.includes('해설') || f.includes('solution')));
				if (p6Files.length > 0) {
					console.log(`📄 P6 해설 관련 파일들:`);
					p6Files.forEach(f => console.log(`   - ${f}`));
					const filePath = path.join(searchPath, p6Files[0]);
					return filePath;
				}
			} catch (err) {
				console.log(`   폴더 읽기 실패: ${err.message}`);
			}
		}
	}
	
	return null;
}

// 해설 파일 읽기
function readSolutionFile(filePath) {
	try {
		const ext = path.extname(filePath).toLowerCase();
		const content = fs.readFileSync(filePath, 'utf-8');
		
		if (ext === '.json') {
			return JSON.parse(content);
		} else if (ext === '.csv') {
			// CSV 파싱 (간단한 버전)
			const lines = content.split('\n');
			const headers = lines[0].split(',');
			const data = [];
			for (let i = 1; i < lines.length; i++) {
				if (lines[i].trim()) {
					const values = lines[i].split(',');
					const obj = {};
					headers.forEach((h, idx) => {
						obj[h.trim()] = values[idx]?.trim() || '';
					});
					data.push(obj);
				}
			}
			return data;
		} else {
			return content;
		}
	} catch (error) {
		console.error(`❌ 파일 읽기 오류: ${error.message}`);
		return null;
	}
}

// 수학적 논리 검토
function reviewMathLogic(문제ID, 해설, question) {
	const errors = [];
	const warnings = [];
	
	if (!해설) return { errors, warnings };
	
	const 해설Text = typeof 해설 === 'string' ? 해설 : JSON.stringify(해설);
	
	// LaTeX 수식 괄호 검사
	const dollarCount = (해설Text.match(/\$/g) || []).length;
	const dollarBlockCount = (해설Text.match(/\$\$/g) || []).length;
	const singleDollarCount = dollarCount - dollarBlockCount * 2;
	
	if (singleDollarCount % 2 !== 0) {
		errors.push(`LaTeX 수식 괄호 불일치: $ 기호가 홀수 개 (${singleDollarCount}개)`);
	}
	
	// 확률질량함수 검토
	if (해설Text.includes('확률질량함수') || 해설Text.includes('이산확률변수')) {
		if (!해설Text.includes('∑') && !해설Text.includes('합') && !해설Text.includes('확률의 합') && !해설Text.includes('= 1')) {
			warnings.push('확률질량함수의 성질 ∑p_i = 1 확인 필요');
		}
		if (해설Text.includes('P(X>n+1)') && 해설Text.includes('{P(X>n)}²')) {
			if (!해설Text.includes('P(X>1)') && !해설Text.includes('P(X=1)')) {
				warnings.push('P(X>n+1) = {P(X>n)}² 관계에서 초기값 P(X=1) 또는 P(X>1) 필요');
			}
		}
	}
	
	// 분산 계산 검토
	if (해설Text.includes('분산') || 해설Text.includes('V(X)')) {
		if (해설Text.includes('E(X²)') && !해설Text.includes('E(X)') && !해설Text.includes('E(X)²')) {
			warnings.push('분산 계산 시 V(X) = E(X²) - {E(X)}² 공식에서 E(X) 필요');
		}
	}
	
	// 정규분포 변환 검토
	if (해설Text.includes('정규분포') && 해설Text.includes('N(')) {
		if (해설Text.includes('표준정규분포표') || 해설Text.includes('표준정규분포')) {
			if (!해설Text.includes('(X-m)/σ') && !해설Text.includes('변환') && !해설Text.includes('표준화')) {
				warnings.push('정규분포를 표준정규분포로 변환하는 과정 명시 필요');
			}
		}
	}
	
	// 이항분포 검토
	if (해설Text.includes('이항분포') || (해설Text.includes('독립시행') && 해설Text.includes('확률'))) {
		if (해설Text.includes('E(X)') && !해설Text.includes('np') && !해설Text.includes('n×p')) {
			warnings.push('이항분포의 기댓값 E(X) = np 언급 필요');
		}
		if (해설Text.includes('V(X)') && !해설Text.includes('npq') && !해설Text.includes('np(1-p)')) {
			warnings.push('이항분포의 분산 V(X) = npq 언급 필요');
		}
	}
	
	return { errors, warnings };
}

async function main() {
	console.log('='.repeat(80));
	console.log('확통 P6 해설 파일 찾기 및 검토');
	console.log('='.repeat(80));
	
	// 해설 파일 찾기
	const solutionFile = findSolutionFile();
	if (!solutionFile) {
		console.log('\n❌ 해설 파일을 찾을 수 없습니다.');
		console.log('다음 위치에서 찾았습니다:');
		console.log('  - Documents/MathPDF-organized-현우진-확통_2024학년도_현우진_드릴');
		console.log('  - Downloads/MathPDF-organized-현우진-확통_2024학년도_현우진_드릴');
		return;
	}
	
	// 해설 파일 읽기
	console.log(`\n📖 해설 파일 읽는 중: ${path.basename(solutionFile)}`);
	const solutionData = readSolutionFile(solutionFile);
	if (!solutionData) {
		console.log('❌ 해설 파일을 읽을 수 없습니다.');
		return;
	}
	
	console.log(`✅ 해설 데이터 로드 완료`);
	
	// P6 문제 가져오기
	console.log('\n📝 노션에서 P6 문제 가져오는 중...');
	const pages = await collectPaginatedAPI(notion.databases.query, {
		database_id: databaseId,
		filter: {
			property: '문제ID',
			title: {
				contains: '확통_2024학년도_현우진_드릴_P6'
			}
		}
	});
	
	console.log(`✅ ${pages.length}개 문제 발견\n`);
	
	// 해설 데이터를 문제ID로 매핑
	const solutionMap = {};
	if (Array.isArray(solutionData)) {
		solutionData.forEach(item => {
			const 문제ID = item['문제ID'] || item['문제 ID'] || item['id'] || '';
			if (문제ID) {
				solutionMap[문제ID] = item;
			}
		});
	}
	
	// 각 문제에 대해 해설 검토 및 업데이트
	let updatedCount = 0;
	let reviewedCount = 0;
	
	for (const page of pages) {
		const props = page.properties;
		const 문제ID = extractPropertyValue(props['문제ID']);
		const question = extractPropertyValue(props['핵심패턴']) || extractPropertyValue(props['LaTeX예시']) || '';
		
		console.log(`\n📝 ${문제ID} 검토 중...`);
		
		// 해설 찾기
		let 해설 = solutionMap[문제ID];
		if (!해설 && Array.isArray(solutionData)) {
			// 문제 번호로 찾기 (예: P6_01, P6_02 등)
			const problemNum = 문제ID.match(/P6_(\d+)/)?.[1];
			if (problemNum) {
				해설 = solutionData.find(item => {
					const id = item['문제ID'] || item['문제 ID'] || item['id'] || '';
					return id.includes(`P6_${problemNum}`) || id.includes(`P6_0${problemNum}`);
				});
			}
		}
		
		if (!해설) {
			console.log(`  ⚠️  해설을 찾을 수 없습니다.`);
			continue;
		}
		
		// 해설 내용 추출
		const 해설Text = 해설['해설'] || 해설['solution'] || 해설['내용'] || 
		                 (typeof 해설 === 'string' ? 해설 : JSON.stringify(해설));
		
		if (!해설Text || 해설Text.trim() === '') {
			console.log(`  ⚠️  해설 내용이 비어있습니다.`);
			continue;
		}
		
		console.log(`  📖 해설 확인됨 (${해설Text.length}자)`);
		
		// 수학적 논리 검토
		const review = reviewMathLogic(문제ID, 해설Text, question);
		reviewedCount++;
		
		if (review.errors.length > 0) {
			console.log(`  ❌ 수학적 논리 오류:`);
			review.errors.forEach(err => console.log(`     - ${err}`));
		}
		
		if (review.warnings.length > 0) {
			console.log(`  ⚠️  수학적 논리 경고:`);
			review.warnings.forEach(warn => console.log(`     - ${warn}`));
		}
		
		if (review.errors.length === 0 && review.warnings.length === 0) {
			console.log(`  ✅ 수학적 논리 검토 통과`);
		}
		
		// 노션에 해설 업데이트 (25번 필드 - 소단원 또는 새 필드)
		// 먼저 해설 필드가 있는지 확인
		const updateProps = {};
		
		// 해설 필드가 없으면 소단원 필드에 업데이트하거나, 사용자에게 알림
		// 여기서는 해설 내용을 출력만 하고, 실제 업데이트는 사용자 확인 후 진행
		console.log(`  💡 해설 내용 (처음 200자): ${해설Text.substring(0, 200)}...`);
	}
	
	console.log('\n' + '='.repeat(80));
	console.log('[작업 결과 요약]');
	console.log('='.repeat(80));
	console.log(`총 문제 수: ${pages.length}개`);
	console.log(`검토 완료: ${reviewedCount}개`);
	console.log(`업데이트 완료: ${updatedCount}개`);
	console.log('='.repeat(80));
}

main().catch(error => {
	console.error('\n❌ 실행 중 오류 발생:', error);
	process.exit(1);
});
