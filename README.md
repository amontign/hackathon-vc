# Ultimate Market Research VC Tool 

![alt text](https://i.imgur.com/O8vZHPM.png)

> This project was built as part of the Data-Driven VC Hackathon organized by [Red River West](https://redriverwest.com) & [Bivwak! by BNP Paribas](https://bivwak.bnpparibas/)

## Demo

Go to https://hack25mr.rdp.vc and check how it works!

## How to deploy locally

1. Create `.env` file `cp .env.example .env`
2. Fill the [OpenAI API key](https://platform.openai.com/api-keys) and [Perplexity API key](https://www.perplexity.ai/settings/api)
3. Run `docker compose build` and `docker compose up`
4. Visit https://localhost:30012

## Docs
- Backend: https://localhost:30011/docs or https://api.hack25mr.rdp.vc/docs

## Checklist

#### Code modules
- [x]  GitHub Repo
- [x]  .env 
- [ ]  description
- [x]  Perplexity API wrapper
- [ ]  Harmonic wrapper
- [ ]  Harmonic export to gpt input
- [x]  docker-compose: python + frontend
- [x]  deploy
- [ ]  recheck whether everything exists in the result
- [x]  prompts
- [ ]  fund specific metrics

#### Inputs / data

- [x]  Overview prompts
- [ ]  Final prompt

#### QA

- [ ]  Find 10 examples topics and test them

#### Security

- [ ]  Session auth
- [ ]  OpenAI Key / Local Key saving to the session

## Nice to add

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