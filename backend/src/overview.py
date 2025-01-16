import asyncio
from settings import SRC_DIR
from ai import PerplexityWrapper
from job import Job
from typing import List


class ParallelQuestions:
    """
    A simple class to ask multiple questions asynchronously,
    with staggered start times for each task.
    """

    def __init__(self, topic, job: Job, topics: List[str] = None):
        self.perplexity = PerplexityWrapper()
        self.job = job
        self.responses = []
        self.topic = topic
        self.prompts = self.load_prompts(topics)
        with open(SRC_DIR / 'prompts' / 'overview_role.txt', 'r') as f:
            self.role = f.read()

    def load_prompts(self, topics: List[str] = None):
        prompts = {}
        prompts_dir = SRC_DIR / 'prompts' / 'overview'

        # Check if directory exists
        if not prompts_dir.exists():
            raise FileNotFoundError(f"Prompts directory not found: {prompts_dir}")

        # Get all txt files
        available_files = {file.stem: file for file in prompts_dir.glob('*.txt')}

        if not available_files:
            raise FileNotFoundError(f"No txt files found in {prompts_dir}")

        # If specific topics are requested, filter for those topics
        files_to_load = {}
        if topics:
            for topic in topics:
                if topic in available_files:
                    files_to_load[topic] = available_files[topic]
                else:
                    print(f"Warning: Requested topic '{topic}' not found in prompts directory")
        else:
            files_to_load = available_files

        # Load the files
        for topic, file_path in files_to_load.items():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    prompts[topic] = f.read().strip()
            except Exception as e:
                print(f"Error reading file {file_path}: {str(e)}")
                continue
        if len(prompts) == 0:
            if 'Current Market State' in available_files:
                return self.load_prompts(['Current Market State'])
        return prompts

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
    pq = ParallelQuestions("Federated GraphQl",
                           job=Job.create(),
                           topics=['ai_use_cases', 'growth_projection']
                           )
    answers = await pq.ask_all()
    for prompt, response in answers:
        print(f"*{prompt}*:\n{response}\n")


if __name__ == "__main__":
    asyncio.run(main())
