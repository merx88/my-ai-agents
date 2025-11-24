// types.ts
import { z } from "zod";

/** ---- Scenario ---- */

export const ScenarioSchema = z.object({
  summary: z.string(),
  beats: z.array(z.string()),
  panelCount: z.number(),
  tone: z.string(),
  styleHint: z.string(),
});

export type ComicScenario = z.infer<typeof ScenarioSchema>;

/** ---- Panel / ComicPage ---- */

export const ComicPanelSchema = z.object({
  index: z.number(),
  beat: z.string(),
  description: z.string(),
  dialogues: z.array(
    z.object({
      speaker: z.string(),
      text: z.string(),
    })
  ),
});

export type ComicPanel = z.infer<typeof ComicPanelSchema>;

export const ComicPageSchema = z.object({
  layout: z.object({
    panelCount: z.number(),
    layoutType: z.enum([
      "4cut-horizontal",
      "2x2-grid",
      "vertical-webtoon",
      "custom",
    ]),
    description: z.string(),
  }),
  panels: z.array(ComicPanelSchema),
  pageImagePrompt: z.string(),
});

export type ComicPage = z.infer<typeof ComicPageSchema>;

/** ---- Graph State ---- */

export const ComicGraphStateSchema = z.object({
  // 인풋: 유저가 넣는 쿼리 한 줄
  prompt: z.string(),

  // 시나리오 노드 출력
  scenario: ScenarioSchema.optional(),

  // 만화가 노드 출력
  page: ComicPageSchema.optional(),

  imageBase64: z.string().optional(),
});

export type ComicGraphState = z.infer<typeof ComicGraphStateSchema>;
