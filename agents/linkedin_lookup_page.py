import os

from langchain import hub
from langchain_ollama import ChatOllama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from tools.tools import get_profile_url_tavily


def look_up_about(name: str) -> str:

    if "name=" in name:
        name = name.split("=")[-1]
    llm = ChatOllama(
        model="llama3.1"
    )

    template = """
    Given the full name of a person as listed on their Public profile on LinkedIn , "{name_of_person}", your task is to search for the LinkedIn profile URL for this person. In your search query, include the phrase "Search for a public LinkedIn profile {name_of_person}".

    Requirements:
    1. The URL must contain "linkedin.com/in".
    2. Provide only the URL without any additional text or explanation.
    """

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="Searches for LinkedIn profile URLs. Use this to find LinkedIn profiles.",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)


    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    output = result["output"]
    return output






