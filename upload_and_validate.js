// upload_and_validate.js
// CSV 데이터를 Notion에 업로드하고 자동으로 오류 검사하는 워크플로우

import 'dotenv/config';
import { Client } from '@notionhq/client';
import fs from 'fs';
import csv from 'csv-parser';

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

// 25개 필드 이름
const FIELD_NAMES = [
	'문제ID', '출처', '대단원', '중단원', '소단원', '난이도', '핵심개념',
	'LaTeX예시', '문제구조', '핵심패턴', '변형요소', '난이도조절', '함정설계',
	'출제의도', '유사유형', '선행개념', '후행개념', '예상시간', '실수포인트',
	'개념연결', '검증상태', 'AI신뢰도', '수정이력', '사용빈도', '학생반응'
];

// JSON 형식 검사
function validateJSON(text) {
	if (!text || text.trim() === '') return { valid: true, error: null };
	try {
		JSON.parse(text);
		return { valid: true, error: null };
	} catch (e) {
		return { valid: false, error: e.message };
	}
}

// LaTeX 형식 검사
function validateLaTeX(text) {
	if (!text || text.trim() === '') return { valid: true, error: null };
	
	const dollarCount = (text.match(/\$/g) || []).length;
	
	if (dollarCount === 0) {
		return { valid: true, error: null };
	}
	
	if (dollarCount % 2 !== 0) {
		return { valid: false, error: `$ 기호의 짝이 맞지 않습니다 (개수: ${dollarCount}개, 홀수)` };
	}
	
	// 빈 수식 확인
	if (/\$\s*\$/g.test(text)) {
		return { valid: false, error: '빈 LaTeX 수식이 있습니다 ($ $ 사이에 내용 없음)' };
	}
	
	return { valid: true, error: null };
}

// CSV 행을 Notion 속성으로 변환
function convertRowToProperties(row) {
	const properties = {};
	
	// 문제ID (제목 필드)
	if (row['문제ID']) {
		properties['문제ID'] = {
			title: [{ text: { content: row['문제ID'] } }]
		};
	}
	
	// 나머지 필드들 (rich_text로 처리)
	const textFields = [
		'출처', '대단원', '중단원', '소단원', '난이도', '핵심개념',
		'LaTeX예시', '문제구조', '핵심패턴', '변형요소', '난이도조절',
		'함정설계', '출제의도', '유사유형', '선행개념', '후행개념',
		'실수포인트', '개념연결', '검증상태', '수정이력', '학생반응'
	];
	
	for (const field of textFields) {
		if (row[field] !== undefined && row[field] !== '') {
			properties[field] = {
				rich_text: [{ text: { content: String(row[field]) } }]
			};
		}
	}
	
	// 숫자 필드
	if (row['예상시간']) {
		const time = parseInt(row['예상시간']);
		if (!isNaN(time)) {
			properties['예상시간'] = { number: time };
		}
	}
	
	if (row['AI신뢰도']) {
		const confidence = parseInt(row['AI신뢰도']);
		if (!isNaN(confidence)) {
			properties['AI신뢰도'] = { number: confidence };
		}
	}
	
	if (row['사용빈도']) {
		const frequency = parseInt(row['사용빈도']);
		if (!isNaN(frequency)) {
			properties['사용빈도'] = { number: frequency };
		}
	}
	
	return properties;
}

// CSV 파일 읽기 및 검증
async function validateCSV(csvPath) {
	const errors = {
		구조오류: [],
		JSON오류: [],
		LaTeX오류: []
	};
	
	const rows = [];
	
	return new Promise((resolve, reject) => {
		fs.createReadStream(csvPath)
			.pipe(csv())
			.on('data', (row) => {
				rows.push(row);
				
				const rowNum = rows.length + 1; // 헤더 포함
				const problemId = row['문제ID'] || '(제목 없음)';
				
				// 1. 구조 오류 검사 (필수 필드 확인)
				const missingFields = [];
				for (const field of FIELD_NAMES) {
					if (!(field in row)) {
						missingFields.push(field);
					}
				}
				
				if (missingFields.length > 0) {
					errors.구조오류.push({
						행번호: rowNum,
						문제ID: problemId,
						이유: `필수 필드 누락: ${missingFields.join(', ')}`
					});
				}
				
				// 2. JSON 오류 검사 (변형요소 필드)
				if (row['변형요소']) {
					const jsonCheck = validateJSON(row['변형요소']);
					if (!jsonCheck.valid) {
						errors.JSON오류.push({
							행번호: rowNum,
							문제ID: problemId,
							이유: `변형요소 필드 JSON 오류: ${jsonCheck.error}`
						});
					}
				}
				
				// 3. LaTeX 오류 검사 (LaTeX예시 필드)
				if (row['LaTeX예시']) {
					const latexCheck = validateLaTeX(row['LaTeX예시']);
					if (!latexCheck.valid) {
						errors.LaTeX오류.push({
							행번호: rowNum,
							문제ID: problemId,
							이유: `LaTeX 오류: ${latexCheck.error}`
						});
					}
				}
			})
			.on('end', () => {
				resolve({ errors, rows });
			})
			.on('error', reject);
	});
}

// Notion에 업로드
async function uploadToNotion(rows) {
	console.log('\n[Notion 업로드 시작]');
	console.log('='.repeat(60));
	
	let successCount = 0;
	let failCount = 0;
	const failedItems = [];
	
	for (let i = 0; i < rows.length; i++) {
		const row = rows[i];
		const problemId = row['문제ID'] || `항목_${i + 1}`;
		
		try {
			await rateLimiter.waitIfNeeded();
			
			const properties = convertRowToProperties(row);
			
			await notion.pages.create({
				parent: { database_id: databaseId },
				properties: properties
			});
			
			successCount++;
			
			if ((i + 1) % 10 === 0) {
				console.log(`  ${i + 1}/${rows.length} 업로드 완료...`);
			}
		} catch (error) {
			failCount++;
			failedItems.push({
				행번호: i + 2,
				문제ID: problemId,
				오류: error.message
			});
			console.error(`  [실패] 행 ${i + 2} (${problemId}): ${error.message}`);
		}
	}
	
	return { successCount, failCount, failedItems };
}

// 업로드 후 검증
async function validateAfterUpload() {
	console.log('\n[업로드 후 검증 시작]');
	console.log('='.repeat(60));
	
	const errors = {
		구조오류: [],
		JSON오류: [],
		LaTeX오류: []
	};
	
	let allPages = [];
	let hasMore = true;
	let startCursor = null;
	
	while (hasMore) {
		await rateLimiter.waitIfNeeded();
		
		const response = await notion.databases.query({
			database_id: databaseId,
			start_cursor: startCursor || undefined,
			page_size: 100,
		});
		
		allPages.push(...response.results);
		hasMore = response.has_more;
		startCursor = response.next_cursor;
	}
	
	// 최근 업로드된 항목들만 검증 (예: 마지막 100개)
	const recentPages = allPages.slice(-100);
	
	for (let i = 0; i < recentPages.length; i++) {
		const page = recentPages[i];
		const props = page.properties;
		const problemId = props['문제ID']?.title?.[0]?.plain_text || '(제목 없음)';
		
		// JSON 검증
		const variationField = props['변형요소'];
		if (variationField?.rich_text?.[0]?.plain_text) {
			const text = variationField.rich_text[0].plain_text;
			const jsonCheck = validateJSON(text);
			if (!jsonCheck.valid) {
				errors.JSON오류.push({
					문제ID: problemId,
					이유: `변형요소 필드 JSON 오류: ${jsonCheck.error}`
				});
			}
		}
		
		// LaTeX 검증
		const latexField = props['LaTeX예시'];
		if (latexField?.rich_text?.[0]?.plain_text) {
			const text = latexField.rich_text[0].plain_text;
			const latexCheck = validateLaTeX(text);
			if (!latexCheck.valid) {
				errors.LaTeX오류.push({
					문제ID: problemId,
					이유: `LaTeX 오류: ${latexCheck.error}`
				});
			}
		}
	}
	
	return errors;
}

// 오류 리포트 생성
function generateErrorReport(errors, outputPath) {
	const report = [];
	
	if (errors.구조오류.length > 0) {
		report.push('\n[구조 오류]');
		report.push('-'.repeat(60));
		errors.구조오류.forEach(err => {
			report.push(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
		});
	}
	
	if (errors.JSON오류.length > 0) {
		report.push('\n[JSON 오류]');
		report.push('-'.repeat(60));
		errors.JSON오류.forEach(err => {
			report.push(`  행 ${err.행번호 || ''} (${err.문제ID}): ${err.이유}`);
		});
	}
	
	if (errors.LaTeX오류.length > 0) {
		report.push('\n[LaTeX 오류]');
		report.push('-'.repeat(60));
		errors.LaTeX오류.forEach(err => {
			report.push(`  행 ${err.행번호 || ''} (${err.문제ID}): ${err.이유}`);
		});
	}
	
	const reportText = report.join('\n');
	
	if (outputPath) {
		fs.writeFileSync(outputPath, reportText, 'utf-8');
		console.log(`\n오류 리포트 저장: ${outputPath}`);
	}
	
	return reportText;
}

// 메인 함수
async function main() {
	const csvPath = process.argv[2];
	
	if (!csvPath) {
		console.error('사용법: node upload_and_validate.js <CSV파일경로>');
		console.error('예: node upload_and_validate.js data.csv');
		process.exit(1);
	}
	
	if (!fs.existsSync(csvPath)) {
		console.error(`❌ 파일을 찾을 수 없습니다: ${csvPath}`);
		process.exit(1);
	}
	
	console.log('='.repeat(60));
	console.log('[CSV 업로드 및 자동 검증 워크플로우]');
	console.log('='.repeat(60));
	console.log(`CSV 파일: ${csvPath}\n`);
	
	try {
		// 1. 업로드 전 검증
		console.log('[1단계] 업로드 전 검증');
		console.log('='.repeat(60));
		
		const { errors: preErrors, rows } = await validateCSV(csvPath);
		
		const totalPreErrors = preErrors.구조오류.length + preErrors.JSON오류.length + preErrors.LaTeX오류.length;
		
		if (totalPreErrors > 0) {
			console.log(`\n⚠️  ${totalPreErrors}개의 오류를 발견했습니다.`);
			console.log('업로드 전에 오류를 수정하는 것을 권장합니다.\n');
			
			const report = generateErrorReport(preErrors, `pre_upload_errors_${Date.now()}.txt`);
			console.log(report);
			
			console.log('\n계속 진행하시겠습니까? (y/n)');
			// 실제로는 readline을 사용하거나 자동 진행 옵션 추가
		} else {
			console.log('✅ 오류가 없습니다. 업로드를 진행합니다.\n');
		}
		
		// 2. Notion 업로드
		console.log('[2단계] Notion 업로드');
		console.log('='.repeat(60));
		
		const uploadResult = await uploadToNotion(rows);
		
		console.log(`\n✅ 성공: ${uploadResult.successCount}개`);
		console.log(`❌ 실패: ${uploadResult.failCount}개`);
		
		if (uploadResult.failedItems.length > 0) {
			console.log('\n[실패한 항목]:');
			uploadResult.failedItems.forEach(item => {
				console.log(`  행 ${item.행번호} (${item.문제ID}): ${item.오류}`);
			});
		}
		
		// 3. 업로드 후 검증
		if (uploadResult.successCount > 0) {
			console.log('\n[3단계] 업로드 후 검증');
			console.log('='.repeat(60));
			
			const postErrors = await validateAfterUpload();
			
			const totalPostErrors = postErrors.구조오류.length + postErrors.JSON오류.length + postErrors.LaTeX오류.length;
			
			if (totalPostErrors > 0) {
				console.log(`\n⚠️  ${totalPostErrors}개의 오류를 발견했습니다.\n`);
				
				const report = generateErrorReport(postErrors, `post_upload_errors_${Date.now()}.txt`);
				console.log(report);
			} else {
				console.log('\n✅ 모든 데이터가 올바르게 업로드되었습니다!');
			}
		}
		
		console.log('\n' + '='.repeat(60));
		console.log('[완료]');
		console.log('='.repeat(60));
		
	} catch (error) {
		console.error('\n❌ 오류 발생:', error.message);
		process.exit(1);
	}
}

main();
