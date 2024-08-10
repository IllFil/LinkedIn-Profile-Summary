from typing import List, Dict, Any
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
class Summary(BaseModel):
    summary: List[str] = Field(description="A concise summary of the person's qualifications and experience")
    facts: List[str] = Field(description="Two specific facts about the person")
    topics_of_interest: List[str] = Field(description="A list of topics that may be interesting for the person")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "facts": self.facts,
            "topics_of_interest": self.topics_of_interest
        }


summary_parser = PydanticOutputParser(pydantic_object=Summary)


