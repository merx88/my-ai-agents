// graph.ts
import { StateGraph, START, END } from "@langchain/langgraph";
import { ComicGraphStateSchema } from "./types";
import { scenarioNode } from "./nodes/scenarioNode";
import { cartoonNode } from "./nodes/cartoonNode"; // 네가 만든 cartoonNode
import { imageNode } from "./nodes/imageNode";

export function runComicGraph() {
  const graph = new StateGraph(ComicGraphStateSchema)
    .addNode("scenarioNode", scenarioNode)
    .addNode("cartoonNode", cartoonNode)
    .addNode("imageNode", imageNode)
    .addEdge(START, "scenarioNode")
    .addEdge("scenarioNode", "cartoonNode")
    .addEdge("cartoonNode", "imageNode")
    .addEdge("imageNode", END);

  return graph.compile();
}
