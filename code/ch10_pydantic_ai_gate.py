"""The approval gate from ch10 @sec-rt-pydantic-ai, runnable with no API key.

FunctionModel scripts the model's replies; the framework's real control flow
runs. Verified against pydantic-ai 2.34.0.

    pip install pydantic-ai
    python ch10_pydantic_ai_gate.py
"""

from pydantic_ai import Agent, DeferredToolRequests, DeferredToolResults, ToolDenied
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

calls: list[tuple[str, str]] = []


def scripted(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
    """First turn: call publish. Every turn after: finish."""
    if sum(1 for m in messages if m.kind == "response") == 0:
        return ModelResponse(parts=[ToolCallPart("publish", {"path": "cut.mp4", "channel": "main"})])
    return ModelResponse(parts=[TextPart("done")])


producer = Agent(FunctionModel(scripted), output_type=[str, DeferredToolRequests])


@producer.tool_plain(requires_approval=True)
def publish(path: str, channel: str) -> str:
    """Irreversible. Publishes the cut."""
    calls.append((path, channel))
    return f"published {path} to {channel}"


def run(decision):
    """Run once, answer the pending approval with `decision`, return (output, calls)."""
    calls.clear()
    result = producer.run_sync("make the episode")
    assert isinstance(result.output, DeferredToolRequests), "no approval surfaced"
    assert calls == [], "the tool ran before it was approved"

    results = DeferredToolResults()
    for call in result.output.approvals:
        results.approvals[call.tool_call_id] = decision
    result = producer.run_sync(message_history=result.all_messages(), deferred_tool_results=results)
    return result.output, list(calls)


if __name__ == "__main__":
    out, ran = run(True)
    print(f"approved: {out!r} | tool ran: {ran}")
    assert ran == [("cut.mp4", "main")]

    out, ran = run(ToolDenied("operator declined"))
    print(f"denied:   {out!r} | tool ran: {ran}")
    assert ran == []

    print("\nthe gate holds: no effect before approval, no effect on denial")
