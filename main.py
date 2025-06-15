from utils.file_loader import load_textbook, load_user_content
from chains.orchestrator_chain import generate_guidelines
from chains.output_chain import generate_output
from utils.converter import convert_markdown
import json
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

    # Generate didactic guidelines
    didactic_guidelines = generate_guidelines(combined_inputs)

    # Save as markdown
    with open("inputs/didactic_guidelines.md", "w", encoding="utf-8") as f:
        f.write(didactic_guidelines)

    # (Optional) Parse to structured dict if JSON-like
    # For now we use the markdown text directly

    # Proceed to second step
    final_md = generate_output(
        prompt_type="lesson_unit",
        didactic_guidelines=didactic_guidelines,
        user_content=user_input
    )

    # Convert to .html and .docx
    convert_markdown(
        final_md,
        out_html="outputs/lesson_unit.html",
        out_docx="outputs/lesson_unit.docx"
    )
