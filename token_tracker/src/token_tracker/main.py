#!/usr/bin/env python
import sys
import warnings


from token_tracker.crew import TokenTracker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


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

def run():
    """
    Run the crew.
    """
    
    try:
        TokenTracker().crew().kickoff(inputs={"tokens": memecoins})
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         TokenTracker().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         TokenTracker().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
    
#     try:
#         TokenTracker().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
