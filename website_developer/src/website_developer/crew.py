# website_developer.py
# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import shutil
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileWriterTool, FileReadTool

from utils.deploy_website import deploy_sites_under

file_read_tool = FileReadTool(file_path="output/token_metadata.json")
site_writer_tool = FileWriterTool(directory="output/sites")
mood_writer_tool = FileWriterTool(directory="output/moods")


@CrewBase
class WebsiteDeveloper:
    """WebsiteDeveloper crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def _copy_token_image(self, symbol: str) -> None:
        src = "output/images/token_image.png"
        dst_dir = f"output/sites/{symbol}/images"
        if os.path.exists(src):
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(src, dst_dir)
            print(f"🖼 Copied token_image.png → {dst_dir}")
        else:
            print(f"⚠️ Token image not found at {src}")

    @after_kickoff
    def deploy_to_cloudflare_pages(self, output) -> None:
        sites_dir = "output/sites"
        deploy_sites_under(
            sites_dir=sites_dir,
            image_copier=self._copy_token_image,
            branch="main",
            report_path="output/deployment_report.md",
        )

    @agent
    def meme_mood_curator(self) -> Agent:
        return Agent(
            config=self.agents_config["meme_mood_curator"],
            tools=[file_read_tool, mood_writer_tool],
        )

    @agent
    def meme_token_site_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["meme_token_site_designer"],
            tools=[file_read_tool, site_writer_tool],
        )

    @task
    def extract_token_moods(self) -> Task:
        return Task(config=self.tasks_config["extract_token_moods"])

    @task
    def build_meme_token_sites(self) -> Task:
        return Task(config=self.tasks_config["build_meme_token_sites"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
