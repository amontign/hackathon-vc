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

    async def _get_answer(self, role: str, question: str) -> [Optional[str], Optional[str]]:
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
            citations = response.model_extra.get('citations')
            return response.choices[0].message.content, citations
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

    @staticmethod
    def format_result(message: str, citations: list) -> str:
        ...

    async def get_answer(self, role: str, question: str) -> [Optional[str], Optional[str]]:
        message, citations = await self._get_answer(role, question)
        return self.format_result(message, citations)


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

    async def get_answer(self, role: str, question: str) -> [Optional[str], Optional[str]]:
        return await self._get_answer(role, question)[0]


def test():
    example_message = """
            To forecast the market growth and size for Federated GraphQL over the next five years, we can rely on several key insights and predictions from industry analysts and reports.

    ## Market Growth and Adoption

    - According to Gartner predictions, by 2027, more than 60% of enterprises will use GraphQL in production, up from less than 30% in 2024. Specifically, Gartner forecasts that by 2027, 30% of enterprises utilizing GraphQL will employ GraphQL federation, a significant increase from less than 5% in 2024[1][5].

    ## Driving Factors

    - **Personalization and Omnichannel Strategies**: The need for personalized and omnichannel experiences is driving the adoption of GraphQL Federation. This technology enables enterprises to combine hundreds or thousands of business and domain APIs, facilitating the rapid and cost-effective building of world-class customer experiences[2].
    - **Mergers and Acquisitions**: The integration of multiple APIs from different domains and systems, often resulting from mergers and acquisitions, is another driving factor. GraphQL Federation helps in managing and combining these APIs efficiently[2].
    - **AI-Driven Experiences**: The increasing demand for AI-driven experiences is also propelling the adoption of GraphQL Federation, as it integrates seamlessly with AI technologies to enhance API interactions[2].

    ## Potential Obstacles

    - **Scaling Challenges**: One of the potential obstacles is the challenge of scaling GraphQL Federation. Enterprises need to implement well-known architectural best practices, such as decoupling the graph by concern and using microservice-like architectures, to manage and scale traffic effectively[3].
    - **Centralized Governance**: While GraphQL Federation offers centralized governance, ensuring that this governance is balanced with team autonomy can be a challenge. Proper implementation and management are crucial to avoid bottlenecks and maintain the benefits of federation[1][5].

    ## Breakdown by Key Segments or Regions

    While the reports do not provide a detailed regional breakdown specifically for GraphQL Federation, the adoption trends are generally observed across various industries globally, including retail, media, banking, and more.

    - **Industry Segments**: GraphQL Federation is being adopted across multiple industries, with significant traction in sectors that require complex API integrations and personalized customer experiences. For example, retail and banking sectors are among the early adopters due to their need for integrated and scalable API solutions[2].

    ## Conclusion

    Given the forecasts and driving factors, here is a summary of the projected growth:

    - **Adoption Rate**: By 2027, 30% of enterprises using GraphQL are expected to employ GraphQL Federation, indicating a substantial growth from the current less than 5% in 2024.
    - **Industry-Wide Adoption**: More than 60% of enterprises are expected to use GraphQL in production by 2027, which will likely drive the demand for GraphQL Federation as a key component of their API strategies.
    - **Growth Drivers**: Personalization, omnichannel strategies, mergers and acquisitions, and the integration with AI technologies are key drivers of this growth.

    While specific financial projections for the GraphQL Federation market are not provided in the sources, the anticipated increase in adoption rates and the broad industry applicability suggest significant market growth over the next five years."""
    example_citations = ['https://www.apollographql.com/resources/gartner-when-to-use-graphql-to-accelerate-api-delivery',
                         'https://www.apiscene.io/ai-and-apis/graphql-federation-combining-apis-for-ai-era/',
                         'https://www.apollographql.com/blog/9-lessons-from-a-year-of-apollo-federation/',
                         'https://www.grandviewresearch.com/industry-analysis/education-technology-market',
                         'https://graphql.org/conf/2024/schedule/9b4f92f2579d24a3c20e6533686aca6b/']

    print(PerplexityWrapper().format_result(example_message, example_citations))

if __name__ == "__main__":
    test()