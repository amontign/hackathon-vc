from ai import PerplexityWrapper, ChatGPTWrapper
from overview import ParallelQuestions
from job import Job, Status

class Workflow:
    def __init__(self, search_term: str):
        self.search_term = search_term
        self.chat_gpt = ChatGPTWrapper()
        self.perplexity = PerplexityWrapper()
        self.term_type = None
        self.qa_pairs = []
        self.summary = ""

    async def step1(self):
        """
        Determine if the search term is a company or a market topic
        using ChatGPTWrapper (two variants only).
        """
        prompt = (
            f"Given the term '{self.search_term}', is it a company name "
            "or a market topic? Answer with only 'company' or 'market'."
        )
        response = await self.chat_gpt.get_answer(role="system", question=prompt)
        self.term_type = response.strip().lower()  # 'company' or 'market'

    async def step2(self, job: Job):
        """
        Ask questions based on the term type and store the answers.
        """
        pqw = ParallelQuestions(self.search_term, job)
        answ = await pqw.ask_all()
        self.qa_pairs += answ

    async def step3(self):
        """
        Combine all questions + answers and ask ChatGPT for a summary (markdown).
        """
        combined_qa = "\n".join(
            [f"**Q**: {item[0]}\n**A**: {item[1]}" for item in self.qa_pairs]
        )
        final_prompt = (
            "Summarize the following questions and answers in a concise way:\n\n"
            f"{combined_qa}"
        )
        self.summary = await self.chat_gpt.get_answer(role="system", question=final_prompt)
        # Format the summary in Markdown
        self.summary = f"# Summary\n\n{self.summary}"

    async def run(self, job: Job) -> str:
        """
        Execute the entire workflow and return the markdown summary.
        """
        await self.step1()
        job.progress = 10
        job.message = f'Topic detected as {self.term_type}'
        print(job.message)
        await self.step2(job)
        job.progress = 70
        await self.step3()
        job.progress = 100
        job.state = Status.DONE
        job.result = self.summary
        print(self.summary)
        return self.summary


async def main():
    workflow = Workflow(search_term="Foundational GraphQL")
    result_markdown = await workflow.run(Job.create())  # Assuming run() is now async
    print(result_markdown)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
