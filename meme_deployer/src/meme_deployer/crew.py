from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileWriterTool, FileReadTool
from crewai_tools import DallETool
from typing import List
from meme_deployer.tools.download_image_tool import DownloadImageTool
from meme_deployer.tools.final_token_metadata_writer import FinalTokenMetadataWriter


file_read_tool = FileReadTool(file_path="../../output/final.md")
prompt_writer_tool = FileWriterTool(directory="output/prompts", overwrite=True)
metadata_writer_tool = FileWriterTool(directory="output/metadata", overwrite=True)
dalle_tool = DallETool(model="dall-e-3", size="1024x1024", quality="standard", n=1)
metadata_read_tool = FileReadTool(file_path="../../output/metadata/token_metadata.md")


@CrewBase
class MemeDeployer:
    """MemeDeployer crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

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

    @agent
    def image_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["image_generator"],
            tools=[dalle_tool, DownloadImageTool()],
        )

    @agent
    def metadata_assembler(self) -> Agent:
        return Agent(
            config=self.agents_config["metadata_assembler"],
            tools=[metadata_read_tool, FinalTokenMetadataWriter()],
        )

    @task
    def generate_token_metadata(self) -> Task:
        return Task(config=self.tasks_config["generate_token_metadata"])

    @task
    def generate_image_prompt(self) -> Task:
        return Task(config=self.tasks_config["generate_image_prompt"])

    @task
    def generate_image_from_file(self) -> Task:
        return Task(config=self.tasks_config["generate_image_from_file"])

    @task
    def assemble_metadata(self) -> Task:
        return Task(config=self.tasks_config["assemble_metadata"])

    @crew
    def crew(self) -> Crew:
        """Creates the MemeDeployer crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
