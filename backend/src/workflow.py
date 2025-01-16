from ai import PerplexityWrapper, ChatGPTWrapper
from overview import ParallelQuestions
from job import Job, Status
from typing import List
import harmonic_requests


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

    async def get_table_enterprise(self):
        enterprise_domains = await harmonic_requests.find_enterprises(self.search_term, self.perplexity)
        self.enterprise_companies = harmonic_requests.enrich_company_list(enterprise_domains)
        return enterprise_domains

    async def get_table_startup(self):
        startup_domains = await harmonic_requests.find_top_startups(self.search_term, self.perplexity)
        self.startup_companies = harmonic_requests.enrich_company_list(startup_domains)
        return self.startup_companies

    async def get_table_webvisits(self):
        self.startup_yearly_webtraffic = harmonic_requests.combine_yearly_webtraffic(self.startup_companies)
        self.enterprise_yearly_webtraffic = harmonic_requests.combine_yearly_webtraffic(self.enterprise_companies)
        return self.enterprise_yearly_webtraffic

    async def get_table_employees_total(self):
        self.startup_yearly_headcount = harmonic_requests.combine_yearly_metrics(self.startup_companies)
        self.enterprise_yearly_headcount = harmonic_requests.combine_yearly_metrics(self.enterprise_companies)
        return self.enterprise_yearly_headcount

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
