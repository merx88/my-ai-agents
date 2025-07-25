import sys, os
from notion_uploader import NotionUploader
from dotenv import load_dotenv
import time
from datetime import datetime


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(BASE_DIR)

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew, after_kickoff
from crewai_tools import FileWriterTool


from token_tracker.tools.dexscreener_tool import DexscreenerTool

# Tools
data_writer_tool = FileWriterTool(file_name="token_data.json", directory="datas")
report_writer_tool = FileWriterTool(file_name="token_report.md", directory="reports")
load_dotenv() 

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

now_date = datetime.now().isoformat()


@CrewBase
class TokenTracker:
    """TokenTracker Crew to 1. collect data"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"


    @after_kickoff
    def save_results_on_notion(self, output):
        uploader = NotionUploader(NOTION_API_KEY, DATABASE_ID)
        uploader.upload_report("token_report", now_date)
        

    @agent
    def token_data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config["token_data_collector"], # pylint: disable=invalid-sequence-index
            tools=[DexscreenerTool(), data_writer_tool],
            verbose=True,
        )


    @agent
    def token_report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["token_report_writer"], # pylint: disable=invalid-sequence-index
            tools=[report_writer_tool],
            verbose=True,
        )

    @task
    def collect_token_data(self) -> Task:
        return Task(
            config=self.tasks_config["collect_token_data"],
        )

    @task
    def write_token_report(self) -> Task:
        return Task(
            config=self.tasks_config["write_token_report"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
