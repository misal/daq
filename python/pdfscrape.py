import fitz  # PyMuPDF
import os
import json
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def parse_fanfic_text(raw_text):
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    
    # Naive parsing — assumes structure like:
    # Line 0: Title
    # Line 1: Author
    # Lines 2-3: Summary or metadata
    # Rest: Story

    title = lines[0] if len(lines) > 0 else "Untitled"
    author = lines[1] if len(lines) > 1 else "Unknown"
    summary = lines[2] if len(lines) > 2 else ""
    
    # Try to extract tags, ships, etc. from summary line (naively)
    tags = []
    ships = []
    characters = []
    
    if "Tags:" in summary:
        tags = [t.strip() for t in summary.split("Tags:")[1].split(",")]

    story_text = "\n".join(lines[3:])

    return {
        "title": title,
        "author": author,
        "summary": summary,
        "tags": tags,
        "ships": ships,
        "characters": characters,
        "text": story_text,
        "word_count": len(story_text.split())
    }

def convert_folder_to_json(input_folder, output_jsonl):
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    
    with open(output_jsonl, 'w', encoding='utf-8') as out_file:
        for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
            pdf_path = os.path.join(input_folder, pdf_file)
            raw_text = extract_text_from_pdf(pdf_path)
            fanfic_data = parse_fanfic_text(raw_text)
            json_line = json.dumps(fanfic_data, ensure_ascii=False)
            out_file.write(json_line + "\n")

# --- Usage ---
input_folder = "path/to/your/pdf/fanfics"
output_jsonl = "fanfiction_dataset.jsonl"

convert_folder_to_json(input_folder, output_jsonl)
