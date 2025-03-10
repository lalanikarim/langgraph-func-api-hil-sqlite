# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "langgraph",
#     "langgraph-checkpoint-sqlite>=2.0.6",
# ]
# ///
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.func import entrypoint, task
from langgraph.types import Command, interrupt
import asyncio
import sys


@task
async def step_1(input_query):
    """Append bar."""
    return f"{input_query} bar"


@task
async def human_feedback(input_query):
    """Append user input."""
    feedback = interrupt(f"Please provide feedback: {input_query}")
    return f"{input_query} {feedback}"


@task
async def step_3(input_query):
    """Append qux."""
    return f"{input_query} qux"


# checkpointer = MemorySaver()

async def main():
    async with AsyncSqliteSaver.from_conn_string("checkpoint.db") as checkpointer:
        @entrypoint(checkpointer=checkpointer)
        async def graph(input_query):
            result_1 = await step_1(input_query)
            result_2 = await human_feedback(result_1)
            result_3 = await step_3(result_2)

            return result_3

        config = {"configurable": {"thread_id": sys.argv[1]}}
        prompt = sys.argv[2]

        state = await graph.aget_state(config)
        print(f"{state=}", end="\n\n")
        if len(state.tasks) > 0:
            tasks = state.tasks
            print(f"{tasks=}", end="\n\n")
            if len(tasks[0].interrupts) > 0:
                interrupts = tasks[0].interrupts
                print(f"{interrupts=}", end="\n\n")
                prompt = Command(resume=prompt)

        async for event in graph.astream(prompt, config):
            print(f"{event=}", end="\n\n")
            if "graph" in event:
                print(f"Result: {event['graph']}")
            if "__interrupt__" in event:
                value = event["__interrupt__"][0].value
                print(f"Need Feedback: {value}")

asyncio.run(main())
