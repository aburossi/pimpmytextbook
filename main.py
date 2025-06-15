from utils.file_loader import load_textbook, load_user_content
from chains.orchestrator_chain import generate_guidelines
from chains.output_chain import generate_output
from utils.converter import convert_markdown
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    # Load base inputs
    chapter = load_textbook()
    user_input = load_user_content()

    combined_inputs = {
        "chapter": chapter,
        "user_input": user_input
    }

    # Generate didactic guidelines (returns JSON string + parsed object)
    json_string, parsed_object = generate_guidelines(combined_inputs)

    # Save raw JSON and markdown version
    with open("outputs/guidelines_output.json", "w", encoding="utf-8") as f:
        f.write(json_string)

    with open("inputs/didactic_guidelines.md", "w", encoding="utf-8") as f:
        f.write(json_string)

    # Generate lesson unit markdown from the JSON string
    final_md = generate_output(
        prompt_type="lesson_unit",
        didactic_guidelines=json_string,
        user_content=user_input
    )

    # Convert to .html and .docx
    convert_markdown(
        final_md,
        out_html="outputs/lesson_unit.html",
        out_docx="outputs/lesson_unit.docx"
    )
