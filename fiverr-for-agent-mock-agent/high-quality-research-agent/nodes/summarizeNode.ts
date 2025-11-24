// nodes/summarizePages.ts
import { HighQualityGraphState, PageSummary } from "../types";
import { ChatOpenAI } from "@langchain/openai";

const llm = new ChatOpenAI({
  modelName: "gpt-4o-mini",
  temperature: 0.3,
});

export async function summarizeNode(
  state: HighQualityGraphState
): Promise<HighQualityGraphState> {
  const { topic, scraped } = state;
  if (!scraped || scraped.length === 0) return state;

  const summaries: PageSummary[] = [];

  await Promise.all(
    scraped.map(async (page) => {
      const content = page.content.slice(0, 8000); // context 보호용 자르기

      const prompt = `
다음 문서는 "${topic}"와 관련된 자료 중 하나다.
이 문서의 핵심 내용을 요약해라.

요약 규칙:
- 문서의 주장/핵심 아이디어를 3~5개의 bullet로 정리
- 중요한 수치/사례는 가능한 한 포함
- 문서의 관점(찬성/반대/중립 등)을 명확히
- 사실과 의견을 구분해서 표현하려고 노력

문서 제목: ${page.title || "(제목 없음)"}
URL: ${page.url}

문서 내용:
${content}
      `.trim();

      const res = await llm.invoke([{ role: "user", content: prompt }]);

      summaries.push({
        url: page.url,
        title: page.title,
        summary: res.content.toString(),
      });
    })
  );

  return {
    ...state,
    pageSummaries: summaries,
  };
}
