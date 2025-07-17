from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import ScrapeWebsiteTool,FileWriterTool

# Uncomment the following line to use an example of a custom tool
# from summarizer_bot.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool
file_writer_scrapped_site = FileWriterTool(file_name="scrapped_site.txt", directory="output")


@CrewBase
class TrendingScraper():
	"""TrendingScraper crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff # Optional hook to be executed before the crew starts
	def get_url(self, inputs):
		if not inputs.get("url"):
			url = 'https://namu.wiki/w/%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4:%EB%8C%80%EB%AC%B8'
			inputs["url"] = url.strip()
		return inputs
 

	@after_kickoff # Optional hook to be executed after the crew has finished
	def log_results(self, output):
		# Example of logging results, dynamically changing the output
		print(f"Result: \n{output}")
		return output

	@agent
	def scrapper(self) -> Agent:
		return Agent(
            config=self.agents_config['trending_keyword_scrapper'],
            tools=[ScrapeWebsiteTool(),file_writer_scrapped_site],  
            verbose=True
        )


	@task
	def scrapping_task(self) -> Task:
		return Task(
			config=self.tasks_config['trending_keyword_scrapping_task']
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the SummarizerBot crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
