// src/utils/notion_utils.js
// Notion API 관련 공통 유틸리티 함수들

/**
 * Notion 속성 값 추출
 * @param {Object} prop - Notion 속성 객체
 * @returns {string|number|Array|null} 추출된 값
 */
export function extractPropertyValue(prop) {
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
		case 'relation':
			return prop.relation.map(r => r.id);
		case 'formula':
			return prop.formula;
		default:
			return null;
	}
}

/**
 * Notion 페이지에서 문제 데이터 구조화
 * @param {Object} page - Notion 페이지 객체
 * @param {Array<string>} fieldNames - 추출할 필드 이름 배열
 * @returns {Object} 구조화된 문제 데이터
 */
export function extractProblemData(page, fieldNames = []) {
	const props = page.properties;
	const data = {
		id: page.id,
		문제ID: extractPropertyValue(props['문제ID']),
	};
	
	// 기본 필드들
	const defaultFields = [
		'question', 'topic', '핵심개념', '함정설계', '실수포인트', 
		'중단원', '대단원', '원리공유문제', '오답시나리오',
		'LaTeX예시', '핵심패턴', '개념연결', '후행개념'
	];
	
	const allFields = [...new Set([...defaultFields, ...fieldNames])];
	
	allFields.forEach(field => {
		const prop = props[field];
		if (prop) {
			data[field] = extractPropertyValue(prop);
		}
	});
	
	// question 필드가 없으면 LaTeX예시 또는 핵심패턴 사용
	if (!data.question) {
		data.question = data.LaTeX예시 || data.핵심패턴 || '';
	}
	
	// topic 필드가 없으면 중단원 또는 대단원 사용
	if (!data.topic) {
		data.topic = data.중단원 || data.대단원 || '';
	}
	
	return data;
}

/**
 * Notion rich_text 속성 생성
 * @param {string} content - 텍스트 내용
 * @returns {Object} Notion rich_text 속성 객체
 */
export function createRichTextProperty(content) {
	if (!content) {
		return {
			rich_text: []
		};
	}
	
	return {
		rich_text: [
			{
				text: {
					content: String(content)
				}
			}
		]
	};
}

/**
 * Notion 필터 생성 헬퍼
 * @param {Object} options - 필터 옵션
 * @returns {Object} Notion 필터 객체
 */
export function createNotionFilter(options = {}) {
	const { property, contains, equals, isEmpty, isNotEmpty } = options;
	
	if (!property) {
		return {};
	}
	
	if (contains !== undefined) {
		return {
			property,
			title: { contains }
		};
	}
	
	if (equals !== undefined) {
		return {
			property,
			title: { equals }
		};
	}
	
	if (isEmpty) {
		return {
			property,
			title: { is_empty: true }
		};
	}
	
	if (isNotEmpty) {
		return {
			property,
			title: { is_not_empty: true }
		};
	}
	
	return {};
}

/**
 * 여러 문제 ID 패턴으로 필터 생성
 * @param {Array<string>} patterns - 문제 ID 패턴 배열 (예: ['수1_2025', '수2_2025'])
 * @returns {Object} Notion OR 필터 객체
 */
export function createProblemIdFilter(patterns) {
	if (!patterns || patterns.length === 0) {
		return {};
	}
	
	return {
		or: patterns.map(pattern => ({
			property: '문제ID',
			title: { contains: pattern }
		}))
	};
}
