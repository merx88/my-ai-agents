import { ChatOpenAI } from "@langchain/openai";

import { ComicGraphState, ComicPage, ComicPageSchema } from "../types";

const llm = new ChatOpenAI({
  modelName: "gpt-4o-mini", // 네가 말한 그대로
  temperature: 0.9, // 살짝 창의적으로
});

export async function cartoonNode(
  state: ComicGraphState
): Promise<ComicGraphState> {
  if (!state.scenario) {
    console.warn("[COMIC] cartoonNode: scenario is missing, skipping.");
    return state;
  }

  const scenario = state.scenario;

  const structured = llm.withStructuredOutput(ComicPageSchema);

  const system = `
너는 한 장짜리 만화 페이지를 설계하는 만화가다.

해야 할 일:
1. scenario.beats를 기반으로 각 컷에 대해:
   - 장면 설명(description)
   - 캐릭터 대사(dialogues)를 만든다.
2. 전체 페이지를 "한 장짜리 만화 이미지"로 만들 수 있도록
   pageImagePrompt를 작성한다.
   - 한 장 안에 여러 패널이 나뉘어 있는 구성이어야 한다.
   - 각 패널이 대략 어떤 장면인지 요약해서 포함한다.
   - 말풍선 텍스트는 한국어라는 점을 명시한다.

출력 스키마:

{
  "layout": {
    "panelCount": number,
    "layoutType": "4cut-horizontal" | "2x2-grid" | "vertical-webtoon" | "custom",
    "description": string
  },
  "panels": [
    {
      "index": number,
      "beat": string,
      "description": string,
      "dialogues": [
        { "speaker": string, "text": string }
      ]
    }
  ],
  "pageImagePrompt": string
}
`;

  const user = `
Scenario:
${JSON.stringify(scenario, null, 2)}

요구사항:
- layout.panelCount는 scenario.panelCount를 기본으로 사용해라.
- 특별한 언급이 없으면 현대 한국 회사/일상 웹툰 스타일을 기본으로 한다.
- pageImagePrompt는 영어로 작성해도 되지만,
  "a single comic page with multiple panels" 같은 문구로
  한 장 안에 컷이 분할되어 있다는 점을 분명히 표현해라.
- 말풍선 안의 텍스트는 한국어로 되어 있음을 분명히 언급해라.
`;

  const page = (await structured.invoke([
    { role: "system", content: system },
    { role: "user", content: user },
  ])) as ComicPage;

  return {
    ...state,
    page,
  };
}
