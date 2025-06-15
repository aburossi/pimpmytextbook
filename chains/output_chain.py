from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def generate_output(prompt_type, didactic_guidelines, user_content):
    with open(f"prompts/{prompt_type}.txt") as f:
        template = f.read()

    prompt = PromptTemplate.from_template(template)
    model = ChatOpenAI(model_name="gpt-4o-mini")

    inputs = {"guidelines": didactic_guidelines, "user_content": user_content}
    formatted_prompt = prompt.format(**inputs)

    with open(f"outputs/debug_prompt_{prompt_type}.txt", "w") as f:
        f.write(formatted_prompt)

    result = model.invoke(formatted_prompt)
    with open(f"outputs/{prompt_type}.md", "w") as f:
        f.write(result.content)
    return result.content
