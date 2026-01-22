// check_haktong_p1_json_error.js
// 확통 P1 JSON 오류 항목 상세 확인 및 수정

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
		default:
			return '';
	}
}

function pythonDictToJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return null;
	}
	
	let result = text.trim();
	
	// 수동 파싱으로 키-값 쌍 추출 (키에 작은따옴표가 포함된 경우 처리)
	const pairs = [];
	let i = 1; // 첫 번째 '{' 건너뛰기
	let currentKey = '';
	let currentValue = '';
	let inKey = false;
	let inValue = false;
	let keyStart = -1;
	let depth = 0;
	
	while (i < result.length - 1) { // 마지막 '}' 전까지
		const char = result[i];
		
		if (char === "'" && !inValue) {
			if (!inKey) {
				// 키 시작
				inKey = true;
				keyStart = i + 1;
			} else {
				// 키 끝 확인 (다음 문자가 ':'인지 확인)
				let j = i + 1;
				while (j < result.length && (result[j] === ' ' || result[j] === '\t')) {
					j++;
				}
				if (j < result.length && result[j] === ':') {
					// 키 끝
					currentKey = result.substring(keyStart, i);
					inKey = false;
					i = j; // ':' 위치로 이동
					continue;
				}
				// 키 내부의 작은따옴표
			}
		} else if (char === ':' && !inKey && !inValue) {
			// 값 시작
			inValue = true;
			let j = i + 1;
			while (j < result.length && (result[j] === ' ' || result[j] === '\t')) {
				j++;
			}
			if (j < result.length && result[j] === '[') {
				// 배열 값
				let arrayStart = j;
				depth = 1;
				j++;
				while (j < result.length && depth > 0) {
					if (result[j] === '[') depth++;
					if (result[j] === ']') depth--;
					j++;
				}
				currentValue = result.substring(arrayStart, j);
				pairs.push({ key: currentKey, value: currentValue });
				currentKey = '';
				currentValue = '';
				inValue = false;
				i = j - 1;
				continue;
			} else {
				// 배열이 아닌 값 (숫자, 문자열 등)
				let valueStart = j;
				while (j < result.length) {
					if (result[j] === ',' || result[j] === '}') {
						break;
					}
					j++;
				}
				currentValue = result.substring(valueStart, j).trim();
				pairs.push({ key: currentKey, value: currentValue });
				currentKey = '';
				currentValue = '';
				inValue = false;
				i = j - 1;
				continue;
			}
		} else if (char === ',' && !inKey && depth === 0) {
			// 다음 키-값 쌍
			inValue = false;
		}
		
		i++;
	}
	
	// 수동 파싱이 실패하면 기존 방법 사용
	if (pairs.length === 0) {
		// 키에 작은따옴표가 포함된 경우를 더 정교하게 처리
		result = result.replace(/'([^']*(?:'[^':]*)*)'\s*:/g, (match, key) => {
			const escapedKey = key.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
			return `"${escapedKey}":`;
		});
	} else {
		// 수동 파싱 결과로 재구성
		const jsonPairs = pairs.map(pair => {
			const key = `"${pair.key.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
			// 값 처리
			let value = pair.value.trim();
			
			// 배열인 경우
			if (value.startsWith('[') && value.endsWith(']')) {
				value = value.replace(/\[([^\]]+)\]/g, (match, content) => {
					const items = content.split(',').map(item => {
						item = item.trim();
						if (item.startsWith("'") && item.endsWith("'")) {
							const content = item.slice(1, -1);
							return `"${content.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
						}
						if (/^-?\d+(\.\d+)?$/.test(item)) {
							return item;
						}
						return `"${item.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
					});
					return '[' + items.join(', ') + ']';
				});
			} else {
				// 배열이 아닌 경우 (숫자, 문자열 등)
				if (value.startsWith("'") && value.endsWith("'")) {
					value = `"${value.slice(1, -1).replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
				} else if (/^-?\d+(\.\d+)?$/.test(value)) {
					// 숫자는 그대로
				} else {
					value = `"${value.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
				}
			}
			
			return `${key}: ${value}`;
		});
		result = '{' + jsonPairs.join(', ') + '}';
	}
	
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

async function updatePage(pageId, jsonText) {
	await rateLimiter.waitIfNeeded();
	
	try {
		await notion.pages.update({
			page_id: pageId,
			properties: {
				'변형요소': {
					rich_text: [{ text: { content: jsonText } }]
				}
			}
		});
		return true;
	} catch (error) {
		console.error(`  [오류] ${error.message}`);
		return false;
	}
}

async function checkAndFixError() {
	console.log('='.repeat(70));
	console.log('[확통 P1 JSON 오류 항목 상세 확인 및 수정]');
	console.log('='.repeat(70));
	
	await rateLimiter.waitIfNeeded();
	
	const response = await notion.databases.query({
		database_id: databaseId,
		filter: {
			property: '문제ID',
			title: {
				contains: '확통_2024학년도_현우진_드릴_P1_06'
			}
		},
		page_size: 100,
	});
	
	const items = response.results;
	
	if (items.length === 0) {
		console.log('\n⚠️  항목을 찾을 수 없습니다.\n');
		return;
	}
	
	const page = items[0];
	const props = page.properties;
	const problemId = getPropertyValue(props['문제ID']);
	const variation = getPropertyValue(props['변형요소']);
	
	console.log(`\n[1] ${problemId}`);
	console.log('-'.repeat(70));
	console.log(`변형요소 원본: ${variation}`);
	console.log(`길이: ${variation.length}자\n`);
	
	// 여러 방법으로 변환 시도
	let converted = null;
	
	// 방법 1: 기본 변환
	converted = pythonDictToJSON(variation);
	
	// 방법 2: 빈 객체인 경우
	if (!converted && (variation.trim() === '{}' || variation.trim() === '')) {
		converted = '{}';
	}
	
	// 방법 3: 특수 문자 처리
	if (!converted) {
		// 작은따옴표가 키에만 있는 경우
		let temp = variation.trim();
		// 첫 번째 작은따옴표를 큰따옴표로
		temp = temp.replace(/^'/, '"');
		// 키의 작은따옴표를 큰따옴표로
		temp = temp.replace(/'([^']+)'\s*:/g, '"$1":');
		converted = pythonDictToJSON(temp);
	}
	
	if (converted) {
		try {
			JSON.parse(converted);
			const success = await updatePage(page.id, converted);
			if (success) {
				console.log('  ✅ 변환 및 수정 완료');
				console.log(`  변환된 JSON: ${converted.substring(0, 100)}...\n`);
			} else {
				console.log('  ❌ 업데이트 실패\n');
			}
		} catch (e) {
			console.log(`  ❌ 변환된 JSON도 파싱 실패: ${e.message}\n`);
		}
	} else {
		console.log('  ❌ 변환 실패\n');
	}
	
	console.log('='.repeat(70));
	console.log('[완료]');
	console.log('='.repeat(70));
}

checkAndFixError();
