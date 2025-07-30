# src/meme_landing/tools/layout_matcher.py

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yaml
import random
import os

class LayoutMatcherInput(BaseModel):
    description: str = Field(..., description="Token description text")
    image_prompt: str = Field(..., description="Image prompt for the token")


class LayoutMatcherTool(BaseTool):
    name: str = "Layout Matcher Tool"
    description: str = (
        "Matches a layout pattern based on a meme token's description and image prompt "
        "using the layout_patterns.yaml configuration."
    )
    args_schema: Type[BaseModel] = LayoutMatcherInput

    def _run(self, description: str, image_prompt: str) -> str:
        # 경로 안전하게 지정
        pattern_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "config", "layout_patterns.yaml")
        )

        if not os.path.exists(pattern_path):
            raise FileNotFoundError(f"layout_patterns.yaml not found at {pattern_path}")

        with open(pattern_path, "r") as f:
            layout_patterns = yaml.safe_load(f)["layout_patterns"]

        desc = (description + " " + image_prompt).lower()

        if "love" in desc or "memory" in desc:
            name = "Floating Island"
        elif "surprise" in desc or "unexpected" in desc or "chaos" in desc:
            name = "Split Screen Chaos"
        elif "military" in desc or "discipline" in desc or "rocket" in desc:
            name = "Meme Matrix"
        elif "retro" in desc or "arcade" in desc:
            name = "Retro Arcade"
        else:
            name = random.choice(["Classic Centered", "ZigZag Dynamic", "Pop-Art Party"])

        pattern = next(p for p in layout_patterns if p["name"] == name)
        return yaml.dump(pattern, allow_unicode=True)
