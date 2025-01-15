import json
import asyncio
from ai import PerplexityWrapper
from job import Job
from settings import SRC_DIR


class ParallelQuestions:
    """
    A simple class to ask multiple questions asynchronously,
    with staggered start times for each task.
    """

    def __init__(self, topic, job: Job):
        self.perplexity = PerplexityWrapper()
        self.job = job
        self.responses = []
        self.topic = topic
        with open(SRC_DIR / 'prompts' / 'overview_questions.json', 'r') as f:
            self.prompts = json.load(f)
        with open(SRC_DIR / 'prompts' / 'overview_role.txt', 'r') as f:
            self.role = f.read()

    async def ask_all(self):
        tasks = []
        # Schedule tasks with incremental delays
        for i, (key, prompt) in enumerate(self.prompts.items()):
            # Each subsequent task starts 1.5s after the previous
            delay = i * 1.5
            tasks.append(asyncio.create_task(self._ask_question(key, prompt, delay)))

        # Wait for all tasks to finish
        results = await asyncio.gather(*tasks)

        return results

    async def _ask_question(self, key, prompt, delay):
        # Wait the specified delay before starting the request
        await asyncio.sleep(delay)
        prompt = f"{prompt}\nMy topic is {self.topic}."  # noqa: E501}
        self.job.message = f'Asking about {key}'
        print(self.job.message)
        # Perform the API call
        answer = await self.perplexity.get_answer(role=self.role, question=prompt)
        self.job.message = f'Got answer about {key}'
        print(self.job.message)
        return prompt, answer


async def main():
    pq = ParallelQuestions("Federated GraphQl", job=Job.create())
    answers = await pq.ask_all()
    for prompt, response in answers:
        print(f"*{prompt}*:\n{response}\n")


if __name__ == "__main__":
    asyncio.run(main())
