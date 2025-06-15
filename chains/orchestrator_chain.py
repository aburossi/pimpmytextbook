import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def generate_guidelines(inputs):
    # Prepare parser for schema validation
    parser = PydanticOutputParser(pydantic_object=LessonPlan)

    # Load template text
    with open("prompts/didactic_guidelines.txt", encoding="utf-8") as f:
        system_template = f.read()

    print("[DEBUG] Template preview:", system_template[:300])
    print("[DEBUG] Inputs received:", inputs.keys())

    # Include parser format instructions
    format_instructions = parser.get_format_instructions()

    # Use format_instructions in human message
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

    # Model
    model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2, max_tokens=13000)

    result = model.invoke(messages)

    # Parse into validated schema object
    lesson_plan = parser.parse(result.content)

    # Save raw JSON (pretty-printed)
    import json
    with open("outputs/guidelines_output.json", "w", encoding="utf-8") as f:
        json.dump(lesson_plan.dict(by_alias=True), f, ensure_ascii=False, indent=2)

    return json.dumps(lesson_plan.dict(by_alias=True), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    from utils.file_loader import load_textbook, load_user_content

    chapter = load_textbook()
    user_input = load_user_content()

    combined_inputs = {
        "chapter": chapter,
        "user_input": user_input
    }

    result = generate_guidelines(combined_inputs)
    print("\n[DEBUG] Final Result:\n", result[:1000])
    print("[DEBUG] Loaded chapter content preview:", chapter[:500])
    print("[DEBUG] Loaded user_input preview:", user_input[:500])
