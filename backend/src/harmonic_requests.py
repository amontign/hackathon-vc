import os
import httpx
from ai import PerplexityWrapper
import re

def extract_yearly_metrics(metrics):
    yearly_metrics = {}
    
    # Sort metrics by timestamp in descending order
    sorted_metrics = sorted(metrics, key=lambda x: x["timestamp"], reverse=True)
    
    # Track years we've seen
    seen_years = set()
    
    # Get first value for each year from 2020 onwards
    for metric in sorted_metrics:
        timestamp = metric["timestamp"]
        year = timestamp[:4]  # Extract year from timestamp
        
        if int(year) >= 2020 and year not in seen_years:
            yearly_metrics[year] = metric["metric_value"]
            seen_years.add(year)

    return yearly_metrics

async def get_company(domain):
    """
        Starting point for a startup specific search, returning key info about the company

        Input: Domain of the company
        Output: Harmonic company object with relevant fields
    """
    url = "https://api.harmonic.ai/companies"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers={
                "accept": "application/json",
                "apikey": os.getenv("HARMONIC_API_KEY")
            },
            params={"website_domain": domain}
        )
        response = response.json()

    try:
        company_output = {}
        company_output["entity_urn"] = response["entity_urn"]
        company_output["id"] = response["id"]
        company_output["website"] = response["website"]["domain"]
        company_output["customer_type"] = response["customer_type"]
        company_output["name"] = response["name"]
        company_output["description"] = response["description"]
        company_output["founding_date"] = response["founding_date"]["date"]
        company_output["headcount"] = response["headcount"]
        company_output["ownership_status"] = response["ownership_status"]
        company_output["company_type"] = response["company_type"]
        company_output["stage"] = response["stage"]
        company_output["location"] = response["location"]["country"]
        company_output["funding_total"] = response["traction_metrics"]["funding_total"]["14d_ago"]["value"]
        company_output["headcount"] = response["traction_metrics"]["headcount"]
        company_output["web_traffic"] = response["traction_metrics"]["web_traffic"]
    except:
        return None
    
    # Extract yearly headcount metrics
    headcount_metrics = company_output["headcount"]["metrics"]
    company_output["yearly_headcounts"] = extract_yearly_metrics(headcount_metrics)

    # Extract yearly web traffic metrics
    web_traffic_metrics = company_output["web_traffic"]["metrics"]
    company_output["yearly_web_traffic"] = extract_yearly_metrics(web_traffic_metrics)

    # Remove the main headcount field since we have the detailed yearly breakdown
    del company_output["headcount"]
    return company_output

def extract_domains(response):
    # Extract domains from the response using regex
    domains = re.findall(r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,})', response)
    
    # Clean up domains and remove duplicates while preserving order
    cleaned_domains = []
    seen = set()
    for domain in domains:
        # Strip any www. or protocol prefixes
        clean_domain = re.sub(r'^(?:https?://)?(?:www\.)?', '', domain)
        if clean_domain not in seen:
            cleaned_domains.append(clean_domain)
            seen.add(clean_domain)

    return list(seen)

async def enrich_company_list(company_list):
    """
        Enrich a list of startups or enterprises with Harmonic data

        Input: List of company domains
        Output: List of Harmonic company objects with relevant fields
    """
    company_data = [await get_company(domain) for domain in company_list]
    company_data = [company for company in company_data if company is not None]
    return company_data
    

async def find_top_startups(market_description, perplexity: PerplexityWrapper):
    prompt = f"""
        Given the following market description / company name, find the top startups in this market.
        Return a list of up to 10 website addresses of the companies.

        Market Description / Company name: {market_description}
    """
    answer = await perplexity.get_answer("user", prompt)
            
    return extract_domains(answer)

async def find_enterprises(market_description, perplexity: PerplexityWrapper):
    prompt = f"""
        Given the following market description / company name, find the top 10 enterprise or incumbents in this market.
        Return a list of up to 10 website addresses of the companies.

        Market Description / Company name: {market_description}
    """
    answer = await perplexity.get_answer("user", prompt)
    return extract_domains(answer)

async def combine_yearly_metrics(company_list):
    yearly_headcount = {}

    # Sum yearly headcount and webtraffic for startups
    for company in company_list:
        if 'yearly_headcounts' in company:
            for year, count in company['yearly_headcounts'].items():
                yearly_headcount[year] = yearly_headcount.get(year, 0) + count

    return yearly_headcount

async def combine_yearly_webtraffic(company_list):
    yearly_webtraffic = {}

    for company in company_list:
        if 'yearly_web_traffic' in company:
            for year, traffic in company['yearly_web_traffic'].items():
                yearly_webtraffic[year] = yearly_webtraffic.get(year, 0) + traffic

    return yearly_webtraffic


