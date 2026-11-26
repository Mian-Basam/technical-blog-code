# CrewAI Research & Writing Crew

Companion code for the article **[Building an AI Application Using CrewAI](https://mian-basam.github.io/blog/building-an-ai-application-using-crewai/)**.

Three agents work in sequence to turn a topic into a fact-checked blog post:

| Agent | Job | Tools |
|---|---|---|
| Senior Technical Researcher | Gathers sourced facts | Web search (Serper) |
| Technical Content Writer | Drafts the post from the research | — |
| Technical Editor | Checks the draft against the research and tightens it | — |

## Setup

Requires Python 3.10–3.13, an [OpenAI API key](https://platform.openai.com/api-keys) and a free [Serper API key](https://serper.dev) for web search.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then add your keys
```

## Run

```bash
python crew_app.py "Python's asyncio library"
```

You'll see each agent's reasoning in the terminal. Results are saved to:

```text
output/research.md     research brief with sources
output/post.md         first draft
output/post-final.md   edited final post
```

## Customize

- **Change the model:** edit `LLM(model="gpt-4o-mini", ...)` in `crew_app.py`.
- **Change the output format:** edit each task's `expected_output`; it's the strongest lever on quality.
- **Add an agent:** define an `Agent` and a `Task` with `context=[...]`, then add both to the `Crew`.

Each run makes several LLM and search API calls, so keep an eye on usage.
