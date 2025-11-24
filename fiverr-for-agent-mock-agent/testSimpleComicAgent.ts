// example.ts
import "dotenv/config";
import { runComicGraph } from "./simple-comic-agent/graph";
import fs from "fs";

async function main() {
  const graph = runComicGraph();

  const result = await graph.invoke({
    prompt: "블록체인이 뭔지 완전 초보한테 설명해주는 4컷 만화 만들어줘",
  });

  // 텍스트 콘티
  console.log(result.page);

  // 이미지 (Base64)
  if (result.imageBase64) {
    console.log("Image base64 length:", result.imageBase64.length);
    const buffer = Buffer.from(result.imageBase64, "base64");
    fs.writeFileSync("comic.png", buffer);
    console.log("Saved as comic.png");
  }
}

main().catch(console.error);
