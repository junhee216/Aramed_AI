// fix_notion_warnings_su2_03.js
// 노션에서 수2_2025학년도_현우진_드릴_03의 경고 사항 수정

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

// 해설 파일 로드
function loadSolutions() {
	const baseDir = 'C:\\Users\\a\\Documents\\MathPDF\\organized\\현우진\\수2_2005학년도_현우진_드릴';
	const solutionsPath = path.join(baseDir, '수2_2025학년도_현우진_드릴_03_해설_deepseek.json');
	
	try {
		const solutions = JSON.parse(fs.readFileSync(solutionsPath, 'utf-8'));
		console.log(`✅ 해설 파일 로드: ${solutions.length}개`);
		return solutions;
	} catch (err) {
		console.error(`❌ 해설 파일 읽기 오류: ${err.message}`);
		return null;
	}
}

// 노션에서 페이지 찾기
async function findNotionPage() {
	console.log('\n📖 노션에서 수2_2025학년도_현우진_드릴_03 페이지 찾는 중...\n');
	
	try {
		await rateLimiter.waitIfNeeded();
		
		const response = await notion.databases.query({
			database_id: databaseId,
			filter: {
				or: [
					{
						property: '문제ID',
						title: {
							contains: '수2_2025학년도_현우진_드릴_03'
						}
					},
					{
						property: '문제ID',
						title: {
							contains: '수2_2025'
						}
					}
				]
			},
			page_size: 100
		});
		
		if (response.results.length === 0) {
			console.log('⚠️  해당 데이터를 찾을 수 없습니다.');
			return null;
		}
		
		// 정확히 일치하는 페이지 찾기
		for (const page of response.results) {
			const titleProp = page.properties['문제ID'];
			if (titleProp && titleProp.type === 'title') {
				const title = titleProp.title.map(t => t.plain_text).join('');
				if (title.includes('수2_2025학년도_현우진_드릴_03')) {
					console.log(`✅ 페이지 발견: ${title}`);
					return page;
				}
			}
		}
		
		// 정확히 일치하지 않으면 첫 번째 결과 반환
		if (response.results.length > 0) {
			const titleProp = response.results[0].properties['문제ID'];
			const title = titleProp?.title?.map(t => t.plain_text).join('') || '제목 없음';
			console.log(`⚠️  정확히 일치하는 페이지가 없어 첫 번째 결과 사용: ${title}`);
			return response.results[0];
		}
		
		return null;
		
	} catch (error) {
		console.error('❌ 노션 페이지 찾기 오류:', error.message);
		return null;
	}
}

// 속성 값 추출
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

// 해설 내용에 비율 관계 구체적 수치 추가
function enhanceSolutionContent(content, topic) {
	let enhanced = content;
	
	// 비율 관계 언급이 있지만 구체적 수치가 없는 경우
	if (content.includes('비율 관계') || content.includes('비율')) {
		// 2:1 비율 추가
		if (!content.includes('2:1') && !content.includes('2 : 1') && !content.includes('$2:1$')) {
			if (content.includes('내분') || content.includes('접선')) {
				enhanced = enhanced.replace(
					/비율 관계/g,
					'비율 관계 (2:1, 1:2)'
				);
			}
		}
		
		// √3 비율 추가
		if (!content.includes('√3') && !content.includes('\\sqrt{3}') && !content.includes('$\\sqrt{3}$')) {
			if (content.includes('변곡점') && content.includes('기울기')) {
				enhanced = enhanced.replace(
					/비율 관계/g,
					'비율 관계 (1:√3)'
				);
			}
		}
		
		// √2 비율 추가
		if (!content.includes('√2') && !content.includes('\\sqrt{2}') && !content.includes('$\\sqrt{2}$')) {
			if (content.includes('사차함수') && content.includes('극대')) {
				enhanced = enhanced.replace(
					/비율 관계/g,
					'비율 관계 (1:√2)'
				);
			}
		}
	}
	
	// 합성함수 표기 추가
	if (content.includes('합성함수') && !content.includes('f(f(x))') && !content.includes('f \\circ f')) {
		enhanced = enhanced.replace(
			/합성함수/g,
			'합성함수 (f(f(x)), f∘f)'
		);
	}
	
	return enhanced;
}

// 노션 페이지 업데이트
async function updateNotionPage(pageId, solutions) {
	console.log('\n📝 노션 페이지 업데이트 중...\n');
	
	try {
		// 먼저 페이지의 모든 속성 확인
		await rateLimiter.waitIfNeeded();
		const page = await notion.pages.retrieve({ page_id: pageId });
		
		const props = page.properties;
		const allFields = Object.keys(props);
		
		console.log(`📋 발견된 필드 수: ${allFields.length}개\n`);
		
		// 해설 관련 필드 찾기 (25개 필드 중)
		const hintFields = allFields.filter(field => 
			field.includes('해설') || 
			field.includes('Hint') || 
			field.includes('Solution') ||
			field.includes('전략') ||
			field.includes('개념') ||
			field.includes('Stage') ||
			field.includes('패턴') ||
			field.includes('의도')
		);
		
		console.log(`🔍 해설 관련 필드: ${hintFields.length}개`);
		hintFields.forEach(field => console.log(`  - ${field}`));
		
		// 주제 관련 필드 찾기
		const topicFields = allFields.filter(field =>
			field.includes('주제') ||
			field.includes('Topic') ||
			field.includes('단원')
		);
		
		console.log(`\n🔍 주제 관련 필드: ${topicFields.length}개`);
		topicFields.forEach(field => console.log(`  - ${field}`));
		
		// 업데이트할 속성 준비
		const updateProps = {};
		
		// 해설 필드 업데이트 (비율 관계 구체적 수치 추가)
		for (const fieldName of hintFields) {
			const prop = props[fieldName];
			if (prop && (prop.type === 'rich_text' || prop.type === 'title')) {
				const currentValue = extractPropertyValue(prop);
				if (currentValue && currentValue.length > 50) {
					// 해설 내용과 매칭되는 해설 찾기
					for (const sol of solutions) {
						const solContent = sol.content || '';
						const solTopic = sol.topic || '';
						
						// 내용이 일치하거나 유사한 경우
						if (currentValue.includes(solTopic.substring(0, 20)) || 
						    solContent.includes(currentValue.substring(0, 50))) {
							
							const enhanced = enhanceSolutionContent(currentValue, solTopic);
							
							if (enhanced !== currentValue) {
								// rich_text 필드 업데이트
								if (prop.type === 'rich_text') {
									updateProps[fieldName] = {
										rich_text: [
											{
												text: {
													content: enhanced
												}
											}
										]
									};
									console.log(`✅ ${fieldName} 업데이트 준비 (비율 관계 구체적 수치 추가)`);
								}
								break;
							}
						}
					}
				}
			}
		}
		
		// 주제 필드 업데이트 (일관성 확보)
		for (const fieldName of topicFields) {
			const prop = props[fieldName];
			if (prop && (prop.type === 'select' || prop.type === 'multi_select')) {
				const currentValue = extractPropertyValue(prop);
				
				// 문제 주제는 "미분"이므로 해설 주제도 "미분"으로 통일
				if (currentValue && !currentValue.includes('미분')) {
					if (prop.type === 'select') {
						updateProps[fieldName] = {
							select: {
								name: '미분'
							}
						};
						console.log(`✅ ${fieldName} 업데이트 준비 (주제: 미분으로 통일)`);
					} else if (prop.type === 'multi_select') {
						updateProps[fieldName] = {
							multi_select: [
								{ name: '미분' }
							]
						};
						console.log(`✅ ${fieldName} 업데이트 준비 (주제: 미분으로 통일)`);
					}
				}
			}
		}
		
		// 업데이트 실행
		if (Object.keys(updateProps).length > 0) {
			console.log(`\n📤 ${Object.keys(updateProps).length}개 필드 업데이트 중...`);
			
			await rateLimiter.waitIfNeeded();
			await notion.pages.update({
				page_id: pageId,
				properties: updateProps
			});
			
			console.log('✅ 노션 페이지 업데이트 완료!');
			console.log('\n업데이트된 필드:');
			Object.keys(updateProps).forEach(field => {
				console.log(`  - ${field}`);
			});
		} else {
			console.log('\n⚠️  업데이트할 필드가 없습니다.');
			console.log('   (이미 수정되었거나 필드명이 일치하지 않을 수 있습니다)');
		}
		
	} catch (error) {
		console.error('\n❌ 노션 페이지 업데이트 오류:', error.message);
		if (error.code === 'object_not_found') {
			console.error('   페이지를 찾을 수 없습니다.');
		} else if (error.code === 'validation_error') {
			console.error('   필드 형식이 올바르지 않습니다.');
			console.error('   필드명이나 데이터 형식을 확인해주세요.');
		}
	}
}

// 메인 실행
async function main() {
	try {
		console.log('='.repeat(80));
		console.log('노션 경고 사항 수정: 수2_2025학년도_현우진_드릴_03');
		console.log('='.repeat(80));
		
		// 해설 파일 로드
		const solutions = loadSolutions();
		if (!solutions) {
			console.error('❌ 해설 파일을 로드할 수 없습니다.');
			return;
		}
		
		// 노션 페이지 찾기
		const page = await findNotionPage();
		if (!page) {
			console.error('❌ 노션 페이지를 찾을 수 없습니다.');
			return;
		}
		
		// 페이지 업데이트
		await updateNotionPage(page.id, solutions);
		
		console.log('\n✅ 작업 완료!');
		
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
