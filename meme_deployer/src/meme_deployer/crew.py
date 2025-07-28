from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileWriterTool, FileReadTool
from crewai_tools import DallETool
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

file_read_tool = FileReadTool(file_path='../../output/final.md')
meme_tokens_writer_tool = FileWriterTool(file_name="meme_tokens.md", directory="output", overwrite=True )
dalle_tool = DallETool(model="dall-e-3",size="1024x1024",quality="standard",n=1)

@CrewBase
class MemeDeployer():
    """MemeDeployer crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def meme_token_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["meme_token_creator"],
            tools=[file_read_tool, meme_tokens_writer_tool],
        )

    @agent
    def meme_token_image_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["meme_token_image_generator"],
            tools=[dalle_tool],  # 여기에 DALL·E나 자체 생성 툴 연동 가능
        )


    @task
    def create_meme_tokens(self) -> Task:
        return Task(config=self.tasks_config["create_meme_tokens"])

    @task
    def generate_meme_token_images(self) -> Task:
        return Task(config=self.tasks_config["generate_meme_token_images"])

    @crew
    def crew(self) -> Crew:
        """Creates the MemeDeployer crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
