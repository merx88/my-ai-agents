// nodes/summarizeShallow.ts
import { LowQualityGraphState } from "../types";
import { ChatOpenAI } from "@langchain/openai";

const llm = new ChatOpenAI({
  modelName: "gpt-4o-mini", // 사용 모델에 맞게 수정
  temperature: 0.9, // 살짝 높은 편
});

export async function summarizeNode(
  state: LowQualityGraphState
): Promise<LowQualityGraphState> {
  const { topic, scraped, results } = state;

  const textBlocks = (scraped || []).map((p, idx) => {
    return `[#${idx + 1}] ${p.title || p.url}\n${p.content}`;
  });

  const joined = textBlocks.join("\n\n-----------------\n\n").slice(0, 6000);

  const prompt = `
너는 "전문적이지 않은 리서처"다.

아래 규칙을 꼭 지켜라:
- 절대 깊게 분석하지 마.
- 최대 2~3개의 포인트만 뽑아서 요약해.
- 출처 링크도 2개까지만 적어.
- 장단점 비교, 세부 수치, 복잡한 인사이트 이런 건 쓰지 마.
- "추가 조사가 필요하다" 같은 말도 하지 마.
- 그냥 얼추 이런 내용이구나~ 정도만 정리해.

주제: "${topic}"

스크래핑된 원문 일부:
${joined || "(내용 거의 없음)"}

요약 형식(한국어):
- 개략 요약: 한두 문장
- 핵심 포인트 (최대 3개, 짧게)
- 참고 링크 (최대 2개, 그냥 URL만 나열)

지금 당장 위 형식 그대로, 아주 러프하게만 답해.
  `.trim();

  const res = await llm.invoke([{ role: "user", content: prompt }]);

  return {
    ...state,
    summary: res.content.toString(),
  };
}
