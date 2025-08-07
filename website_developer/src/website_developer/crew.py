from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileWriterTool, FileReadTool
from typing import List
import os
import subprocess
import shutil


file_read_tool = FileReadTool(file_path="output/token_metadata.json")
site_writer_tool = FileWriterTool(directory="output/sites")
mood_writer_tool = FileWriterTool(directory="output/moods")


@CrewBase
class WebsiteDeveloper:
    """WebsiteDeveloper crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def _copy_token_image(self, symbol: str):
        """Copy token_image.png into each site's images folder before deployment."""
        src = "output/images/token_image.png"
        dst_dir = f"output/sites/{symbol}/images"
        if os.path.exists(src):
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(src, dst_dir)
            print(f"🖼 Copied token_image.png → {dst_dir}")
        else:
            print(f"⚠️ Token image not found at {src}")

    @after_kickoff
    def deploy_to_netlify_sites(self, output):
        print("🚀 Starting deployment via Netlify...\n")

        sites_dir = "output/sites"
        if not os.path.exists(sites_dir):
            print("⚠️ No sites found to deploy.")
            return

        deployed = []

        for symbol in os.listdir(sites_dir):
            site_path = os.path.join(sites_dir, symbol)
            if not os.path.isdir(site_path):
                continue

            # ✅ 배포 전 이미지 복사
            self._copy_token_image(symbol)

            site_name = f"{symbol.lower()}-token-site"
            print(f"📦 Deploying {symbol} as '{site_name}'...")

            # ✅ Netlify 사이트 생성 (이미 있으면 오류 무시)
            result = subprocess.run(
                ["netlify", "sites:create", "--name", site_name],
                cwd=site_path,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                print(f"❌ Failed to create site '{site_name}'")
                print("🔴 stderr:")
                print(result.stderr)
                print("🔵 stdout:")
                print(result.stdout)
                continue

            else:
                print(f"✅ Created site '{site_name}'")

            # ✅ 배포 실행
            deploy_result = subprocess.run(
                ["netlify", "deploy", "--prod", "--dir", ".", "--site", site_name],
                cwd=site_path,
                capture_output=True,
                text=True,
            )

            if deploy_result.returncode == 0:
                for line in deploy_result.stdout.splitlines():
                    if "Website Draft URL" in line or "Website URL" in line:
                        url = line.split(":")[-1].strip()
                        deployed.append((symbol, url))
                        print(f"✅ Deployed {symbol} → {url}")
                        break
            else:
                print(f"❌ Failed to deploy {symbol}")
                print(deploy_result.stderr)

        # ✅ 리포트 저장
        if deployed:
            report_path = "output/deployment_report.md"
            with open(report_path, "w") as f:
                f.write("# 📦 Netlify Deployment Report\n\n")
                for symbol, url in deployed:
                    f.write(f"- **{symbol}** → [{url}]({url})\n")

            print(f"\n📝 Report saved to `{report_path}`")
        else:
            print("\n⚠️ No deployments were successful.")

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
        """Creates the WebsiteDeveloper crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
