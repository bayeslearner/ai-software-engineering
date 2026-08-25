import asyncio
from dataclasses import dataclass
from agent_framework import (WorkflowBuilder, Executor, handler, WorkflowContext,
                             RequestInfoExecutor, RequestInfoMessage, RequestInfoEvent,
                             RequestResponse)

@dataclass
class Draft:
    text: str

@dataclass
class ReviewRequest(RequestInfoMessage):
    draft: str = ""

trace = []

class Worker(Executor):
    @handler
    async def start(self, topic: str, ctx: WorkflowContext[Draft]) -> None:
        trace.append("worker.start")
        await ctx.send_message(Draft(text=f"cut of {topic}"))

    @handler
    async def revise(self, draft: Draft, ctx: WorkflowContext[Draft]) -> None:
        trace.append("worker.revise")
        await ctx.send_message(Draft(text=draft.text + " (revised)"))

class Reviewer(Executor):
    @handler
    async def ask(self, draft: Draft, ctx: WorkflowContext[ReviewRequest]) -> None:
        trace.append("reviewer.ask")
        await ctx.send_message(ReviewRequest(draft=draft.text))

    @handler
    async def decide(self, resp: RequestResponse[ReviewRequest, str],
                     ctx: WorkflowContext[Draft, str]) -> None:
        trace.append(f"reviewer.decide={resp.data}")
        if resp.data == "accept":
            await ctx.yield_output(f"PUBLISHED {resp.original_request.draft}")
        else:
            await ctx.send_message(Draft(text=resp.original_request.draft))

worker, reviewer = Worker(id="worker"), Reviewer(id="reviewer")
review = RequestInfoExecutor(id="review")

workflow = (WorkflowBuilder()
    .set_start_executor(worker)
    .add_edge(worker, reviewer)
    .add_edge(reviewer, review)
    .add_edge(review, reviewer)
    .add_edge(reviewer, worker)
    .build())

async def main():
    events = await workflow.run("episode 12")
    reqs = [e for e in events if isinstance(e, RequestInfoEvent)]
    print("trace:", trace)
    print("paused on:", reqs[0].data.draft)

    events = await workflow.send_responses({reqs[0].request_id: "reject"})
    reqs = [e for e in events if isinstance(e, RequestInfoEvent)]
    print("trace:", trace)
    print("paused on:", reqs[0].data.draft)

    result = await workflow.send_responses({reqs[0].request_id: "accept"})
    print("trace:", trace)
    print("output:", result.get_outputs())

    print("graph as data:", list(workflow.to_dict()))

asyncio.run(main())
