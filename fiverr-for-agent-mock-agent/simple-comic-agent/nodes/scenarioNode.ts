// nodes/scenarioNode.ts
import { ChatOpenAI } from "@langchain/openai";

import { ComicGraphState, ScenarioSchema, ComicScenario } from "../types";

const llm = new ChatOpenAI({
  modelName: "gpt-4o-mini", // 네가 말한 그대로
  temperature: 0.9, // 살짝 창의적으로
});

export async function scenarioNode(
  state: ComicGraphState
): Promise<ComicGraphState> {
  const preferredPanels = 4;
  const defaultTone = "가벼운 회사/일상 코미디";

  const structured = llm.withStructuredOutput(ScenarioSchema);

  const system = `
너는 어떤 형식의 입력이든 받아서
'한 장짜리 만화 페이지'로 만들 수 있는 시나리오를 만드는 작가다.

출력은 아래 스키마를 따르는 JSON이다:

{
  "summary": string,
  "beats": string[],
  "panelCount": number,
  "tone": string,
  "styleHint": string
}
`;

  const user = `
사용자 요청(prompt):
"${state.prompt}"

요구사항:
- 대략 ${preferredPanels}컷 안에 들어갈 정도의 시나리오로 구성해라.
- 특별한 언급이 없으면 톤은 "${defaultTone}"를 사용하되,
  prompt에서 명시적인 톤(진지하게, 감동적으로 등)이 보이면 그쪽을 우선해라.
- beats 배열의 길이는 panelCount와 비슷하게 맞춰라.
`;

  const scenario = (await structured.invoke([
    { role: "system", content: system },
    { role: "user", content: user },
  ])) as ComicScenario;

  return {
    ...state,
    scenario,
  };
}
