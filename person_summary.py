from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_page import *
from third_parties.linkedin import scrape_linkedin_profile
from tools.output_parser import summary_parser
import json
def look_up_person(name: str) -> str:
    # linkedin_profile_url = look_up_about(name)
    linkedin_profile_url = "https://gist.githubusercontent.com/IllFil/8076d38078a3a69606c2a77d449b9f04/raw/295c506af9caff06480976de943a5c919519aa6a/mylinkedin.json"
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url, mock=True)
    summary_template = """You are virtual assistant that must analyse information given about a person that are 
    provided in json format {information}, and after analysing given information give as a response two lines with: 
    1. A short summary 2. two facts about them

        Use information from Linkedin
        \n{format_instructions}
        """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOllama( model="llama3.1")

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data})

    print(res)

    try:
        res = chain.invoke(input={"information": linkedin_data})
        print("Raw result from chain.invoke:")
        print(res)

        # Parse and handle the result
        return res
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        # Handle error, e.g., return a default value or raise an exception
        return "Failed to parse the output. Please check the data and try again."
if __name__ == "__main__":
    look_up_person("Illia Filipas Linkedin")




