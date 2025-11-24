import "dotenv/config";
import express from "express";
import cors from "cors";

import { runLowQualityResearchGraph } from "../low-quality-research-agent/graph";
import { runHighQualityResearchGraph } from "../high-quality-research-agent/graph";
import { LowQualityGraphState } from "../low-quality-research-agent/types";
import { HighQualityGraphState } from "../high-quality-research-agent/types";

const app = express();
const port = process.env.PORT || 3000;

// 그래프 미리 컴파일
const lowAgent = runLowQualityResearchGraph();
const highAgent = runHighQualityResearchGraph();

app.use(cors());
app.use(express.json());

app.get("/", (_req, res) => {
  res.json({
    ok: true,
    message: "Research agent API",
    endpoints: {
      low: "POST /research/low",
      high: "POST /research/high",
    },
  });
});

app.post("/research/low", async (req, res) => {
  try {
    const { topic } = req.body as { topic?: string };

    if (!topic || typeof topic !== "string") {
      return res.status(400).json({
        ok: false,
        error: "topic(string) is required",
      });
    }

    const initialState: LowQualityGraphState = { topic };

    const result = await lowAgent.invoke(initialState);

    return res.json({
      ok: true,
      mode: "low",
      topic: result.topic,
      results: result.results || [],
      scrapedCount: result.scraped?.length || 0,
      summary: result.summary || null, // low 에서 핵심
    });
  } catch (err: any) {
    console.error(err);
    return res.status(500).json({
      ok: false,
      error: err?.message || "internal error",
    });
  }
});

app.post("/research/high", async (req, res) => {
  try {
    const { topic } = req.body as { topic?: string };

    if (!topic || typeof topic !== "string") {
      return res.status(400).json({
        ok: false,
        error: "topic(string) is required",
      });
    }

    const initialState: HighQualityGraphState = { topic };

    const result = await highAgent.invoke(initialState);

    return res.json({
      ok: true,
      mode: "high",
      topic: result.topic,
      results: result.results || [],
      scrapedCount: result.scraped?.length || 0,
      pageSummaries: result.pageSummaries || [],
      finalReport: result.finalReport || null, // high에서 핵심
    });
  } catch (err: any) {
    console.error(err);
    return res.status(500).json({
      ok: false,
      error: err?.message || "internal error",
    });
  }
});

app.listen(port, () => {
  console.log(`Research agent API listening on port ${port}`);
});
