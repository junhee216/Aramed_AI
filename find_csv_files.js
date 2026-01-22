// find_csv_files.js
// 다운로드 폴더에서 CSV 파일 찾기

import fs from 'fs';
import path from 'path';

const downloadsPath = path.join(process.env.USERPROFILE || process.env.HOME, 'Downloads');

console.log('='.repeat(70));
console.log('[다운로드 폴더 CSV 파일 검색]');
console.log('='.repeat(70));
console.log(`검색 경로: ${downloadsPath}\n`);

if (!fs.existsSync(downloadsPath)) {
	console.log('❌ 다운로드 폴더를 찾을 수 없습니다.');
	process.exit(1);
}

const files = fs.readdirSync(downloadsPath);
const csvFiles = files.filter(f => f.endsWith('.csv'));

console.log(`총 ${csvFiles.length}개 CSV 파일 발견\n`);

// P3 관련 파일
const p3Files = csvFiles.filter(f => f.includes('P3'));
console.log(`[P3 포함 파일] ${p3Files.length}개:`);
p3Files.forEach(f => console.log(`  - ${f}`));

// 미적분 관련 파일
const calcFiles = csvFiles.filter(f => f.includes('미적분'));
console.log(`\n[미적분 포함 파일] ${calcFiles.length}개:`);
calcFiles.forEach(f => console.log(`  - ${f}`));

// 2025 관련 파일
const year2025Files = csvFiles.filter(f => f.includes('2025'));
console.log(`\n[2025 포함 파일] ${year2025Files.length}개:`);
year2025Files.forEach(f => console.log(`  - ${f}`));

// 미적분 + P3 조합
const calcP3Files = csvFiles.filter(f => f.includes('미적분') && f.includes('P3'));
console.log(`\n[미적분 + P3 포함 파일] ${calcP3Files.length}개:`);
calcP3Files.forEach(f => console.log(`  - ${f}`));
