import markdown2
import subprocess
import os

def convert_markdown(md_text, out_html="outputs/output.html", out_docx="outputs/output.docx"):
    # Convert markdown to HTML
    html = markdown2.markdown(md_text)

    # Save HTML version
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)

    # Save raw Markdown to temporary file
    temp_md_path = "outputs/temp_input.md"
    with open(temp_md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    # Use Pandoc to convert to DOCX
    result = subprocess.run(
        ["pandoc", temp_md_path, "-o", out_docx],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Pandoc error:", result.stderr)
    else:
        print(f"DOCX saved to {out_docx}")
