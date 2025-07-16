from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import FileWriterTool

from my_memecoin_summarizer_crew.crews.summary_crew.tools.dexscreener_tool import (
    DexscreenerTool,
)

# Tools
file_writer_data = FileWriterTool(file_name="meme_data.json", directory="data")
file_writer_report = FileWriterTool(file_name="meme_report.txt", directory="output")


@CrewBase
class SummaryCrew:
    """Memecoin Summary Crew to 1. collect data and 2. generate summary reports"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def meme_info_fetcher(self) -> Agent:
        return Agent(
            config=self.agents_config["meme_info_fetcher"],
            tools=[DexscreenerTool(), file_writer_data],
            verbose=True,
        )

    @agent
    def meme_report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["meme_report_writer"],
            tools=[file_writer_report],
            verbose=True,
        )

    @task
    def fetch_meme_data_task(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_meme_data_task"],
        )

    @task
    def write_meme_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_meme_report_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
