import sys, os
from notion_trends_uploader import NotionTrendUploader
from dotenv import load_dotenv
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(BASE_DIR)

from final import result

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, after_kickoff
from crewai_tools import FileWriterTool, SeleniumScrapingTool


signal_scraping_tool = SeleniumScrapingTool(website_url='https://signal.bz/',css_element='.container',wait_time=5)
namuwiki_scraping_tool = SeleniumScrapingTool(website_url='https://arca.live/b/namuhotnow',css_element='.list-table table',wait_time=5)
x_scraping_tool = SeleniumScrapingTool(website_url='https://getdaytrends.com/ko/korea/',css_element='#trends',wait_time=5)
google_scraping_tool = SeleniumScrapingTool(website_url='https://trends.google.com/trending?geo=KR&hours=24',css_element='.enOdEe-wZVHld-zg7Cn',wait_time=5)

signal_writer_tool = FileWriterTool(file_name="signal.md", directory="output")
namuwiki_writer_tool = FileWriterTool(file_name="namuwiki.md", directory="output")
x_writer_tool = FileWriterTool(file_name="x.md", directory="output")
google_writer_tool = FileWriterTool(file_name="google.md", directory="output")

file_writer_tool = FileWriterTool(file_name="scrapped_site.md", directory="output")
final_writer_tool = FileWriterTool(file_name="final.py", directory="output")
notion_upload_tool = FileWriterTool(file_name="notion_upload.log", directory="output") 

load_dotenv() 

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")


@CrewBase
class TrendingScraper:
    """TrendingScraper crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @after_kickoff
    def save_results_on_notion(self, output):
        print("FUCK!!!",output)
        time.sleep(3) 
        
        uploader = NotionTrendUploader(NOTION_API_KEY, DATABASE_ID)
        uploader.upload_trends(result)
        

    # === Agents ===
    @agent
    def signal_trending_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["signal_trending_scraper"],
            tools=[signal_scraping_tool, signal_writer_tool],
            verbose=True,
        )

    @agent
    def namuwiki_trending_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["namuwiki_trending_scraper"],
            tools=[namuwiki_scraping_tool, namuwiki_writer_tool],
            verbose=True,
        )

    @agent
    def x_trending_crawler(self) -> Agent:
        return Agent(
            config=self.agents_config["x_trending_crawler"],
            tools=[x_scraping_tool, x_writer_tool],
            verbose=True,
        )

    @agent
    def google_trending_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["google_trending_scraper"],
            tools=[google_scraping_tool, google_writer_tool],
            verbose=True,
        )

    @agent
    def trending_organizer(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_organizer"],
            tools=[file_writer_tool],
            verbose=True,
        )

    @agent
    def cross_validation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["cross_validation_agent"],
            tools=[final_writer_tool],
            verbose=True,
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
    def collect_signal_trending(self) -> Task:
        return Task(config=self.tasks_config["collect_signal_trending"])

    @task
    def collect_namuwiki_trending(self) -> Task:
        return Task(config=self.tasks_config["collect_namuwiki_trending"])

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
