// lib/generateImage.ts
import { GoogleGenAI } from "@google/genai";

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

if (!GEMINI_API_KEY) {
  throw new Error("GEMINI_API_KEY is not set");
}

const ai = new GoogleGenAI({
  apiKey: GEMINI_API_KEY,
});

export default async function generateImage(prompt: string) {
  console.log("[GEMINI IMAGE PROMPT]", prompt);

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash-image",
    contents: prompt,
  });

  for (const cand of response.candidates ?? []) {
    for (const part of cand.content?.parts ?? []) {
      if (part.inlineData?.data) {
        // Buffer로 리턴 (서버 사이드)
        return Buffer.from(part.inlineData.data, "base64");
      }
    }
  }

  throw new Error("No image data returned from Gemini response");
}
