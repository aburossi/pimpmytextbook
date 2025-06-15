from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI

def generate_guidelines(inputs):
    with open("prompts/didactic_guidelines.txt") as f:
        template = f.read()

    prompt = PromptTemplate.from_template(template)
    model = ChatOpenAI(model_name="gpt-4o-mini")

    formatted_prompt = prompt.format(**inputs)
    with open("outputs/debug_prompt_guidelines.txt", "w") as f:
        f.write(formatted_prompt)

    result = model.invoke(formatted_prompt)
    with open("outputs/guidelines_output.md", "w") as f:
        f.write(result.content)
    return result.content
