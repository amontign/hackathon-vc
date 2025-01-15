from openai import OpenAI

import json

with open('topics.json', 'r') as file:
    data = json.load(file)

# data["topic"] is prompt

YOUR_API_KEY = "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"

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

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="llama-3.1-sonar-large-128k-online",
    messages=messages,
)
print(response)
