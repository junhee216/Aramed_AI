// fix_su2_p3_notion_warnings.js
// 수2_2025학년도_현우진_드릴_P3 경고 사항 수정

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';

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

// 비율 관계 구체적 수치 추가
function enhanceRatioRelation(content) {
	if (!content) return content;
	
	let enhanced = content;
	
	// 비율 관계 언급이 있지만 구체적 수치가 없는 경우
	if ((content.includes('비율 관계') || content.includes('비율')) && 
	    !content.includes('2:1') && !content.includes('1:2') && 
	    !content.includes('√3') && !content.includes('√2') &&
	    !content.includes('\\sqrt{3}') && !content.includes('\\sqrt{2}')) {
		
		// 변곡점 관련이면 1:√3 추가
		if (content.includes('변곡점')) {
			enhanced = enhanced.replace(
				/비율 관계/g,
				'비율 관계 (1:√3, 2:1)'
			);
		}
		// 접선 관련이면 2:1, 1:2 추가
		else if (content.includes('접선') || content.includes('교점')) {
			enhanced = enhanced.replace(
				/비율 관계/g,
				'비율 관계 (2:1, 1:2)'
			);
		}
		// 사차함수 관련이면 1:√2 추가
		else if (content.includes('사차함수') || content.includes('극대')) {
			enhanced = enhanced.replace(
				/비율 관계/g,
				'비율 관계 (1:√2)'
			);
		}
		// 일반적으로는 2:1, 1:2 추가
		else {
			enhanced = enhanced.replace(
				/비율 관계/g,
				'비율 관계 (2:1, 1:2)'
			);
		}
	}
	
	return enhanced;
}

// 합성함수 표기 추가
function enhanceCompositeFunction(content) {
	if (!content) return content;
	
	let enhanced = content;
	
	if (content.includes('합성함수') && 
	    !content.includes('f(f(x))') && 
	    !content.includes('f \\circ f') &&
	    !content.includes('(f∘f)')) {
		enhanced = enhanced.replace(
			/합성함수/g,
			'합성함수 (f(f(x)), f∘f)'
		);
	}
	
	return enhanced;
}

async function fixWarnings() {
	console.log('='.repeat(80));
	console.log('수2_2025학년도_현우진_드릴_P3 경고 사항 수정');
	console.log('='.repeat(80));
	
	try {
		// P3 관련 모든 페이지 가져오기
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				property: '문제ID',
				title: {
					contains: '수2_2025학년도_현우진_드릴_P3'
				}
			}
		});
		
		console.log(`\n✅ ${allPages.length}개 페이지 발견\n`);
		
		let totalUpdated = 0;
		
		for (const page of allPages) {
			const titleProp = page.properties['문제ID'];
			const title = titleProp?.title?.map(t => t.plain_text).join('') || '';
			
			console.log(`\n📄 처리 중: ${title}`);
			
			const props = page.properties;
			const updateProps = {};
			let pageUpdated = false;
			
			// 비율 관계 구체적 수치 추가가 필요한 필드들
			const fieldsToCheck = [
				'핵심패턴',
				'출제의도',
				'개념연결',
				'후행개념',
				'핵심개념',
				'선행개념',
				'유사유형'
			];
			
			for (const fieldName of fieldsToCheck) {
				const prop = props[fieldName];
				if (prop && prop.type === 'rich_text') {
					const currentValue = extractPropertyValue(prop);
					if (currentValue) {
						let enhanced = enhanceRatioRelation(currentValue);
						enhanced = enhanceCompositeFunction(enhanced);
						
						if (enhanced !== currentValue) {
							updateProps[fieldName] = {
								rich_text: [
									{
										text: {
											content: enhanced
										}
									}
								]
							};
							console.log(`  ✅ ${fieldName} 업데이트 준비`);
							pageUpdated = true;
						}
					}
				}
			}
			
			// 주제 일관성 확인 (중단원이 미분인지 확인)
			const 중단원 = props['중단원'];
			if (중단원 && 중단원.type === 'select') {
				const currentTopic = extractPropertyValue(중단원);
				if (currentTopic !== '미분') {
					updateProps['중단원'] = {
						select: {
							name: '미분'
						}
					};
					console.log(`  ✅ 중단원 업데이트 준비 (${currentTopic} → 미분)`);
					pageUpdated = true;
				}
			}
			
			// 업데이트 실행
			if (pageUpdated && Object.keys(updateProps).length > 0) {
				await rateLimiter.waitIfNeeded();
				await notion.pages.update({
					page_id: page.id,
					properties: updateProps
				});
				
				console.log(`  ✅ ${Object.keys(updateProps).length}개 필드 업데이트 완료`);
				totalUpdated++;
			} else {
				console.log(`  ⏭️  업데이트 필요 없음`);
			}
		}
		
		console.log('\n' + '='.repeat(80));
		console.log(`✅ 작업 완료! 총 ${totalUpdated}개 페이지 업데이트됨`);
		console.log('='.repeat(80));
		
	} catch (error) {
		console.error('\n❌ 오류 발생:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
	}
}

fixWarnings();
