from openai import OpenAI

import json

prompt_path = '../backend/src/prompts/ai_use_cases.txt'

with open(prompt_path, 'r') as file:
    data = file.read()

# with open('../backend/src/prompts/ai_use_cases.txt', 'r') as file:


# data["topic"] is prompt

messages = [
    {
        "role": "system",
        "content": (
            "You are a market research assistant specializing in venture capital analysis."
        ),
    },
    {
        "role": "user",
        "content": (
            data["investment_analysis"]
        ),
    },
]

client = OpenAI(api_key=YOUR_API_KEY,base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="llama-3.1-sonar-large-128k-online",
    messages=messages,
)
print(response)
