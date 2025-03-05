import re

def extract_content(text) -> str:
    """Extract content from text using regex."""
    match = re.search(r"content=\"(.*?)\"", text)
    if match:
        return match.group(1)
    return None

# Example text
data = '''content="It's nice to meet you. Is there something I can help you with or would you like to chat?" content_type='str' event='RunResponse' messages=[Message(role='user', content='hi', name=None, tool_call_id=None, tool_calls=None, audio=None, images=None, videos=None, tool_name=None, tool_args=None, tool_call_error=None, stop_after_tool_call=False, metrics={}, references=None, created_at=1740379979), Message(role='assistant', content="It's nice to meet you. Is there something I can help you with or would you like to chat?", name=None, tool_call_id=None, tool_calls=None, audio=None, images=None, videos=None, tool_name=None, tool_args=None, tool_call_error=None, stop_after_tool_call=False, metrics={'time': 1.1455671000294387, 'input_tokens': 36, 'prompt_tokens': 36, 'output_tokens': 23, 'completion_tokens': 23, 'total_tokens': 59, 'completion_time': 0.084989293, 'prompt_time': 0.004778713, 'queue_time': 0.233243305, 'total_time': 0.089768006}, references=None, created_at=1740379980)]''' 

content_value = extract_content(data)
print("Extracted Content:", content_value)
