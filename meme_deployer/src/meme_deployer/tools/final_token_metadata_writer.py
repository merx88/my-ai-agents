from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import os
import json

class FinalMetadataToolInput(BaseModel):
    metadata_path: str = Field(..., description="Path to the JSON metadata file")
    image_path: str = Field(..., description="Path to the image file")

class FinalTokenMetadataWriter(BaseTool):
    name: str = "FinalTokenMetadataWriter"
    description: str = (
        "Reads JSON metadata and image path, combines them into a Python dictionary named "
        "`final_token_metadata`, and saves it to output/final_token_metadata.py"
    )
    args_schema: Type[BaseModel] = FinalMetadataToolInput

    def _run(self, metadata_path: str, image_path: str) -> str:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        final_token_metadata = {
            "name": metadata["name"],
            "symbol": metadata["symbol"],
            "description": metadata["description"],
            "image_path": image_path
        }

        os.makedirs("output", exist_ok=True)
        with open("output/final_token_metadata.py", "w", encoding="utf-8") as f:
            f.write("final_token_metadata = ")
            f.write(json.dumps(final_token_metadata, indent=2))
            f.write("\n")

        return "✅ Saved to output/final_token_metadata.py"
