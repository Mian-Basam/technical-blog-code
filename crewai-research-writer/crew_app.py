"""Research -> write -> edit pipeline built with CrewAI.

Usage:
    python crew_app.py "Python's asyncio library"
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from crewai import LLM, Agent, Crew, Process, Task  # noqa: E402
from crewai_tools import SerperDevTool  # noqa: E402

llm = LLM(model="gpt-4o-mini", temperature=0.3)
search_tool = SerperDevTool()

# ---------- Agents ----------

researcher = Agent(
    role="Senior Technical Researcher",
    goal="Find accurate, current and well-sourced information about {topic}",
    backstory=(
        "You are a meticulous researcher who has spent years evaluating "
        "developer tools. You prefer official documentation and primary "
        "sources, and you always note where each fact came from."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Technical Content Writer",
    goal="Turn research into a clear, engaging blog post about {topic}",
    backstory=(
        "You are a former computer science lecturer who now writes for "
        "developers. You explain ideas with concrete examples and never "
        "invent facts that aren't in the research you were given."
    ),
    llm=llm,
    verbose=True,
)

editor = Agent(
    role="Technical Editor",
    goal="Make sure the post about {topic} is accurate, clear and well structured",
    backstory=(
        "You are a strict editor. You cross-check every claim in a draft "
        "against the research brief and remove anything unsupported."
    ),
    llm=llm,
    verbose=True,
)

# ---------- Tasks ----------

research_task = Task(
    description=(
        "Research {topic}. Cover what it is, the problem it solves, "
        "key features, a simple usage example and notable limitations. "
        "Use web search and prefer official sources."
    ),
    expected_output=(
        "A structured research brief with 5-8 bullet-point findings, "
        "each followed by its source URL."
    ),
    agent=researcher,
    output_file="output/research.md",
)

writing_task = Task(
    description=(
        "Using the research brief, write a beginner-friendly blog post "
        "about {topic}. Include an introduction, 3-4 sections with "
        "headings, one code example if relevant, and a short conclusion."
    ),
    expected_output="A complete blog post in Markdown, 600-900 words.",
    agent=writer,
    context=[research_task],
    output_file="output/post.md",
)

editing_task = Task(
    description=(
        "Review the draft blog post against the research brief. Fix "
        "factual errors, remove unsupported claims, tighten wordy "
        "sentences and keep the Markdown formatting."
    ),
    expected_output="The final, edited blog post in Markdown.",
    agent=editor,
    context=[research_task, writing_task],
    output_file="output/post-final.md",
)

# ---------- Crew ----------

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True,
)


def main() -> None:
    topic = " ".join(sys.argv[1:]) or "Python's asyncio library"
    Path("output").mkdir(exist_ok=True)
    result = crew.kickoff(inputs={"topic": topic})
    print("\n=== FINAL POST ===\n")
    print(result.raw)
    print("\nSaved: output/research.md, output/post.md, output/post-final.md")


if __name__ == "__main__":
    main()
