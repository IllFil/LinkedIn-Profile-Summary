from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile

var = True
if var == True:

    print("Hello User")
    summary_template = """given the information {information} about a person: 1.Short summary 2.Any contact information"""

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOllama(model="llama3")
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url= "https://gist.githubusercontent.com/IllFil/8076d38078a3a69606c2a77d449b9f04/raw/2f4d5934251e525844c3440069a2311bc8968acf/mylinkedin.json"
    )
    chain = summary_prompt_template | llm | StrOutputParser()
    res = chain.invoke(input={"information": linkedin_data})

    print(res)
