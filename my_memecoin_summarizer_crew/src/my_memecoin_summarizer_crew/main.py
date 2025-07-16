from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start

from my_memecoin_summarizer_crew.crews.summary_crew.summary_crew import SummaryCrew
from my_memecoin_summarizer_crew.crews.gmail_crew.gmail_crew import GmailCrew

memecoins = {
    "Torch of Liberty": {
        "symbol": "Liberty",
        "address": "0x6ea8211a1e47dbd8b55c487c0b906ebc57b94444",
    },
    "EGL1": {
        "symbol": "EGL1",
        "address": "0xf4b385849f2e817e92bffbfb9aeb48f950ff4444",
    },
    "Janitor": {
        "symbol": "Janitor",
        "description": "Janitor Memecoin",
        "address": "0x3c8d20001fe883934a15c949a3355a65ca984444",
    },
}


class MyMemecoinSummarizerState(BaseModel):
    summary: str = ""


class MyMemecoinSummarizerFlow(Flow[MyMemecoinSummarizerState]):

    @start()
    def generate_summaries(self):
        print("🏁 Start!")
        print("🏃 Generating memecoin summary...")
        crew = SummaryCrew()

        self.state.summary = str(crew.crew().kickoff(inputs={"tokens": memecoins}))
        print(f"Summary: {self.state.summary}")

    @listen(generate_summaries)
    def send_summary_email(self):
        print("📧 Saving summary on Gmail draft...")
        crew = GmailCrew()
        inputs = {"body": self.state.summary}
        crew.crew().kickoff(inputs)


def kickoff():
    my_memecoin_summarizer_flow = MyMemecoinSummarizerFlow()
    my_memecoin_summarizer_flow.kickoff()


if __name__ == "__main__":
    kickoff()
