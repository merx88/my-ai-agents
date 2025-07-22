
from notion_client import Client

class NotionTrendUploader:
    def __init__(self, api_key: str, database_id: str):
        self.notion = Client(auth=api_key)
        self.database_id = database_id

    def upload_trends(self, trends):
        db_info = self.notion.databases.retrieve(database_id=self.database_id)
        print(db_info["properties"])

        for rank, keyword, reason in reversed(trends):
            try:
                self.notion.pages.create(
                    parent={"database_id": self.database_id},
                    properties={
                        "키워드": {
                            "title": [
                                {
                                    "text": {
                                        "content": keyword
                                    }
                                }
                            ]
                        },
                        "순위": {
                            "number": rank
                        },
                        "선정 이유": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": reason
                                    }
                                }
                            ]
                        }
                    }
                )
            except Exception as e:
                print(f"[오류] {keyword} 업로드 실패: {e}")
