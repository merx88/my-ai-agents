// nodes/scrapeHigh.ts
import { FireCrawlLoader } from "@langchain/community/document_loaders/web/firecrawl";
import { HighQualityGraphState, ScrapedPage } from "../types";

const BLOCKED_DOMAINS = [
  "x.com",
  "twitter.com",
  "www.youtube.com",
  "youtube.com",
  "youtu.be",
];

function isBlocked(url: string): boolean {
  try {
    const u = new URL(url);
    return BLOCKED_DOMAINS.includes(u.hostname);
  } catch {
    return false;
  }
}

export async function scrapeNode(
  state: HighQualityGraphState
): Promise<HighQualityGraphState> {
  const apiKey = process.env.FIRECRAWL_API_KEY;
  if (!apiKey) throw new Error("FIRECRAWL_API_KEY is not set");

  if (!state.results || state.results.length === 0) return state;

  // 상위 6~8개 정도 깊게 스캔 (이전 코드랑 비슷하게 8개로)
  const targets = state.results.slice(0, 8);
  const scraped: ScrapedPage[] = [];

  for (const r of targets) {
    if (isBlocked(r.url)) {
      console.warn("[HIGH] skipped unsupported domain:", r.url);
      continue;
    }

    try {
      const loader = new FireCrawlLoader({
        url: r.url,
        apiKey,
        mode: "crawl",
        params: {
          // Firecrawl v0 스타일 params -> FirecrawlApp.crawlUrl 로 그대로 전달됨
          pageOptions: {
            // 메인 콘텐츠 위주로만
            onlyMainContent: true,
            // 필요하다면 HTML까지 포함
            // includeHtml: true,
          },
          crawlerOptions: {
            // depth: 2 였던 의도 반영
            maxDepth: 2,
            // 너무 많이 안 긁도록 상한
            limit: 50,
          },
        },
      });

      const docs = await loader.load();
      if (!docs || docs.length === 0) {
        console.warn("[HIGH] crawl returned empty docs:", r.url);
        continue;
      }

      // 여러 페이지를 한 덩어리로 합쳐 고품질 컨텍스트 생성
      const mergedContent = docs
        .map((d) => {
          const meta = (d.metadata ?? {}) as any;
          const title = meta.title ?? meta.ogTitle ?? "";
          const header = title ? `# ${title}\n\n` : "";
          return `${header}${d.pageContent}`;
        })
        .join("\n\n---\n\n");

      const firstMeta = (docs[0].metadata ?? {}) as any;

      scraped.push({
        url: r.url,
        title: firstMeta.title ?? firstMeta.ogTitle ?? r.title ?? r.url,
        // high-quality니까 길이 제한 없이 그대로 저장
        content: mergedContent,
      });
    } catch (e) {
      console.error("[HIGH] scrape failed:", r.url, e);
    }
  }

  return {
    ...state,
    scraped,
  };
}
