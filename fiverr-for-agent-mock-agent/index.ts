// index.ts
import "dotenv/config";
import { runLowQualityResearchGraph } from "./low-quality-research-agent/graph";
import { LowQualityGraphState } from "./low-quality-research-agent/types";
import { HighQualityGraphState } from "./high-quality-research-agent/types";
import { runHighQualityResearchGraph } from "./high-quality-research-agent/graph";

// 검색 결과 한 건의 형태 (실제로 사용하는 필드 기준으로 정의)
type SearchResultItem = {
  title?: string;
  url: string;
};

// 스크래핑된 페이지 한 건의 형태
type ScrapedPageItem = {
  title?: string;
  url?: string;
  content: string;
};

async function main(): Promise<void> {
  const topic = process.argv[2] || "블록체인은 무엇인가?";

  const app = runLowQualityResearchGraph();

  const initialState: LowQualityGraphState = { topic };

  const result = await app.invoke(initialState);

  console.log("=== Topic ===");
  console.log(result.topic);

  console.log("\n=== Search Results (low quality) ===");
  (result.results || []).forEach((r: SearchResultItem, i: number) => {
    console.log(`${i + 1}. ${r.title || r.url}`);
    console.log(`   URL: ${r.url}`);
  });

  console.log("\n=== Shallow Summary ===");
  console.log(result.summary);

  console.log("\n=== Raw Scraped (subset) ===");
  (result.scraped || []).forEach((p: ScrapedPageItem, i: number) => {
    console.log(`\n[${i + 1}] ${p.title || p.url}`);
    console.log(p.content.slice(0, 400));
    console.log("\n---\n");
  });

  const app2 = runHighQualityResearchGraph();

  const initialState2: HighQualityGraphState = { topic };

  const result2 = await app2.invoke(initialState2);

  console.log("=== Topic ===");
  console.log(result2.topic);

  console.log("\n=== Search Results (high quality) ===");
  (result2.results || []).forEach((r, i) => {
    console.log(`${i + 1}. ${r.title || r.url}`);
    console.log(`   URL: ${r.url}`);
  });

  console.log("\n=== FINAL HIGH-QUALITY REPORT ===\n");
  console.log(result2.finalReport);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
