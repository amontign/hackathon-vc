from openai import OpenAI

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
            "What are the current fundraising trends in the Legaltech sector as of January 2025? "
            "Please provide insights into the types of funding sources being utilized, notable recent investments, "
            "and any emerging technologies or startups that are gaining traction in this field. Additionally, "
            "it would be helpful to understand how these trends compare to previous years and what factors "
            "are driving changes in investment strategies within Legaltech."
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
