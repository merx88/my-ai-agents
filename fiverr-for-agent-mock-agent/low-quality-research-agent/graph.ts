// graph.ts
import { StateGraph, END, START } from "@langchain/langgraph";
import { z } from "zod";

import { LowQualityGraphState } from "./types";
import { searchNode } from "./nodes/searchNode";
import { scrapeNode } from "./nodes/scrapeNode";
import { summarizeNode } from "./nodes/summarizeNode";

const LowQualityGraphState = z.object({
  topic: z.string(),
  results: z
    .array(
      z.object({
        url: z.string(),
        title: z.string().optional(),
        snippet: z.string().optional(),
      })
    )
    .optional(),
  scraped: z
    .array(
      z.object({
        url: z.string(),
        title: z.string().optional(),
        content: z.string(),
      })
    )
    .optional(),
  summary: z.string().optional(),
});

export function runLowQualityResearchGraph() {
  const graph = new StateGraph(LowQualityGraphState)
    .addNode("searchNode", searchNode)
    .addNode("scrapeNode", scrapeNode)
    .addNode("summarizeNode", summarizeNode)
    .addEdge(START, "searchNode")
    .addEdge("searchNode", "scrapeNode")
    .addEdge("scrapeNode", "summarizeNode")
    .addEdge("summarizeNode", END);

  return graph.compile();
}
