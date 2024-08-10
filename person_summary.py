from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile
from typing import Tuple
from agents.linkedin_lookup_page import *
from third_parties.linkedin import scrape_linkedin_profile
from tools.output_parser import summary_parser, Summary
import json


def look_up_person(name: str) -> Tuple[Summary, str]:
    linkedin_profile_url = "https://gist.githubusercontent.com/IllFil/8076d38078a3a69606c2a77d449b9f04/raw/295c506af9caff06480976de943a5c919519aa6a/mylinkedin.json"
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url, mock=True)
    summary_template = """Given the following information about a person from LinkedIn: {information}, I would like you to generate:

1. A concise summary of the person's qualifications and experience.
2. Two specific facts about the person.
3. A list of topics that may be of interest to the person.


Do not include any additional information or details beyond this format.

        \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOllama(model="llama3.1")

    chain = summary_prompt_template | llm | summary_parser

    try:
        res = chain.invoke(input={"information": linkedin_data})
        profile_pic_url = linkedin_data.get("profile_pic_url")
        return res, profile_pic_url

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None


if __name__ == "__main__":
    look_up_person("Illia Filipas Linkedin")
