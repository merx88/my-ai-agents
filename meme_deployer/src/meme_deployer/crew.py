from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileWriterTool, FileReadTool
from crewai_tools import DallETool
from typing import List

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

file_read_tool = FileReadTool(file_path="../../output/final.md")
meme_tokens_writer_tool = FileWriterTool(
    file_name="meme_tokens.md", directory="output", overwrite=True
)
prompt_writer_tool = FileWriterTool(
    directory="output/prompts",
    overwrite=True
)
metadata_writer_tool = FileWriterTool(
    directory="output/metadata",
    overwrite=True
)
image_saver_tool = FileWriterTool(directory="output/images", overwrite=True)
dalle_tool = DallETool(model="dall-e-3", size="1024x1024", quality="standard", n=1)
meme_tokens_read_tool = FileReadTool(file_path="../../output/meme_tokens.md")


@CrewBase
class MemeDeployer:
    """MemeDeployer crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # @agent
    # def meme_token_creator(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["meme_token_creator"],
    #         tools=[file_read_tool, meme_tokens_writer_tool],
    #     )

    # @agent
    # def meme_token_image_generator(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["meme_token_image_generator"],
    #         tools=[meme_tokens_read_tool, dalle_tool, image_saver_tool],
    #     )

    @agent
    def token_meta_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["token_meta_generator"],
            tools=[file_read_tool, metadata_writer_tool],
        )

    @agent
    def visual_prompt_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["visual_prompt_generator"],
            tools=[file_read_tool, prompt_writer_tool],
        )
    # @task
    # def create_meme_tokens(self) -> Task:
    #     return Task(config=self.tasks_config["create_meme_tokens"])

    # @task
    # def generate_meme_token_images(self) -> Task:
    #     return Task(config=self.tasks_config["generate_meme_token_images"])

    @task
    def generate_token_metadata(self) -> Task:
        return Task(config=self.tasks_config["generate_token_metadata"])

    @task
    def generate_image_prompt(self) -> Task:
        return Task(config=self.tasks_config["generate_image_prompt"])


    @crew
    def crew(self) -> Crew:
        """Creates the MemeDeployer crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
