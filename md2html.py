# The function should handle Markdown with yaml metadata, including the repository URL and command-style formatting


import markdown
import re
import yaml

def convert_markdown_to_html(markdown_file_path, html_output_path=None):
    """
    Convert a Markdown file to HTML with special handling for YAML metadata
    
    Parameters:
    markdown_file_path (str): Path to the Markdown file to convert
    html_output_path (str, optional): Path where the HTML file should be saved.
                                      If None, returns the HTML as a string.
    
    Returns:
    str: HTML content if html_output_path is None, otherwise None
    """
    try:
        # Read the markdown file
        with open(markdown_file_path, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()
        
        # Check for YAML frontmatter
        metadata = {}
        yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
        yaml_match = yaml_pattern.match(md_content)
        
        if yaml_match:
            yaml_text = yaml_match.group(1)
            try:
                metadata = yaml.safe_load(yaml_text)
                # Remove the YAML frontmatter from the markdown content
                md_content = md_content[yaml_match.end():]
            except yaml.YAMLError as e:
                print(f"Warning: Failed to parse YAML frontmatter: {e}")
        
        # Process command examples (lines starting with '>')
        cmd_pattern = re.compile(r'^> (.+?)$\n?(.*?)(?=\n> |\n\n|\n?$)', re.DOTALL | re.MULTILINE)
        
        def cmd_replacer(match):
            cmd = match.group(1).strip()
            description = match.group(2).strip()
            return f'<div class="command">{cmd}</div>\n<p class="explanation">{description}</p>\n'
        
        md_content = cmd_pattern.sub(cmd_replacer, md_content)
        
        # Convert markdown to HTML
        html_body_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])
        
        # Generate the HTML with the template
        html_output = generate_html_template(html_body_content, metadata)
        
        # If output path is provided, write to file
        if html_output_path:
            with open(html_output_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_output)
            return None
        else:
            return html_output
            
    except FileNotFoundError:
        print(f"Error: File '{markdown_file_path}' not found.")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise

def generate_html_template(body_content, metadata=None):
    """
    Generate HTML using template with optional metadata handling.
    
    Parameters:
    body_content (str): Converted markdown content
    metadata (dict): Metadata from YAML frontmatter
    
    Returns:
    str: Complete HTML document
    """
    # Extract metadata if available
    tags_html = ""
    related_html = ""
    repo_html = ""
    
    if metadata and 'tags' in metadata:
        tags = metadata.get('tags', [])
        if tags:
            for tag in tags:
                tags_html += f'<div class="tag">{tag}</div>\n'
    
    if metadata and 'related' in metadata:
        related = metadata.get('related', [])
        if related:
            for item in related:
                related_html += f'<div class="related-item">{item}</div>\n'
    
    if metadata and 'repo' in metadata:
        repo_url = metadata.get('repo')
        if repo_url:
            repo_html = f'<div class="repo-link"><a href="{repo_url}" target="_blank">Repository: {repo_url}</a></div>\n'
    
    # Determine if we need the metadata table
    has_metadata = bool(tags_html or related_html)
    
    metadata_table = ""
    if has_metadata:
        metadata_table = f"""
    <table class="metadata-table">
        <tr>
            <th style="width: 50%">tags</th>
            <th style="width: 50%">related</th>
        </tr>
        <tr>
            <td>
                <div class="tags-container">
                    {tags_html}
                </div>
            </td>
            <td>
                <div class="related-container">
                    {related_html}
                </div>
            </td>
        </tr>
    </table>
    """
    
    # Create the full HTML document
    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Html</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.5;
            max-width: 100%;
            margin: 0;
            padding: 0;
        }}
        .metadata-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        .metadata-table th {{
            text-align: center;
            font-size: 24px;
            padding: 10px;
            border: 1px solid #e0e0e0;
            font-weight: normal;
        }}
        .tags-container, .related-container {{
            display: flex;
            flex-wrap: wrap;
            padding: 10px;
        }}
        .tag, .related-item {{
            margin: 5px;
            padding: 10px 20px;
            border: 1px solid #e0e0e0;
            display: inline-block;
        }}
        h1 {{
            font-size: 48px;
            margin-top: 30px;
            margin-bottom: 20px;
            font-weight: normal;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e0e0e0;
            margin: 20px 0;
        }}
        .content {{
            padding: 0 20px;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 4px;
            font-family: monospace;
            border-radius: 3px;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 10px;
            margin: 10px 0;
            font-family: monospace;
            border-left: 4px solid #e0e0e0;
            overflow-x: auto;
        }}
        .command {{
            background-color: #f5f5f5;
            padding: 10px;
            margin: 10px 0;
            font-family: monospace;
            border-left: 4px solid #e0e0e0;
            white-space: pre;
        }}
        .explanation {{
            margin: 10px 0 20px 0;
        }}
        .emphasis {{
            font-style: italic;
        }}
        .repo-link {{
            margin: 20px 0;
            padding: 10px;
            background-color: #f8f8f8;
            border-radius: 4px;
        }}
        .repo-link a {{
            color: #0366d6;
            text-decoration: none;
        }}
        .repo-link a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    {metadata_table}
    <div class="content">
        {repo_html}
        {body_content}
    </div>
</body>
</html>"""
    
    return html_template
