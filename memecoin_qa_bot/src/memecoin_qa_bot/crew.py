from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from memecoin_qa_bot.tools.coingecko_tool import CoingeckoTool
from memecoin_qa_bot.tools.bscscan_tool import BscscanTool
@CrewBase
class MemecoinQaBot():
	"""MemecoinQaBot crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff # Optional hook to be executed before the crew starts
	def get_question(self, inputs):
		if not inputs.get("question"):
			q = input("\n❓ You can ask question on memecoin: ")
			inputs["question"] = q.strip()
		return inputs
 
    
	@agent
	def memecoin_qa_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['memecoin_qa_agent'],
			tools=[CoingeckoTool(), BscscanTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@task
	def memecoin_question_task(self) -> Task:
		return Task(
			config=self.tasks_config['memecoin_question_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MemecoinQaBot crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
