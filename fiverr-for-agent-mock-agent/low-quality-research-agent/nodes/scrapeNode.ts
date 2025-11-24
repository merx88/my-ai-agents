// nodes/scrapeNode.ts
import { FireCrawlLoader } from "@langchain/community/document_loaders/web/firecrawl";
import { LowQualityGraphState, ScrapedPage } from "../types";

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
  state: LowQualityGraphState
): Promise<LowQualityGraphState> {
  const apiKey = process.env.FIRECRAWL_API_KEY;
  if (!apiKey) throw new Error("FIRECRAWL_API_KEY is not set");

  if (!state.results || state.results.length === 0) return state;

  const targets = state.results.slice(0, 2);
  const scraped: ScrapedPage[] = [];

  for (const r of targets) {
    if (isBlocked(r.url)) {
      console.warn("[LOW] skipped unsupported domain:", r.url);
      continue;
    }

    try {
      const loader = new FireCrawlLoader({
        url: r.url,
        apiKey,
        mode: "scrape",
      });

      const docs = await loader.load();
      if (!docs || docs.length === 0) {
        console.warn("[LOW] scrape returned empty docs:", r.url);
        continue;
      }

      const doc = docs[0];
      const meta = (doc.metadata ?? {}) as any;

      scraped.push({
        url: r.url,
        title: meta.title ?? r.title ?? r.url,
        content: doc.pageContent.slice(0, 1500),
      });
    } catch (e) {
      console.error("[LOW] scrape failed:", r.url, e);
    }
  }

  return {
    ...state,
    scraped,
  };
}
