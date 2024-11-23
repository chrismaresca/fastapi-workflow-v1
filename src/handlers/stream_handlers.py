import json
from typing import Generator, Any


# -------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------- #
# Stream Handler Functions

def handle_text_protocol(stream) -> Generator[str, Any, None]:
    """Handles streaming text protocol by yielding formatted text content"""
    for chunk in stream:
        for choice in chunk.choices:
            if choice.finish_reason == "stop":
                break
            if choice.delta.content:
                yield "{text}".format(text=choice.delta.content)

def handle_tool_calls(choice, draft_tool_calls, draft_tool_calls_index, processed_tool_calls, available_tools) -> Generator[str, Any, None]:
    """Processes tool calls and yields formatted tool call and result data"""
    if draft_tool_calls:
        tool_call = draft_tool_calls[draft_tool_calls_index]
        tool_call_id = tool_call["id"]
        
        if tool_call_id not in processed_tool_calls:
            yield '9:{{"toolCallId":"{id}","toolName":"{name}","args":{args}}}\n'.format(
                id=tool_call_id,
                name=tool_call["name"],
                args=tool_call["arguments"])

            tool_result = available_tools[tool_call["name"]](
                **json.loads(tool_call["arguments"]))

            yield 'a:{{"toolCallId":"{id}","toolName":"{name}","args":{args},"result":{result}}}\n'.format(
                id=tool_call_id,
                name=tool_call["name"],
                args=tool_call["arguments"],
                result=json.dumps(tool_result))
            
            processed_tool_calls.add(tool_call_id)

def handle_tool_calls_delta(tool_calls, draft_tool_calls, draft_tool_calls_index):
    """Updates draft tool calls with delta information and returns updated index"""
    for tool_call in tool_calls:
        id = tool_call.id
        name = tool_call.function.name
        arguments = tool_call.function.arguments

        if id is not None:
            draft_tool_calls_index += 1
            draft_tool_calls.append(
                {"id": id, "name": name, "arguments": ""})
        else:
            draft_tool_calls[draft_tool_calls_index]["arguments"] += arguments
    
    return draft_tool_calls_index

def handle_data_protocol(stream, available_tools) -> Generator[str, Any, None]:
    """Handles streaming data protocol by processing tool calls and content"""
    draft_tool_calls = []
    draft_tool_calls_index = -1
    processed_tool_calls = set()

    for chunk in stream:
        for choice in chunk.choices:
            if choice.finish_reason == "tool_calls":
                yield from handle_tool_calls(
                    choice, 
                    draft_tool_calls, 
                    draft_tool_calls_index, 
                    processed_tool_calls, 
                    available_tools
                )

            elif choice.delta.tool_calls:
                draft_tool_calls_index = handle_tool_calls_delta(
                    choice.delta.tool_calls,
                    draft_tool_calls,
                    draft_tool_calls_index
                )

            elif choice.delta.content:
                yield '0:{text}\n'.format(text=json.dumps(choice.delta.content))

        if chunk.choices == [] and chunk.usage:
            usage = chunk.usage
            yield 'd:{{"finishReason":"{reason}","usage":{{"promptTokens":{prompt},"completionTokens":{completion}}}}}\n'.format(
                reason="stop",
                prompt=usage.prompt_tokens,
                completion=usage.completion_tokens
            ) 

# -------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------- #