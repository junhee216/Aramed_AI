/**
 * 간단한 개발 서버
 * 환경변수에서 Notion API 설정을 읽어서 클라이언트에 제공합니다.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// .env 파일에서 환경변수 로드
require('dotenv').config();

const PORT = process.env.PORT || 8000;

// MIME 타입 매핑
const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.wav': 'audio/wav',
    '.mp4': 'video/mp4',
    '.woff': 'application/font-woff',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
    '.wasm': 'application/wasm'
};

const server = http.createServer((req, res) => {
    console.log(`${req.method} ${req.url}`);

    const parsedUrl = url.parse(req.url);
    let pathname = parsedUrl.pathname;

    // 루트 경로는 index.html로
    if (pathname === '/') {
        pathname = '/index.html';
    }

    // /api/config 엔드포인트: 환경변수에서 설정 제공
    if (pathname === '/api/config') {
        const config = {
            apiKey: process.env.NOTION_API_KEY || '',
            pageId: process.env.NOTION_PAGE_ID || ''
        };

        res.writeHead(200, {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        });
        res.end(JSON.stringify(config));
        return;
    }

    // 정적 파일 제공
    const filePath = path.join(__dirname, pathname);
    
    // 보안: 상위 디렉토리 접근 방지
    if (!filePath.startsWith(__dirname)) {
        res.writeHead(403);
        res.end('Forbidden');
        return;
    }

    const ext = path.parse(filePath).ext;
    const contentType = mimeTypes[ext] || 'application/octet-stream';

    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                res.writeHead(404);
                res.end('File not found');
            } else {
                res.writeHead(500);
                res.end(`Server Error: ${err.code}`);
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(PORT, () => {
    console.log(`\n서버가 실행 중입니다!`);
    console.log(`📍 http://localhost:${PORT}`);
    console.log(`\n환경변수 확인:`);
    console.log(`  NOTION_API_KEY: ${process.env.NOTION_API_KEY ? '✅ 설정됨' : '❌ 미설정'}`);
    console.log(`  NOTION_PAGE_ID: ${process.env.NOTION_PAGE_ID || '❌ 미설정'}`);
    console.log(`\n.env 파일을 확인하고 필요시 수정하세요.\n`);
});
