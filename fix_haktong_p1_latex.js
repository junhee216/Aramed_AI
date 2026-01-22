// fix_haktong_p1_latex.js
// 확통 P1 LaTeX 오류 수정

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

async function updatePage(pageId, latexText) {
	await rateLimiter.waitIfNeeded();
	
	try {
		await notion.pages.update({
			page_id: pageId,
			properties: {
				'LaTeX예시': {
					rich_text: [{ text: { content: latexText } }]
				}
			}
		});
		return true;
	} catch (error) {
		console.error(`  [오류] ${error.message}`);
		return false;
	}
}

async function fixLaTeX() {
	console.log('='.repeat(70));
	console.log('[확통 P1 LaTeX 오류 수정]');
	console.log('='.repeat(70));
	
	await rateLimiter.waitIfNeeded();
	
	const response = await notion.databases.query({
		database_id: databaseId,
		filter: {
			property: '문제ID',
			title: {
				contains: '확통_2024학년도_현우진_드릴_P1_03'
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
	const latex = getPropertyValue(props['LaTeX예시']);
	
	console.log(`\n[1] ${problemId}`);
	console.log('-'.repeat(70));
	console.log(`LaTeX 원본: ${latex}`);
	console.log(`길이: ${latex.length}자\n`);
	
	// $ 기호 개수 확인
	const dollarCount = (latex.match(/\$/g) || []).length;
	console.log(`$ 기호 개수: ${dollarCount}개\n`);
	
	// $ 기호 수정
	let fixedLatex = latex;
	
	// $$로 끝나는 경우 (빈 수식 블록) -> $...$ 형식으로 변경
	if (latex.endsWith('$$') && !latex.startsWith('$$')) {
		// 끝의 $$를 $로 변경하고 앞에 $ 추가
		fixedLatex = '$' + latex.slice(0, -2) + '$';
		console.log(`수정된 LaTeX: ${fixedLatex}\n`);
		
		const success = await updatePage(page.id, fixedLatex);
		if (success) {
			console.log('  ✅ LaTeX 수정 완료\n');
		} else {
			console.log('  ❌ 수정 실패\n');
		}
	} else if (dollarCount % 2 !== 0) {
		// $ 기호가 홀수인 경우
		if (latex.endsWith('$')) {
			// 끝에 $가 있으면 앞에 $ 추가
			fixedLatex = '$' + latex;
		} else {
			// 끝에 $가 없으면 끝에 $ 추가
			fixedLatex = latex + '$';
		}
		console.log(`수정된 LaTeX: ${fixedLatex}\n`);
		
		const success = await updatePage(page.id, fixedLatex);
		if (success) {
			console.log('  ✅ LaTeX 수정 완료\n');
		} else {
			console.log('  ❌ 수정 실패\n');
		}
	} else {
		console.log('  ℹ️  $ 기호가 짝수입니다. 다른 문제일 수 있습니다.\n');
	}
	
	console.log('='.repeat(70));
	console.log('[완료]');
	console.log('='.repeat(70));
}

fixLaTeX();
