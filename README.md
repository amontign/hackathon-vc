# OneSearch - Ultimate Market Analysis Tool

![alt text](https://i.imgur.com/O8vZHPM.png)

> This project was built as part of the Data-Driven VC Hackathon organized by [Red River West](https://redriverwest.com) & [Bivwak! by BNP Paribas](https://bivwak.bnpparibas/)

### How to deploy locally

1. Create `.env` file `cp .env.example .env`
2. Fill the [OpenAI API key](https://platform.openai.com/api-keys), [Perplexity API key](https://www.perplexity.ai/settings/api) and [Harmonic API key](https://console.harmonic.ai/docs)
3. Run `make`
4. Visit https://localhost:30012

### Docs
- Backend: https://localhost:30011/docs

## Description

This repository contains the MVP of a product designed to analyze data from the internet and the Harmonic service to provide a comprehensive overview of specific markets or startups.

### How It Works
#### Input Selection
At the start, you can choose a company or market and select the questions you are interested in. These questions are passed to Perplexity, which searches the web, aggregates information from multiple articles, and provides detailed answers.

#### Question Customization
A default set of questions is available, but you can modify it by editing the relevant part of the code. This allows you to tailor the analysis to your specific needs.

#### Market Insights
- For selected markets, we identify top companies, startups, and enterprises using Perplexity.
- We gather metrics about these companies and compile a list of potentially interesting startups worth exploring.

#### Trend Analysis
- Employee counts of relevant companies.
- Website visits, reflecting market activity and momentum.

#### Data Aggregation
All collected insights are synthesized using GPT and displayed on the front-end for an easy-to-read summary.

## How to Contribute
This project is open for contributions! Here’s how you can help:

1. Add New Questions
   - Navigate to the backend-source-prompts-overview folder. 
   - Create a new text file named after your topic. 
   - Add the relevant prompt
   - The prompt will automatically be included in the build process.
2. Enhance Harmonic Data Usage
   - Add more fields from the Harmonic dataset. 
   - Improve how the data is visualized in the reports.

## Checklist

#### Code modules
- [x]  GitHub Repo
- [x]  .env 
- [x]  description
- [x]  Perplexity API wrapper
- [x]  Harmonic wrapper
- [x]  Harmonic export to gpt input
- [x]  docker-compose: python + frontend
- [x]  deploy
- [x]  recheck whether everything exists in the result
- [x]  prompts
- [ ]  fund specific metrics
- [x]  questions checkboxes
- [x]  table of the startups and enterprises
- [x]  trend chart
- [ ]  source links

#### Inputs / data

- [x]  Overview prompts
- [x]  Final prompt

#### QA

- [x]  Find 10 examples topics and test them

#### Security

- [ ]  Session auth
- [ ]  OpenAI Key / Local Key saving to the session

#### Nice to add

- [ ]  Fund custom questions

## Authors
- [Gareth Carless - Atomico](https://www.linkedin.com/in/garethcarless/)
- [Eugene Chernyavsky - Runa Capital](https://www.linkedin.com/in/evgeniy-chernyavskiy/)
- [Stevenson Jossaint - Developer - 42](https://www.linkedin.com/in/stevenson-jossaint/)
- [Alban Montigny - Developer - 42](https://www.linkedin.com/in/alban-montigny/)
- [Martin Naturel - Bpifrance](https://www.linkedin.com/in/martin-naturel-459270130/)
- [Thomas Prudhomme - Bpifrance](https://www.linkedin.com/in/thomasprudhomme/)
- [Thomas Rocher - Bpifrance](https://www.linkedin.com/in/thomas-rocher-bpifrance/)
- [Thomas Willson - Partech Partners](https://www.linkedin.com/in/thomas-willson-5a8b31207/)
- [Daniel Zhou - Data Scientist - Télécom Paris](https://www.linkedin.com/in/zhou-daniel/)