// nodes/searchLow.ts
import axios from "axios";
import { LowQualityGraphState, SearchResult } from "../types";

const TAVILY_ENDPOINT = "https://api.tavily.com/search";

export async function searchNode(
  state: LowQualityGraphState
): Promise<LowQualityGraphState> {
  const { topic } = state;

  const apiKey = process.env.TAVILY_API_KEY;
  if (!apiKey) throw new Error("TAVILY_API_KEY is not set");

  const res = await axios.post(
    TAVILY_ENDPOINT,
    {
      query: topic,
      search_depth: "basic", // 얕게
      include_answer: false,
      include_images: false,
      max_results: 2, // 소수만
    },
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
    }
  );

  const data = res.data;
  const results: SearchResult[] = (data.results || []).map((r: any) => ({
    url: r.url,
    title: r.title,
    snippet: r.content || r.snippet,
  }));

  return {
    ...state,
    results,
  };
}
