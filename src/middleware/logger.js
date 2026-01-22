// src/middleware/logger.js
// 로그 기록 미들웨어 - logs/access.log에 모든 과정 기록

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const LOG_DIR = path.join(__dirname, '../../logs');
const LOG_FILE = path.join(LOG_DIR, 'access.log');

/**
 * 로그 디렉토리 확인 및 생성
 */
async function ensureLogDirectory() {
	try {
		await fs.access(LOG_DIR);
	} catch {
		await fs.mkdir(LOG_DIR, { recursive: true });
	}
}

/**
 * 로그 메시지 포맷팅
 */
function formatLogMessage(level, category, message, metadata = {}) {
	const timestamp = new Date().toISOString();
	const metaStr = Object.keys(metadata).length > 0 
		? ` | ${JSON.stringify(metadata)}` 
		: '';
	return `[${timestamp}] [${level}] [${category}] ${message}${metaStr}\n`;
}

/**
 * 로그 레벨
 */
export const LogLevel = {
	INFO: 'INFO',
	WARN: 'WARN',
	ERROR: 'ERROR',
	DEBUG: 'DEBUG',
};

/**
 * 로거 클래스
 */
export class Logger {
	constructor(logFile = LOG_FILE) {
		this.logFile = logFile;
		this.initialized = false;
	}

	/**
	 * 초기화 (로그 디렉토리 생성)
	 */
	async init() {
		if (!this.initialized) {
			await ensureLogDirectory();
			this.initialized = true;
		}
	}

	/**
	 * 로그 파일에 기록
	 */
	async writeLog(level, category, message, metadata = {}) {
		await this.init();
		const logMessage = formatLogMessage(level, category, message, metadata);
		
		try {
			await fs.appendFile(this.logFile, logMessage, 'utf-8');
		} catch (error) {
			console.error('로그 파일 기록 실패:', error);
		}
	}

	/**
	 * INFO 레벨 로그
	 */
	async info(category, message, metadata = {}) {
		console.log(`[INFO] [${category}] ${message}`);
		await this.writeLog(LogLevel.INFO, category, message, metadata);
	}

	/**
	 * WARN 레벨 로그
	 */
	async warn(category, message, metadata = {}) {
		console.warn(`[WARN] [${category}] ${message}`);
		await this.writeLog(LogLevel.WARN, category, message, metadata);
	}

	/**
	 * ERROR 레벨 로그
	 */
	async error(category, message, metadata = {}) {
		console.error(`[ERROR] [${category}] ${message}`);
		await this.writeLog(LogLevel.ERROR, category, message, metadata);
	}

	/**
	 * DEBUG 레벨 로그
	 */
	async debug(category, message, metadata = {}) {
		console.debug(`[DEBUG] [${category}] ${message}`);
		await this.writeLog(LogLevel.DEBUG, category, message, metadata);
	}

	/**
	 * 캐시 관련 로그
	 */
	async cache(action, key, metadata = {}) {
		await this.info('CACHE', `${action}: ${key}`, metadata);
	}

	/**
	 * Thinking 로직 관련 로그
	 */
	async thinking(action, studentLevel, stage, metadata = {}) {
		await this.info('THINKING', `${action} | 학생 레벨: ${studentLevel} | Stage: ${stage}`, metadata);
	}

	/**
	 * API 호출 관련 로그 (비용 0원 로직에서 중요)
	 */
	async api(action, endpoint, metadata = {}) {
		await this.info('API', `${action} | ${endpoint}`, metadata);
	}
}

// 싱글톤 인스턴스
const logger = new Logger();

// 기본 export
export default logger;
