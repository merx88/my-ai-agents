from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import ScrapeWebsiteTool

# Uncomment the following line to use an example of a custom tool
# from summarizer_bot.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class SummarizerBot():
	"""SummarizerBot crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# @before_kickoff # Optional hook to be executed before the crew starts
	# def pull_data_example(self, inputs):
	# 	# Example of pulling data from an external API, dynamically changing the inputs
	# 	inputs['extra_data'] = "This is extra data"
	# 	return inputs


	@before_kickoff # Optional hook to be executed before the crew starts
	def get_url(self, inputs):
		if not inputs.get("url"):
			url = input("📥 Plz put a url you want to summerize: ")
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
            config=self.agents_config['scrapper'],
            tools=[ScrapeWebsiteTool()],  
            verbose=True
        )

	@agent
	def summerizer(self) -> Agent:
		return Agent(
			config=self.agents_config['summerizer'],
			verbose=True
		)

	@task
	def scrapping_task(self) -> Task:
		return Task(
			config=self.tasks_config['scrapping_task']
		)

	@task
	def summerizing_task(self) -> Task:
		return Task(
			config=self.tasks_config['summerizing_task'],
			output_file='report.md'
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
