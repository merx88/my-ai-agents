from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileWriterTool, FileReadTool
from typing import List
from website_developer.tools.layout_matcher import LayoutMatcherTool

matcher_tool = LayoutMatcherTool()


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


file_read_tool = FileReadTool(file_path="../../output/final.md")
site_writer_tool = FileWriterTool(directory="output/sites")


@CrewBase
class WebsiteDeveloper:
    """WebsiteDeveloper crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def meme_token_site_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["meme_token_site_designer"],
            tools=[
                file_read_tool,
                site_writer_tool,
                matcher_tool
            ],
        )

    # @agent
    # def meme_token_site_deployer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["meme_token_site_deployer"],
    #         tools=[FileWriterTool(directory="output/sites", overwrite=True)],
    #     )

    @task
    def build_meme_token_sites(self) -> Task:
        return Task(config=self.tasks_config["build_meme_token_sites"])

    # @task
    # def package_sites_for_deployment(self) -> Task:
    #     return Task(config=self.tasks_config["package_sites_for_deployment"])

    @crew
    def crew(self) -> Crew:
        """Creates the WebsiteDeveloper crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
