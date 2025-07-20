from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import ScrapeWebsiteTool, FileWriterTool

# from crewai_tools import FirecrawlCrawlWebsiteTool

from crewai_tools import SeleniumScrapingTool


selenium_scraping_tool = SeleniumScrapingTool(website_url='https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8', css_element='.S8ooZIk2 OUzdD2Mn', wait_time=5 )


# Uncomment the following line to use an example of a custom tool
# from summarizer_bot.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool
file_writer_scraped_site = FileWriterTool(
    file_name="scraped_site.md", directory="output"
)


@CrewBase
class TrendingScraper:
    """TrendingScraper crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # @before_kickoff  # Optional hook to be executed before the crew starts
    # def get_url(self, inputs):
    #     if not inputs.get("url"):
    #         url = "https://arca.live/b/namuhotnow"
    #         inputs["url"] = url.strip()
    #     return inputs

    @after_kickoff  # Optional hook to be executed after the crew has finished
    def print_results(self, output):
        # Example of logging results, dynamically changing the output
        print(f"Result: \n{output}")
        return output

    @agent
    def site_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["site_scraper"],
            tools=[selenium_scraping_tool, file_writer_scraped_site],
            verbose=True,
        )

    @agent
    def realtime_trending_keyword_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config["realtime_trending_keyword_extractor"],
            # tools=[ScrapeWebsiteTool(), file_writer_scrapped_site],
            verbose=True,
        )

    @task
    def site_scrapping_task(self) -> Task:
        return Task(config=self.tasks_config["site_scraping_task"])

    @task
    def realtime_trending_keyword_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["realtime_trending_keyword_extraction_task"]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SummarizerBot crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
