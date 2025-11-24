// nodes/searchHigh.ts
import axios from "axios";
import { HighQualityGraphState, SearchResult } from "../types";

const TAVILY_ENDPOINT = "https://api.tavily.com/search";

export async function searchNode(
  state: HighQualityGraphState
): Promise<HighQualityGraphState> {
  const { topic } = state;

  const apiKey = process.env.TAVILY_API_KEY;
  if (!apiKey) throw new Error("TAVILY_API_KEY is not set");

  const res = await axios.post(
    TAVILY_ENDPOINT,
    {
      query: topic,
      search_depth: "advanced", // 더 깊게
      include_answer: true,
      include_images: false,
      max_results: 3, // 결과 많이
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
