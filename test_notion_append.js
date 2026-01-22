/**
 * test_notion_append.js
 * - .env에서 NOTION_API_KEY, NOTION_PAGE_ID 읽음
 * - Notion 페이지(또는 블록)에 Heading / Bullet / Toggle 구조로 append 테스트
 */

import dotenv from "dotenv";
dotenv.config(); // 같은 폴더의 .env 자동 로드

import { Client } from "@notionhq/client";

// 1) ENV 체크
const NOTION_API_KEY = (process.env.NOTION_API_KEY || "").trim();
const NOTION_PAGE_ID = (process.env.NOTION_PAGE_ID || "").trim();

if (!NOTION_API_KEY || !NOTION_PAGE_ID) {
  console.error("❌ .env에 NOTION_API_KEY 또는 NOTION_PAGE_ID가 없습니다.");
  console.error("   예) NOTION_API_KEY=ntn_...");
  console.error("       NOTION_PAGE_ID=32자리페이지ID");
  process.exit(1);
}

// (선택) 페이지 ID에 하이픈이 섞여 있으면 제거해도 동작합니다.
const parentBlockId = NOTION_PAGE_ID.replaceAll("-", "");

console.log("✅ ENV LOADED:", {
  keyPrefix: NOTION_API_KEY.slice(0, 8) + "...",
  pageId: parentBlockId,
});

// 2) Notion Client
const notion = new Client({ auth: NOTION_API_KEY });

// 3) Notion block children append payload (구조화 예시)
function buildBlocks() {
  const now = new Date();
  const stamp = now.toLocaleString("ko-KR");

  return [
    // Heading
    {
      object: "block",
      type: "heading_2",
      heading_2: {
        rich_text: [{ type: "text", text: { content: `✅ API Append Test (${stamp})` } }],
      },
    },

    // Callout
    {
      object: "block",
      type: "callout",
      callout: {
        icon: { type: "emoji", emoji: "🧭" },
        rich_text: [
          { type: "text", text: { content: "이 블록들은 Node.js + Notion API로 자동 추가된 테스트입니다." } },
        ],
      },
    },

    // Bullets
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: "Heading / Bullet / Toggle 구조 테스트" } }],
      },
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: ".env → Client(auth) → blocks.children.append 흐름 확인" } }],
      },
    },

    // Toggle + children
    {
      object: "block",
      type: "toggle",
      toggle: {
        rich_text: [{ type: "text", text: { content: "📌 (Toggle) 세부 로그 / 메모" } }],
        children: [
          {
            object: "block",
            type: "paragraph",
            paragraph: {
              rich_text: [
                { type: "text", text: { content: "여기는 토글 안에 들어가는 내용입니다. 운영 시에는 참고자료/원문 링크 등을 넣습니다." } },
              ],
            },
          },
          {
            object: "block",
            type: "numbered_list_item",
            numbered_list_item: {
              rich_text: [{ type: "text", text: { content: "1) 케이스 요약" } }],
            },
          },
          {
            object: "block",
            type: "numbered_list_item",
            numbered_list_item: {
              rich_text: [{ type: "text", text: { content: "2) 리스크/주의사항" } }],
            },
          },
        ],
      },
    },

    // Divider
    { object: "block", type: "divider", divider: {} },
  ];
}

// 4) 실행
async function main() {
  try {
    const children = buildBlocks();

    const res = await notion.blocks.children.append({
      block_id: parentBlockId, // 페이지 ID도 block_id로 넣으면 됨
      children,
    });

    const appendedId = res?.results?.[0]?.id || "(no id)";
    console.log("🎉 APPEND OK. first_block_id:", appendedId);
  } catch (e) {
    // Notion SDK 에러는 보통 e.body에 자세히 있음
    console.error("❌ APPEND FAILED:", e?.body ?? e);
    process.exit(1);
  }
}

main();

