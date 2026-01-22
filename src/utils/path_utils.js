// path_utils.js
// 크로스 플랫폼 경로 유틸리티

import path from 'path';
import os from 'os';

/**
 * MathPDF organized 디렉토리 경로 가져오기
 * 환경 변수 MATHPDF_PATH가 설정되어 있으면 사용, 없으면 기본 경로 사용
 */
export function getMathPdfPath() {
	const envPath = process.env.MATHPDF_PATH;
	if (envPath) {
		return envPath;
	}
	
	// OS별 기본 경로
	const platform = os.platform();
	const homeDir = os.homedir();
	
	if (platform === 'win32') {
		return path.join(homeDir, 'Documents', 'MathPDF', 'organized');
	} else {
		// Linux, macOS
		return path.join(homeDir, 'Documents', 'MathPDF', 'organized');
	}
}

/**
 * 기하 문제 파일 경로 가져오기
 */
export function getGeometryProblemPath(part) {
	const basePath = getMathPdfPath();
	return path.join(
		basePath,
		'현우진',
		'기하_2024학년도_현우진_드릴',
		`기하_2024학년도_현우진_드릴_${part}_문제_deepseek.json`
	);
}

/**
 * 기하 해설 파일 경로 가져오기
 */
export function getGeometrySolutionPath(part) {
	const basePath = getMathPdfPath();
	return path.join(
		basePath,
		'현우진',
		'기하_2024학년도_현우진_드릴',
		`기하_2024학년도_현우진_드릴_${part}_해설_deepseek_r1.md`
	);
}
