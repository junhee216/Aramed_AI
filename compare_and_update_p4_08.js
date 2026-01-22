// compare_and_update_p4_08.js
// 제공된 25개 필드 데이터와 P4 08번 비교 및 업데이트

import 'dotenv/config';
import { Client } from '@notionhq/client';

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

// 제공된 데이터
const providedData = {
	문제ID: '미적분_2025학년도_현우진_드릴_04_17',
	출처: '자체교재',
	대단원: '미적분',
	중단원: '여러 가지 미분법',
	소단원: '절댓값 함수의 미분가능성',
	난이도: '최상',
	핵심개념: '절댓값 합성함수의 미분가능 조건',
	LaTeX예시: '|g(x)| = |f(\\cos x)\\sin x|',
	문제구조: '조건제시→미분가능성분석→인수추론→수열대입',
	핵심패턴: '|h(x)|가 x=a에서 미분가능 \\iff h(a)=0 \\text{ 이면 } h\'(a)=0',
	변형요소: '{"최고차항계수":[5,10,1],"상수_k":["1이 아닌 양수","k>1"],"항번호":[10,12]}',
	난이도조절: '쉽게: \\sin x 단독 절댓값으로 구성 / 어렵게: f(\\cos x)와의 합성 구조 및 k배 조각 정의 결합',
	함정설계: '1. \\sin x의 부호가 변하는 n\\pi 지점 고려 누락 2. f(\\cos x)가 0이 되는 지점의 중근 조건 간과 3. k값에 따른 연결 지점 미분계수 일치성 오판',
	출제의도: '절댓값을 포함한 복합 함수의 미분가능성을 기하적(접점)으로 해석하여 다항식을 결정하는 능력',
	유사유형: '절댓값 미분가능;합성함수 미분;삼각함수 성질',
	선행개념: '수학II 절댓값 미분;삼각함수 그래프;합성함수 미분법',
	후행개념: '정적분으로 정의된 함수의 미분가능성',
	예상시간: '12',
	실수포인트: '1. \\sin x = 0인 지점에서 f(\\cos x)가 0이 아닐 경우 첨점 발생 주의 2. \\cos x의 범위 [-1, 1] 제한 조건 망각 3. kf(1)=f(1) 등의 특수 상황 계산 실수',
	개념연결: '수학II 미분가능성 심화와 미적분 삼각함수의 하이엔드 융합',
	검증상태: '승인됨',
	AI신뢰도: '98',
	수정이력: '2025-01-15: Claude 초기생성',
	사용빈도: '0',
	학생반응: '미평가'
};

function pythonDictToJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return null;
	}
	
	let result = text.trim();
	result = result.replace(/'([^']+)'\s*:/g, '"$1":');
	
	result = result.replace(/\[([^\]]+)\]/g, (match, content) => {
		const items = [];
		let current = '';
		let depth = 0;
		
		for (let i = 0; i < content.length; i++) {
			const char = content[i];
			if (char === '(' || char === '[') {
				depth++;
				current += char;
			} else if (char === ')' || char === ']') {
				depth--;
				current += char;
			} else if (char === ',' && depth === 0) {
				items.push(current.trim());
				current = '';
			} else {
				current += char;
			}
		}
		if (current.trim()) {
			items.push(current.trim());
		}
		
		const processedItems = items.map(item => {
			item = item.trim();
			if (item.startsWith("'") && item.endsWith("'")) {
				const content = item.slice(1, -1);
				const escaped = content
					.replace(/\\/g, '\\\\')
					.replace(/"/g, '\\"')
					.replace(/\n/g, '\\n')
					.replace(/\r/g, '\\r')
					.replace(/\t/g, '\\t');
				return '"' + escaped + '"';
			}
			if (/^-?\d+(\.\d+)?$/.test(item)) {
				return item;
			}
			if (item.startsWith('"') && item.endsWith('"')) {
				return item;
			}
			const escaped = item
				.replace(/\\/g, '\\\\')
				.replace(/"/g, '\\"')
				.replace(/\n/g, '\\n')
				.replace(/\r/g, '\\r')
				.replace(/\t/g, '\\t');
			return '"' + escaped + '"';
		});
		
		return '[' + processedItems.join(', ') + ']';
	});
	
	try {
		const parsed = JSON.parse(result);
		return JSON.stringify(parsed, null, 0);
	} catch (e) {
		return null;
	}
}

async function compareAndUpdate() {
	console.log('='.repeat(70));
	console.log('[P4 08번 데이터 비교 및 업데이트]');
	console.log('='.repeat(70));
	
	// Notion에서 P4_08 찾기
	await rateLimiter.waitIfNeeded();
	
	const response = await notion.databases.query({
		database_id: databaseId,
		filter: {
			or: [
				{
					property: '문제ID',
					title: {
						equals: '미적분_2025학년도_현우진_드릴_P4_08'
					}
				},
				{
					property: '문제ID',
					title: {
						contains: '미적분_2025학년도_현우진_드릴_04_17'
					}
				}
			]
		},
		page_size: 1,
	});
	
	if (response.results.length === 0) {
		console.log('\n❌ 해당 항목을 찾을 수 없습니다.');
		return;
	}
	
	const page = response.results[0];
	const props = page.properties;
	
	// 현재 데이터 가져오기
	const currentData = {
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
		유사유형: getPropertyValue(props['유사유형']),
		선행개념: getPropertyValue(props['선행개념']),
		후행개념: getPropertyValue(props['후행개념']),
		예상시간: getPropertyValue(props['예상시간']),
		실수포인트: getPropertyValue(props['실수포인트']),
		개념연결: getPropertyValue(props['개념연결']),
		검증상태: getPropertyValue(props['검증상태']),
		AI신뢰도: getPropertyValue(props['AI신뢰도']),
		수정이력: getPropertyValue(props['수정이력']),
		사용빈도: getPropertyValue(props['사용빈도']),
		학생반응: getPropertyValue(props['학생반응'])
	};
	
	console.log('\n[현재 데이터 vs 제공된 데이터 비교]');
	console.log('-'.repeat(70));
	
	const differences = [];
	const updates = {};
	
	// 각 필드 비교
	const fieldsToCompare = [
		'출처', '대단원', '중단원', '소단원', '난이도', '핵심개념',
		'LaTeX예시', '문제구조', '핵심패턴', '변형요소', '난이도조절',
		'함정설계', '출제의도', '유사유형', '선행개념', '후행개념',
		'예상시간', '실수포인트', '개념연결', '검증상태', 'AI신뢰도',
		'수정이력', '사용빈도', '학생반응'
	];
	
	for (const field of fieldsToCompare) {
		const current = currentData[field] || '';
		const provided = providedData[field] || '';
		
		if (current !== provided) {
			differences.push({
				필드: field,
				현재: current.substring(0, 50) + (current.length > 50 ? '...' : ''),
				제공: provided.substring(0, 50) + (provided.length > 50 ? '...' : '')
			});
			
			// 업데이트할 데이터 준비
			if (field === '변형요소') {
				// JSON 형식으로 변환
				const jsonText = provided.startsWith('{') ? provided : pythonDictToJSON(provided);
				if (jsonText) {
					updates[field] = {
						rich_text: [{ text: { content: jsonText } }]
					};
				}
			} else if (field === '예상시간' || field === 'AI신뢰도' || field === '사용빈도') {
				const num = parseInt(provided);
				if (!isNaN(num)) {
					updates[field] = { number: num };
				} else {
					updates[field] = {
						rich_text: [{ text: { content: provided } }]
					};
				}
			} else if (field === '난이도' || field === '검증상태' || field === '출처' || 
			           field === '수정이력' || field === '대단원' || field === '중단원' || 
			           field === '학생반응') {
				// select 타입 필드
				updates[field] = { select: { name: provided } };
			} else {
				// rich_text 타입 필드
				updates[field] = {
					rich_text: [{ text: { content: provided } }]
				};
			}
		}
	}
	
	if (differences.length === 0) {
		console.log('✅ 모든 필드가 일치합니다. 업데이트할 내용이 없습니다.');
		return;
	}
	
	console.log(`\n⚠️  ${differences.length}개 필드에서 차이 발견:\n`);
	
	differences.forEach(diff => {
		console.log(`[${diff.필드}]`);
		console.log(`  현재: ${diff.현재}`);
		console.log(`  제공: ${diff.제공}`);
		console.log();
	});
	
	// 업데이트 실행
	console.log('='.repeat(70));
	console.log('[Notion 업데이트 실행]');
	console.log('='.repeat(70));
	
	await rateLimiter.waitIfNeeded();
	
	try {
		await notion.pages.update({
			page_id: page.id,
			properties: updates
		});
		
		console.log(`\n✅ ${Object.keys(updates).length}개 필드 업데이트 완료!`);
		console.log('\n[업데이트된 필드]:');
		Object.keys(updates).forEach(field => {
			console.log(`  - ${field}`);
		});
		
	} catch (error) {
		console.error(`\n❌ 업데이트 실패: ${error.message}`);
		if (error.body) {
			console.error(`상세: ${JSON.stringify(error.body, null, 2)}`);
		}
	}
	
	console.log('\n' + '='.repeat(70));
	console.log('[완료]');
	console.log('='.repeat(70));
}

compareAndUpdate();
