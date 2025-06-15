from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI

def generate_output(prompt_type, didactic_guidelines, user_content):
    with open(f"prompts/{prompt_type}.txt", encoding="utf-8") as f:
        system_template = f.read()

    system_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_prompt = HumanMessagePromptTemplate.from_template(
        "Leitlinien:\n{guidelines}\n\nNutzerinput:\n{user_content}"
    )

    prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    messages = prompt.format_messages(guidelines=didactic_guidelines, user_content=user_content)

    model = ChatOpenAI(model_name="gpt-4o-mini")

    result = model.invoke(messages)
    with open(f"outputs/{prompt_type}.md", "w", encoding="utf-8") as f:
        f.write(result.content)

    return result.content
