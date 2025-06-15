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
    with open("prompts/didactic_guidelines.txt", encoding="utf-8") as f:
        system_template = f.read()

    print("[DEBUG] Template preview:", system_template[:300])
    print("[DEBUG] Inputs received:", inputs.keys())

    system_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_prompt = HumanMessagePromptTemplate.from_template(
        "Kapitel:\n{chapter}\n\nNutzerinput:\n{user_input}"
    )

    prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    messages = prompt.format_messages(**inputs)

    model = ChatOpenAI(model_name="gpt-4o-mini")

    result = model.invoke(messages)
    with open("outputs/guidelines_output.md", "w", encoding="utf-8") as f:
        f.write(result.content)

    return result.content

    with open("prompts/didactic_guidelines.txt") as f:
        template = f.read()

    print("[DEBUG] Template keys required:", template[:300])
    print("[DEBUG] Inputs received:", inputs.keys())

    prompt = PromptTemplate.from_template(template)
    model = ChatOpenAI(model_name="gpt-4o-mini")

    try:
        formatted_prompt = prompt.format(**inputs)
    except KeyError as e:
        raise ValueError(f"Missing key for template: {e}")

    with open("outputs/debug_prompt_guidelines.txt", "w") as f:
        f.write(formatted_prompt)

    result = model.invoke(formatted_prompt)
    with open("outputs/guidelines_output.md", "w") as f:
        f.write(result.content)
    return result.content

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
