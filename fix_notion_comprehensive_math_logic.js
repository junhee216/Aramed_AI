// fix_notion_comprehensive_math_logic.js
// 전체 노션 데이터베이스 종합 수정 (수학적 논리 심도 고려)

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
		case 'date':
			return prop.date;
		case 'checkbox':
			return prop.checkbox;
		case 'url':
			return prop.url;
		default:
			return null;
	}
}

// 수학적 개념 추출 및 분석 (심도있게)
function extractMathConcepts(question, topic, 핵심개념) {
	const concepts = [];
	
	if (!question) return concepts;
	
	const q = question.toLowerCase();
	
	// 극한 관련
	if (q.includes('\\lim') || q.includes('극한')) {
		concepts.push('극한');
		if (q.includes('\\frac') && q.includes('0')) {
			concepts.push('0/0 꼴 극한');
		}
		if (q.includes('\\infty')) {
			concepts.push('무한대 극한');
		}
		if (q.includes('연속')) {
			concepts.push('연속성');
		}
	}
	
	// 미분 관련
	if (q.includes('미분가능') || q.includes('f\'') || q.includes('도함수')) {
		concepts.push('미분가능성');
		if (q.includes('\\begin{cases}')) {
			concepts.push('구간별 함수의 미분가능성');
		}
		if (q.includes('|f(x)|')) {
			concepts.push('절댓값 함수의 미분가능성');
		}
		if (q.includes('접선')) {
			concepts.push('접선');
		}
		if (q.includes('극값')) {
			concepts.push('극값');
		}
		if (q.includes('변곡점')) {
			concepts.push('변곡점');
		}
	}
	
	// 적분 관련
	if (q.includes('\\int') || q.includes('적분')) {
		concepts.push('적분');
		if (q.includes('넓이')) {
			concepts.push('정적분과 넓이');
		}
		if (q.includes('|f\'')) {
			concepts.push('절댓값 도함수의 정적분');
		}
		if (q.includes('정적분')) {
			concepts.push('정적분');
		}
	}
	
	// 삼차함수 관련
	if (q.includes('삼차함수') || 핵심개념?.toLowerCase().includes('삼차함수')) {
		concepts.push('삼차함수');
		if (q.includes('비율') || 핵심개념?.toLowerCase().includes('비율')) {
			concepts.push('삼차함수 비율 관계');
		}
		if (q.includes('변곡점') || 핵심개념?.toLowerCase().includes('변곡점')) {
			concepts.push('삼차함수 변곡점 대칭성');
		}
		if (q.includes('접선') || 핵심개념?.toLowerCase().includes('접선')) {
			concepts.push('삼차함수 접선의 비율 관계');
		}
	}
	
	// 합성함수 관련
	if (q.includes('f(f(x))') || q.includes('합성함수')) {
		concepts.push('합성함수');
		concepts.push('합성함수 방정식의 대응 관계');
	}
	
	// 집합 관련
	if (q.includes('a=') && q.includes('b=')) {
		concepts.push('집합 연산');
		concepts.push('함수의 교점/접점 관계');
	}
	
	// 확통 관련
	if (q.includes('경우의 수') || q.includes('순열') || q.includes('조합')) {
		concepts.push('경우의 수');
		if (q.includes('원형') || q.includes('원순열')) {
			concepts.push('원순열');
		}
		if (q.includes('이웃') || q.includes('이웃하지')) {
			concepts.push('이웃하는 것/이웃하지 않는 것');
		}
		if (q.includes('부정방정식') || q.includes('음이 아닌 정수')) {
			concepts.push('부정방정식의 정수해');
			concepts.push('중복조합');
		}
		if (q.includes('여사건') || q.includes('드모르간')) {
			concepts.push('여사건');
			concepts.push('드모르간의 법칙');
		}
		if (q.includes('순서가 정해진') || q.includes('≤')) {
			concepts.push('순서가 정해진 배열');
		}
	}
	
	// 수1 관련
	if (q.includes('수열') || q.includes('등차') || q.includes('등비')) {
		concepts.push('수열');
		if (q.includes('등차')) {
			concepts.push('등차수열');
		}
		if (q.includes('등비')) {
			concepts.push('등비수열');
		}
	}
	
	if (q.includes('로그') || q.includes('log')) {
		concepts.push('로그');
		if (q.includes('밑변환')) {
			concepts.push('밑변환공식');
		}
	}
	
	if (q.includes('삼각함수') || q.includes('sin') || q.includes('cos')) {
		concepts.push('삼각함수');
		if (q.includes('덧셈정리')) {
			concepts.push('삼각함수 덧셈정리');
		}
	}
	
	return concepts;
}

// 해설에 수학적 개념이 포함되어 있는지 확인
function checkConceptInSolution(concepts, 해설) {
	if (!해설 || !Array.isArray(해설)) return false;
	
	const solutionText = 해설.join(' ').toLowerCase();
	
	for (const concept of concepts) {
		const conceptLower = concept.toLowerCase();
		// 직접 포함 또는 관련 키워드 포함
		if (solutionText.includes(conceptLower) || 
			solutionText.includes(conceptLower.replace('함수', '')) ||
			solutionText.includes(conceptLower.replace('관계', ''))) {
			return true;
		}
	}
	
	return false;
}

// 수학적으로 타당한 해설 보완 제안
function suggestSolutionEnhancement(문제, 핵심개념, 중단원, 해설) {
	const suggestions = [];
	
	if (!문제) return suggestions;
	
	const concepts = extractMathConcepts(문제, 중단원, 핵심개념);
	const solutionText = Array.isArray(해설) ? 해설.join(' ') : (해설 || '');
	
	// 삼차함수 비율 관계
	if (concepts.includes('삼차함수 비율 관계')) {
		if (!solutionText.includes('2:1') && !solutionText.includes('1:2') && !solutionText.includes('√3')) {
			suggestions.push('삼차함수 비율 관계에서 구체적 수치(2:1, 1:2, 1:√3)를 명시해야 합니다.');
		}
	}
	
	// 합성함수
	if (concepts.includes('합성함수')) {
		if (!solutionText.includes('합성함수') && !solutionText.includes('f(f(x))') && !solutionText.includes('f∘f')) {
			suggestions.push('합성함수 (f(f(x)), f∘f)의 개념을 명시해야 합니다.');
		}
	}
	
	// 미분가능성
	if (concepts.includes('구간별 함수의 미분가능성')) {
		if (!solutionText.includes('연속') && !solutionText.includes('미분계수')) {
			suggestions.push('구간별 함수의 미분가능성에서 연속성과 미분계수 일치를 확인해야 합니다.');
		}
	}
	
	// 정적분과 넓이
	if (concepts.includes('정적분과 넓이')) {
		if (!solutionText.includes('넓이') && !solutionText.includes('정적분')) {
			suggestions.push('정적분과 넓이의 관계를 명시해야 합니다.');
		}
	}
	
	// 원순열
	if (concepts.includes('원순열')) {
		if (!solutionText.includes('회전') && !solutionText.includes('원순열')) {
			suggestions.push('원순열에서 회전하여 일치하는 것은 같은 것으로 본다는 점을 명시해야 합니다.');
		}
		if (!solutionText.includes('순열')) {
			suggestions.push('원순열에서 무엇 하나라도 배치하고 나면 순열로 바뀐다는 점을 명시해야 합니다.');
		}
	}
	
	// 이웃하는 것/이웃하지 않는 것
	if (concepts.includes('이웃하는 것/이웃하지 않는 것')) {
		if (!solutionText.includes('이웃') && !solutionText.includes('여사건')) {
			suggestions.push('이웃하지 않는 것의 여사건을 이용하는 방법을 명시해야 합니다.');
		}
	}
	
	// 부정방정식
	if (concepts.includes('부정방정식의 정수해')) {
		if (!solutionText.includes('중복조합') && !solutionText.includes('H_')) {
			suggestions.push('부정방정식의 정수해는 중복조합으로 다룰 수 있음을 명시해야 합니다.');
		}
	}
	
	return suggestions;
}

// 유사유형을 원리공유문제에 통합
function integrateSimilarTypes(유사유형, 원리공유문제) {
	if (!유사유형) return 원리공유문제;
	
	const 유형List = Array.isArray(유사유형) ? 유사유형 : [유사유형];
	const 유형Text = 유형List.join(', ');
	
	if (!원리공유문제) {
		return `유사유형: ${유형Text}`;
	}
	
	// 원리공유문제에 유사유형이 포함되어 있는지 확인
	for (const 유형 of 유형List) {
		if (!원리공유문제.includes(유형)) {
			return `${원리공유문제}; 유사유형: ${유형}`;
		}
	}
	
	return 원리공유문제;
}

async function fixComprehensiveIssues() {
	console.log('='.repeat(80));
	console.log('[전체 노션 데이터베이스 종합 수정]');
	console.log('수학적 논리 심도 고려');
	console.log('='.repeat(80));
	
	try {
		// 모든 페이지 가져오기
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId
		});
		
		console.log(`\n📖 총 ${allPages.length}개 페이지 발견\n`);
		
		let fixedCount = 0;
		const fixReports = [];
		
		// 각 페이지 수정
		for (let i = 0; i < allPages.length; i++) {
			const page = allPages[i];
			const props = page.properties;
			
			const 문제ID = extractPropertyValue(props['문제ID']);
			const 대단원 = extractPropertyValue(props['대단원']);
			const 중단원 = extractPropertyValue(props['중단원']);
			const 핵심개념 = extractPropertyValue(props['핵심개념']);
			const 유사유형 = extractPropertyValue(props['유사유형']);
			const 원리공유문제 = extractPropertyValue(props['원리공유문제']);
			const 핵심패턴 = extractPropertyValue(props['핵심패턴']);
			const LaTeX예시 = extractPropertyValue(props['LaTeX예시']);
			// 해설 관련 필드가 없으므로 개념 관련 필드 사용
			const 개념연결 = extractPropertyValue(props['개념연결']);
			const 후행개념 = extractPropertyValue(props['후행개념']);
			const 선행개념 = extractPropertyValue(props['선행개념']);
			
			const updateProps = {};
			const pageFixes = [];
			
			// 1. 대단원 필드 통일
			if (문제ID) {
				if (문제ID.includes('수1_') && 대단원 === '수학I') {
					updateProps['대단원'] = {
						select: {
							name: '수1'
						}
					};
					pageFixes.push('대단원: 수학I → 수1');
				} else if (문제ID.includes('수2_') && (대단원 === '수학II' || 대단원 === '미분' || 대단원 === '적분')) {
					updateProps['대단원'] = {
						select: {
							name: '수2'
						}
					};
					pageFixes.push(`대단원: ${대단원} → 수2`);
				} else if (문제ID.includes('미적분_') && 대단원 !== '미적분') {
					updateProps['대단원'] = {
						select: {
							name: '미적분'
						}
					};
					pageFixes.push(`대단원: ${대단원} → 미적분`);
				} else if (문제ID.includes('확통_') && 대단원 !== '확률과 통계') {
					updateProps['대단원'] = {
						select: {
							name: '확률과 통계'
						}
					};
					pageFixes.push(`대단원: ${대단원} → 확률과 통계`);
				}
			}
			
			// 2. 원리공유문제에 유사유형 통합
			if (유사유형 && 원리공유문제) {
				const integrated = integrateSimilarTypes(유사유형, 원리공유문제);
				if (integrated !== 원리공유문제) {
					updateProps['원리공유문제'] = {
						rich_text: [
							{
								text: {
									content: integrated
								}
							}
						]
					};
					pageFixes.push('원리공유문제에 유사유형 통합');
				}
			}
			
			// 3. 개념 필드 수학적 논리 보완
			const 문제 = 핵심패턴 || LaTeX예시 || '';
			const 개념필드들 = [개념연결, 후행개념, 선행개념, 핵심개념].filter(h => h);
			
			if (문제 && 핵심개념) {
				const concepts = extractMathConcepts(문제, 중단원, 핵심개념);
				const suggestions = suggestSolutionEnhancement(문제, 핵심개념, 중단원, 개념필드들);
				
				// 개념연결이 비어있으면 핵심개념 기반 생성
				if (!개념연결 && 핵심개념) {
					const 개념연결Text = generateConceptConnection(핵심개념, concepts, 중단원);
					if (개념연결Text) {
						updateProps['개념연결'] = {
							rich_text: [
								{
									text: {
										content: 개념연결Text
									}
								}
							]
						};
						pageFixes.push('개념연결 생성');
					}
				}
				
				// 후행개념이 비어있으면 생성
				if (!후행개념 && 중단원) {
					const 후행개념Text = generate후행개념(중단원, concepts);
					if (후행개념Text) {
						updateProps['후행개념'] = {
							rich_text: [
								{
									text: {
										content: 후행개념Text
									}
								}
							]
						};
						pageFixes.push('후행개념 생성');
					}
				}
			}
			
			// 업데이트 실행
			if (Object.keys(updateProps).length > 0) {
				await rateLimiter.waitIfNeeded();
				await notion.pages.update({
					page_id: page.id,
					properties: updateProps
				});
				
				fixedCount++;
				fixReports.push({
					문제ID: 문제ID || page.id.substring(0, 8),
					fixes: pageFixes
				});
				
				console.log(`✅ ${문제ID || page.id.substring(0, 8)}... [${pageFixes.join(', ')}] 수정 완료`);
			}
			
			if ((i + 1) % 50 === 0) {
				console.log(`  ${i + 1}/${allPages.length} 페이지 처리 완료...`);
			}
		}
		
		// 결과 출력
		console.log('\n' + '='.repeat(80));
		console.log('[수정 결과 요약]');
		console.log('='.repeat(80));
		console.log(`총 페이지 수: ${allPages.length}개`);
		console.log(`수정된 페이지: ${fixedCount}개`);
		
		// 카테고리별 통계
		const fixCategories = {
			'대단원 통일': fixReports.filter(r => r.fixes.some(f => f.includes('대단원'))).length,
			'원리공유문제 통합': fixReports.filter(r => r.fixes.some(f => f.includes('원리공유문제'))).length,
			'개념연결 생성': fixReports.filter(r => r.fixes.some(f => f.includes('개념연결'))).length,
			'후행개념 생성': fixReports.filter(r => r.fixes.some(f => f.includes('후행개념'))).length
		};
		
		console.log('\n[카테고리별 수정 통계]');
		Object.entries(fixCategories).forEach(([category, count]) => {
			if (count > 0) {
				console.log(`${category}: ${count}개`);
			}
		});
		
		console.log('\n' + '='.repeat(80));
		console.log('✅ 수정 완료!');
		console.log('='.repeat(80));
		
	} catch (error) {
		console.error('\n❌ 수정 중 오류 발생:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
		console.error(error.stack);
	}
}

// 개념연결 생성 (수학적 논리 고려)
function generateConceptConnection(핵심개념, concepts, 중단원) {
	if (!핵심개념) return null;
	
	const connectionParts = [];
	
	// 핵심개념과 관련 개념들의 연결 설명
	const 핵심개념List = 핵심개념.split(/[,;]/).map(c => c.trim());
	
	for (const concept of 핵심개념List) {
		if (concept.includes('비율')) {
			connectionParts.push('비율 관계는 삼차함수의 변곡점 대칭성과 접선의 기울기 관계에서 유도됩니다.');
		}
		if (concept.includes('합성함수')) {
			connectionParts.push('합성함수는 함수의 대응 관계를 연속적으로 적용하는 것으로, 치환을 통해 단순화할 수 있습니다.');
		}
		if (concept.includes('미분가능')) {
			connectionParts.push('미분가능성은 연속성과 미분계수의 일치를 모두 만족해야 하며, 구간별 함수에서는 경계점에서 확인이 필요합니다.');
		}
		if (concept.includes('적분') || concept.includes('넓이')) {
			connectionParts.push('정적분은 미적분학의 기본정리를 통해 넓이와 연결되며, 구간을 나누어 계산할 수 있습니다.');
		}
		if (concept.includes('원순열')) {
			connectionParts.push('원순열은 순열에서 회전 대칭을 고려한 것으로, 하나를 고정하면 순열로 변환됩니다.');
		}
		if (concept.includes('이웃')) {
			connectionParts.push('이웃하지 않는 것의 계산은 여사건인 이웃하는 것을 이용하여 간단히 할 수 있습니다.');
		}
		if (concept.includes('부정방정식') || concept.includes('중복조합')) {
			connectionParts.push('부정방정식의 정수해는 중복조합으로 다룰 수 있으며, 새로운 미지수로 치환하여 음이 아닌 정수 조건으로 변환합니다.');
		}
		if (concept.includes('여사건')) {
			connectionParts.push('여사건은 드모르간의 법칙을 통해 집합 연산을 단순화하는 데 유용합니다.');
		}
	}
	
	return connectionParts.length > 0 ? connectionParts.join(' ') : null;
}

// 후행개념 생성 (수학적 논리 고려)
function generate후행개념(중단원, concepts) {
	if (!중단원) return null;
	
	const 후행Parts = [];
	
	// 중단원에 따른 후행개념
	if (중단원 === '미분') {
		후행Parts.push('적분, 최적화 문제, 곡선의 개형, 함수의 그래프');
	}
	if (중단원 === '적분') {
		후행Parts.push('넓이, 부피, 속도와 거리, 함수의 평균값');
	}
	if (중단원 === '함수의 극한과 연속') {
		후행Parts.push('미분, 연속함수의 성질, 중간값 정리');
	}
	if (중단원 === '경우의 수') {
		후행Parts.push('확률, 통계, 이항정리');
	}
	if (중단원 === '확률') {
		후행Parts.push('조건부 확률, 독립사건, 통계');
	}
	if (중단원 === '수열') {
		후행Parts.push('급수, 무한급수, 수학적 귀납법');
	}
	if (중단원 === '지수와 로그') {
		후행Parts.push('지수함수, 로그함수, 미적분');
	}
	if (중단원 === '삼각함수') {
		후행Parts.push('삼각함수의 미적분, 주기함수, 푸리에 급수');
	}
	
	return 후행Parts.length > 0 ? 후행Parts.join(', ') : null;
}

async function main() {
	try {
		await fixComprehensiveIssues();
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
