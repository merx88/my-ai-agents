
from notion_client import Client

class NotionUploader:
    def __init__(self, api_key: str, database_id: str):
        self.notion = Client(auth=api_key)
        self.database_id = database_id

    def upload_report(self, report, date):
        db_info = self.notion.databases.retrieve(database_id=self.database_id)
        print(db_info["properties"])

        properties = {
            "제목": { 
                "title": [
                    {
                        "text": {
                            "content": f"토큰 리포트"
                        }
                    }
                ]
            },
            "날짜": {  
                "date": {
                    "start":  date
                }
            },
        }

        new_page = self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )

        page_id = new_page["id"]
        file_path = f"reports/{report}.md"
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        blocks = []
        for line in lines:
            stripped = line.strip()

            if stripped.startswith("### "):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": stripped[4:]}}]
                    }
                })
            elif stripped.startswith("## "):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": stripped[3:]}}]
                    }
                })
            elif stripped.startswith("- "):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": stripped[2:]}}]
                    }
                })
            elif stripped == "":
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": []
                    }
                })  # 빈 줄 = 공백 문단
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": stripped}}]
                    }
                })

        # 5. 블록 등록
        BATCH_SIZE = 100  # Notion은 한 번에 최대 100개 블록 추가 가능
        for i in range(0, len(blocks), BATCH_SIZE):
            self.notion.blocks.children.append(
                block_id=page_id,
                children=blocks[i:i + BATCH_SIZE]
            )

