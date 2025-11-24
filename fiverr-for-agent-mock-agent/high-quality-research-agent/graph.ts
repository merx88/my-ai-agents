// graphHigh.ts
import { StateGraph, END } from "@langchain/langgraph";
import { z } from "zod";

import { HighQualityGraphState } from "./types";
import { searchNode } from "./nodes/searchNode";
import { scrapeNode } from "./nodes/scrapeNode";
import { summarizeNode } from "./nodes/summarizeNode";
import { reportNode } from "./nodes/reportNode";

const HighQualityGraphState = z.object({
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
  pageSummaries: z
    .array(
      z.object({
        url: z.string(),
        title: z.string().optional(),
        summary: z.string(),
      })
    )
    .optional(),
  finalReport: z.string().optional(),
});

export function runHighQualityResearchGraph() {
  const graph = new StateGraph(HighQualityGraphState)
    .addNode("search_high", searchNode)
    .addNode("scrape_high", scrapeNode)
    .addNode("summarize_pages", summarizeNode)
    .addNode("synthesize_report", reportNode)
    .addEdge("search_high", "scrape_high")
    .addEdge("scrape_high", "summarize_pages")
    .addEdge("summarize_pages", "synthesize_report")
    .addEdge("synthesize_report", END)
    .setEntryPoint("search_high");

  return graph.compile();
}
