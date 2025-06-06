import markdown

def convert_markdown_to_html(md_text: str) -> str:
    return markdown.markdown(md_text)