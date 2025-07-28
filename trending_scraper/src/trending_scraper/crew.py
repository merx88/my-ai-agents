import sys, os
from dotenv import load_dotenv
from datetime import datetime

from notion_py.config import DATABASE_ID, NOTION_API_KEY
from notion_py.database import NotionDatabase

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(BASE_DIR)

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, after_kickoff
from crewai_tools import FileWriterTool, SeleniumScrapingTool
from crewai_tools.tools.tavily_search_tool.tavily_search_tool import TavilySearchTool


# signal_scraping_tool = SeleniumScrapingTool(website_url='https://signal.bz/',css_element='.container',wait_time=5)
namunews_scraping_tool = SeleniumScrapingTool(website_url='https://namu.news/',wait_time=5)
x_scraping_tool = SeleniumScrapingTool(website_url='https://getdaytrends.com/ko/korea/',css_element='#trends',wait_time=5)
google_scraping_tool = SeleniumScrapingTool(website_url='https://trends.google.com/trending?geo=KR&hours=24',css_element='.enOdEe-wZVHld-zg7Cn',wait_time=5)

# signal_writer_tool = FileWriterTool(file_name="signal.md", directory="output", overwrite=True )
namunews_writer_tool = FileWriterTool(file_name="namunews.md", directory="output", overwrite=True )
x_writer_tool = FileWriterTool(file_name="x.md", directory="output", overwrite=True )
google_writer_tool = FileWriterTool(file_name="google.md", directory="output", overwrite=True )

file_writer_tool = FileWriterTool(file_name="scrapped_site.md", directory="output", overwrite=True )
trend_writer_tool = FileWriterTool(file_name="trend.md", directory="output", overwrite=True )
final_writer_tool = FileWriterTool(file_name="final.md", directory="output", overwrite=True )

tavily_tool = TavilySearchTool()

now_date = datetime.now().isoformat()

@CrewBase
class TrendingScraper:
    """TrendingScraper crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @after_kickoff
    def save_results_on_notion(self, output):
        notion = NotionDatabase(NOTION_API_KEY, DATABASE_ID)
        page = notion.add_page({
            "제목": { 
                "title": [
                    {
                        "text": {
                            "content": f"트렌드 리포트"
                        }
                    }
                ]
            },
            "날짜": {  
                "date": {
                    "start": now_date
                }
            },
        })
        notion.add_blocks_from_markdown("output/final.md", page["id"])

        

    # === Agents ===


    @agent
    def namunews_trending_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["namunews_trending_scraper"],
            tools=[namunews_scraping_tool, namunews_writer_tool],
        )

    # @agent
    # def signal_trending_scraper(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["signal_trending_scraper"],
    #         tools=[signal_scraping_tool, signal_writer_tool],
    #     )

    @agent
    def x_trending_crawler(self) -> Agent:
        return Agent(
            config=self.agents_config["x_trending_crawler"],
            tools=[x_scraping_tool, x_writer_tool],
        )

    @agent
    def google_trending_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["google_trending_scraper"],
            tools=[google_scraping_tool, google_writer_tool],
        )

    @agent
    def trending_organizer(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_organizer"],
            tools=[file_writer_tool],
        )

    @agent
    def cross_validation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["cross_validation_agent"],
            tools=[trend_writer_tool],
        )

    @agent
    def trend_explainer(self) -> Agent:
        return Agent(
            config=self.agents_config["trend_explainer"],
            tools=[final_writer_tool, tavily_tool],
        )

    # @agent
    # def notion_uploader(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["notion_uploader"],
    #         tools=[notion_upload_tool],
    #         verbose=True,
    #     )

    # === Tasks ===
    @task
    def collect_namunews_trending(self) -> Task:
        return Task(config=self.tasks_config["collect_namunews_trending"])


    # @task
    # def collect_signal_trending(self) -> Task:
    #     return Task(config=self.tasks_config["collect_signal_trending"])


    @task
    def collect_x_trending(self) -> Task:
        return Task(config=self.tasks_config["collect_x_trending"])

    @task
    def collect_google_trending(self) -> Task:
        return Task(config=self.tasks_config["collect_google_trending"])

    @task
    def organize_trending(self) -> Task:
        return Task(config=self.tasks_config["organize_trending"])

    @task
    def cross_validate_trending(self) -> Task:
        return Task(config=self.tasks_config["cross_validate_trending"])

    @task
    def explain_trends(self) -> Task:
        return Task(config=self.tasks_config["explain_trends"])

    # @task
    # def upload_to_notion(self) -> Task:
    #     return Task(config=self.tasks_config["upload_to_notion"])

    # === Crew ===
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # All agents defined above
            tasks=self.tasks,    # All tasks defined above
            process=Process.sequential,
            verbose=True,
        )
