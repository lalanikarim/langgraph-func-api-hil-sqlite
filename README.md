# Overview

Example code for LangGraph Functional API to test Human in the Loop.

There are 5 scripts in this repository:

1. :white_check_mark: [hil-func.py](hil-func.py)
2. :white_check_mark: [hil-func-input.py](hil-func-input.py)
3. :white_check_mark: [hil-func-input-sqlite.py](hil-func-input-sqlite.py)
4. :white_check_mark: [hil-func-input-sqlite-sync.py](hil-func-input-sqlite-sync.py)
5. :white_check_mark: [hil-func-input-sqlite-async.py](hil-func-input-sqlite-async.py)

# Pre-requisite

Easiest way to run these scripts is using [uv from Astral](https://docs.astral.sh/uv/).  

Once `uv` is installed, you can run the scripts using `uv run script.py <additional args>`.

# Code

1. [hil-func.py](hil-func.py)

This example code is lifted from [https://langchain-ai.github.io/langgraph/how-tos/wait-user-input-functional/#simple-usage].  

It uses `MemorySaver` and the purpose is to demonstrate how you might introduce human-in-the-loop using `interrupt` function.

```bash
uv run hil-func.py
```

2. [hil-func-input.py](hil-func-input.py)

This example adds additional logic to `hil-func.py` to inspect the current event and collect feedback from the user using the `input` statement.

```bash
uv run hil-func-input.py
```

3. [hil-func-input-sqlite.py](hil-func-input-sqlite.py)

Same code as `hil-func-input.py` but replaces `MemorySaver` with `SqliteSaver` for on disk persistence for checkpointing.

```bash
uv run hil-func-input-sqlite.py
```

4. [hil-func-input-sqlite-sync.py](hil-func-input-sqlite-sync.py)

Modified version of [hil-func-input-sqlite.py] to further test on disk checkpointing persistance.  
It takes 2 arguments:
1. thread id
2. user input
It inspects the state of the runtime config to check if there is an pending interrupt that needs handling.  
If no interrupt is found, then the user input is treated as a prompt.
If interrupt is found, then user input is treated as human feedback.

```bash
# first run for prompt
uv run hil-func-input-sqlite-sync.py 1 prompt

# second run for HIL feedback
uv run hil-func-input-sqlite-sync.py 1 feedback
```

5. [hil-func-input-sqlite-async.py](hil-func-input-sqlite-async.py)

Async version of [hil-func-input-sqlite-sync.py] that uses `AsyncSqliteSaver` instead of `SqliteSaver`.  
~~This version doesn't seem to behave as expected. The `interrupt` doesn't seem to be recorded in the checkpoint for some reason.  
This needs further investigation.~~ Fixed in `langgraph-checkpoint-sqlite==2.0.6`.

```bash
# first run for prompt
uv run hil-func-input-sqlite-async.py 2 prompt

# second run for HIL feedback
uv run hil-func-input-sqlite-async.py 2 feedback
```
