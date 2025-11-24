// nodes/synthesizeReport.ts
import { HighQualityGraphState } from "../types";
import { ChatOpenAI } from "@langchain/openai";

const synthLlm = new ChatOpenAI({
  modelName: "gpt-4o", // 메인 모델
  temperature: 0.4,
});

export async function reportNode(
  state: HighQualityGraphState
): Promise<HighQualityGraphState> {
  const { topic, pageSummaries } = state;

  const blocks = (pageSummaries || []).map((p, i) => {
    return `
[소스 #${i + 1}]
제목: ${p.title || "(제목 없음)"}
URL: ${p.url}

요약:
${p.summary}
`;
  });

  const joined = blocks
    .join("\n\n============================\n\n")
    .slice(0, 12000);

  const prompt = `
너는 신중한 리서처다. 아래는 "${topic}"에 대해 여러 웹페이지를 정리한 요약들이다.
이 요약들을 바탕으로 **깊이 있는 종합 리포트**를 작성해라.

규칙:
1. 서로 다른 소스의 정보를 비교·대조하라.
2. 합의되는 부분과, 소스 간에 의견/데이터가 갈리는 부분을 구분해서 적어라.
3. 가능한 경우, 구체적인 수치나 사례를 포함하라.
4. 불확실한 부분은 "불확실", "추가 검증 필요"라고 명시해라.
5. 마지막에 "한계 및 추가로 보면 좋은 키워드" 섹션을 넣어라.
6. 필요한 경우에만, 소스 번호(#1, #2...)를 괄호 안에 붙여서 참고표시로 사용해도 된다.

아웃풋 형식(한국어):

# 1. 주제 개요
- 2~3문장으로 큰 그림 설명

# 2. 핵심 쟁점 및 내용
- 소주제 2~4개 정도로 나누어 정리
- 각 소주제마다:
  - 개념/배경
  - 주요 주장/데이터
  - 소스 간 차이점이 있으면 비교

# 3. 실제 활용/적용 관점 (있으면)
- 실무/현업에서 이 정보를 어떻게 쓸 수 있는지
- 주의해야 할 포인트

# 4. 한계 및 추가로 보면 좋은 키워드
- 이 리서치의 한계
- 추후 더 찾아볼 만한 키워드 3~5개

아래가 참고용 요약 목록이다:

${joined || "(소스 요약이 거의 없음)"}
  `.trim();

  const res = await synthLlm.invoke([{ role: "user", content: prompt }]);

  return {
    ...state,
    finalReport: res.content.toString(),
  };
}
