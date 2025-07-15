from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start

# from crews.memecoin_summary_crew.memecoin_summary_crew import MemecoinSummaryCrew
from my_memecoin_summarizer_crew.crews.gmail_crew.gmail_crew import GmailCrew

# memecoins = {
#     "DOGE": "Dogecoin is a cryptocurrency featuring a likeness of the Shiba Inu dog.",
#     "PEPE": "Pepe is a meme coin inspired by the Pepe the Frog meme.",
# }


class MyMemecoinSummarizerState(BaseModel):
    summary: str = ""


class MyMemecoinSummarizerFlow(Flow[MyMemecoinSummarizerState]):

    @start()
    def generate_summaries(self):
        print("밈코인 요약 생성 중...")
        # crew = MemecoinSummaryCrew()
        # summaries = []
        # for name, desc in memecoins.items():
        #     # 각 밈코인별 요약 생성
        #     summary = crew.crew().kickoff({"name": name, "description": desc})
        #     summaries.append(f"{name}: {summary}")
        self.state.summary = "is testing2..."
        print(f"Summary: {self.state.summary}")

    @listen(generate_summaries)
    def send_summary_email(self):
        print("지메일로 밈코인 요약 전송 중...")
        crew = GmailCrew()
        inputs = {"body": self.state.summary}
        crew.crew().kickoff(inputs)


def kickoff():
    my_memecoin_summarizer_flow = MyMemecoinSummarizerFlow()
    my_memecoin_summarizer_flow.kickoff()


if __name__ == "__main__":
    kickoff()
