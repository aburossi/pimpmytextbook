import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from utils.schema import LessonPlan
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def generate_guidelines(inputs):
    # Prepare parser for schema validation
    parser = PydanticOutputParser(pydantic_object=LessonPlan)

    # Load system prompt
    with open("prompts/didactic_guidelines.txt", encoding="utf-8") as f:
        system_template = f.read()

    format_instructions = parser.get_format_instructions()

    system_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_prompt = HumanMessagePromptTemplate.from_template(
        "Kapitel:\n{chapter}\n\nNutzerinput:\n{user_input}\n\n{format_instructions}"
    )

    prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    messages = prompt.format_messages(
        chapter=inputs["chapter"],
        user_input=inputs["user_input"],
        format_instructions=format_instructions
    )

    # Invoke model
    model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2, max_tokens=13000)
    result = model.invoke(messages)

    # Parse output to schema
    lesson_plan = parser.parse(result.content)
    json_string = lesson_plan.model_dump_json(indent=2, ensure_ascii=False, by_alias=True)

    return json_string, lesson_plan
