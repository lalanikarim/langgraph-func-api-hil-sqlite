# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "langgraph",
#     "langgraph-checkpoint-sqlite",
# ]
# ///
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.func import entrypoint, task
from langgraph.types import Command, interrupt
import sys


@task
def step_1(input_query):
    """Append bar."""
    return f"{input_query} bar"


@task
def human_feedback(input_query):
    """Append user input."""
    feedback = interrupt(f"Please provide feedback: {input_query}")
    return f"{input_query} {feedback}"


@task
def step_3(input_query):
    """Append qux."""
    return f"{input_query} qux"


# checkpointer = MemorySaver()


with SqliteSaver.from_conn_string("checkpoint.db") as checkpointer:
    @entrypoint(checkpointer=checkpointer)
    def graph(input_query):
        result_1 = step_1(input_query).result()
        result_2 = human_feedback(result_1).result()
        result_3 = step_3(result_2).result()

        return result_3

    config = {"configurable": {"thread_id": sys.argv[1]}}
    prompt = sys.argv[2]

    state = graph.get_state(config)
    print(f"{state=}", end="\n\n")
    if len(state.tasks) > 0:
        tasks = state.tasks
        print(f"{tasks=}", end="\n\n")
        if len(tasks[0].interrupts) > 0:
            interrupts = tasks[0].interrupts
            print(f"{interrupts=}", end="\n\n")
            prompt = Command(resume=prompt)

    for event in graph.stream(prompt, config):
        print(f"{event=}", end="\n\n")
        if "graph" in event:
            print(f"Result: {event['graph']}")
        if "__interrupt__" in event:
            value = event["__interrupt__"][0].value
            print(f"Need Feedback: {value}")
