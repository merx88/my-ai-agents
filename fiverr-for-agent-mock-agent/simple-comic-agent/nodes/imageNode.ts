// nodes/imageNode.ts
import { ComicGraphState } from "../types";
import generateImage from "../../lib/generateImage";

export async function imageNode(
  state: ComicGraphState
): Promise<ComicGraphState> {
  if (!state.page) {
    console.warn(
      "[COMIC] imageNode: page is missing, skipping image generation."
    );
    return state;
  }

  const prompt = state.page.pageImagePrompt;

  try {
    const buffer = await generateImage(prompt);

    // state에는 base64 string으로 저장 (클라이언트에서 <img src=...> 로 쓰기 좋게)
    const imageBase64 = buffer.toString("base64");

    return {
      ...state,
      imageBase64,
    };
  } catch (e) {
    console.error("[COMIC] imageNode: image generation failed", e);
    // 실패해도 그래프는 죽지 않게 그냥 state만 반환
    return state;
  }
}
