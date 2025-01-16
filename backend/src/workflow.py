from ai import PerplexityWrapper, ChatGPTWrapper
from overview import ParallelQuestions
from job import Job, Status
from typing import List


class Workflow:
    def __init__(self,
                 search_term: str,
                 job: Job,
                 topics: List[str] = None,
                 search_type: str = None
                 ):
        self.job = job

        self.chat_gpt = ChatGPTWrapper()
        self.perplexity = PerplexityWrapper()

        self.search_term = search_term
        self.job.search_term = search_term
        self.search_type = search_type
        self.job.search_type = search_type
        self.topics = topics
        self.job.topics = topics

        self.term_type = None

        self.qa_pairs = []
        self.job.qa_pairs = self.qa_pairs

        self.summary = ""
        self.job.summary = self.summary

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

    async def step2(self):
        """
        Ask questions based on the term type and store the answers.
        """
        pqw = ParallelQuestions(self.search_term, self.job, self.topics)
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

    @staticmethod
    async def get_table_enterprise():
        return [
            {'name': 'MegaCorp', 'revenue': 5000000000, 'employees': 100000, 'website': 'https://www.megacorp.biz', 'founded': 1901},
            {'name': 'HyperGlobal Inc.', 'revenue': 12000000000, 'employees': 300000, 'website': 'https://www.hyperglobal.io', 'founded': 1888},
            {'name': 'Quantum Solutions', 'revenue': 2500000000, 'employees': 75000, 'website': 'https://www.qsolutions.ai', 'founded': 1982},
        ]

    @staticmethod
    async def get_table_startup():
        return [
            {'name': 'BananaTech', 'funding': 15000, 'employees': 2, 'website': 'https://www.bananatech.xyz', 'founded': 2023},
            {'name': 'HoverChair Co.', 'funding': 500000, 'employees': 12, 'website': 'https://www.hoverchair.io', 'founded': 2022},
            {'name': 'Unicornify', 'funding': 999999999, 'employees': 5, 'website': 'https://www.unicornify.lol', 'founded': 2021},
        ]

    @staticmethod
    async def get_table_webvisits():
        return {
            '18Q1': 20000,
            '18Q2': 30000,
            '18Q3': 40000,
            '18Q4': 50000,
            '19Q1': 60000,
            '19Q2': 80000,
            '19Q3': 100000,
            '19Q4': 120000,
            '20Q1': 150000,
            '20Q2': 180000,
            '20Q3': 220000,
            '20Q4': 250000,
            '21Q1': 300000,
            '21Q2': 350000,
            '21Q3': 380000,
            '21Q4': 400000,
            '22Q1': 450000,
            '22Q2': 500000,
            '22Q3': 550000,
            '22Q4': 600000,
            '23Q1': 650000,
            '23Q2': 700000,
            '23Q3': 780000,
            '23Q4': 850000,
            '24Q1': 900000,
            '24Q2': 950000,
            '24Q3': 980000,
            '24Q4': 1000000,
        }

    @staticmethod
    async def get_table_employees_total():
        return {
            '18Q1': 100000,
            '18Q2': 105000,
            '18Q3': 110000,
            '18Q4': 115000,
            '19Q1': 120000,
            '19Q2': 125000,
            '19Q3': 130000,
            '19Q4': 135000,
            '20Q1': 140000,
            '20Q2': 145000,
            '20Q3': 150000,
            '20Q4': 155000,
            '21Q1': 160000,
            '21Q2': 165000,
            '21Q3': 170000,
            '21Q4': 180000,
            '22Q1': 190000,
            '22Q2': 200000,
            '22Q3': 210000,
            '22Q4': 220000,
            '23Q1': 230000,
            '23Q2': 240000,
            '23Q3': 255000,
            '23Q4': 270000,
            '24Q1': 285000,
            '24Q2': 300000,
            '24Q3': 310000,
            '24Q4': 320000,
        }

    async def run(self) -> str:
        """
        Execute the entire workflow and return the markdown summary.
        """
        await self.step1()
        self.job.progress += 10
        self.job.message = f'Topic detected as {self.term_type}'
        print(self.job.message)
        self.job.table_startup = await self.get_table_startup()
        self.job.progress += 5
        self.job.table_enterprise = await self.get_table_enterprise()
        self.job.progress += 5
        self.job.chart_web_trend = await self.get_table_webvisits()
        self.job.progress += 5
        self.job.chart_headcount_trend = await self.get_table_employees_total()
        self.job.progress += 5
        await self.step2()
        self.job.progress += 50
        await self.step3()
        self.job.progress += 20
        self.job.state = Status.DONE
        self.job.result = self.summary
        print(self.summary)
        return self.summary


async def main():
    workflow = Workflow(search_term="Foundational GraphQL",
                        job=Job.create()
                        )
    result_markdown = await workflow.run()
    print(result_markdown)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
