from abc import ABC, abstractmethod
from functools import cached_property
from typing import Optional
from openai import AsyncOpenAI
from settings import OPENAI_API_KEY, PERPLEXITY_KEY


class BaseAIWrapper(ABC):
    """
    Base wrapper for AI clients to handle common functionality.
    Subclasses must define a class-level MODEL constant.
    """
    MODEL: str = None  # Must be defined in subclasses

    def __init__(self):
        if not self.MODEL:
            raise ValueError(f"{self.__class__.__name__} must define a MODEL attribute.")

    @property
    @abstractmethod
    def client(self) -> AsyncOpenAI:
        """Abstract property to be implemented in subclasses."""
        pass

    async def get_answer(self, role: str, question: str) -> Optional[str]:
        """
        Generates a response using the AI model asynchronously.
        Args:
            role (str): The role for the system message (e.g., system instructions).
            question (str): The user's question.

        Returns:
            Optional[str]: The generated response or None if an error occurs.
        """
        try:
            messages = [
                {"role": "system", "content": role},
                {"role": "user", "content": question},
            ]

            response = await self.client.chat.completions.create(
                model=self.MODEL,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling API: {str(e)}")
            return None


class PerplexityWrapper(BaseAIWrapper):
    """
    Wrapper for the Perplexity AI client.
    """
    MODEL = "llama-3.1-sonar-large-128k-online"  # Define specific model for this wrapper

    @cached_property
    def client(self) -> AsyncOpenAI:
        return AsyncOpenAI(
            api_key=PERPLEXITY_KEY,
            base_url="https://api.perplexity.ai"
        )


class ChatGPTWrapper(BaseAIWrapper):
    """
    Wrapper for the OpenAI ChatGPT client.
    """
    MODEL = "gpt-4o-mini"  # Define specific model for this wrapper

    @cached_property
    def client(self) -> AsyncOpenAI:
        return AsyncOpenAI(
            api_key=OPENAI_API_KEY
        )
