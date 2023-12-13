HEADING = """
<html>

<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-7V0GZ7SX71"></script>
    <script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-7V0GZ7SX71');</script>

    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>algorithmas</title>
    <link rel="icon" href="/assets/images/icons/tabicon.png">

    <!-- Mathjax Rendering -->
    <div id="mathrendering">
        <script> MathJax = { tex: { inlineMath: [['$', '$'], ['\\\(', '\\\)']] }, }; </script>
        <!-- (we will render mathjax after loading all dynamic elements) -->
        <!-- <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script> -->
    </div>

    <!-- Google Code prettifier -->
        <script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js"></script>

    <link rel="stylesheet" type="text/css" href="/css/main.css">
</head>


<body>

<div id="wrapper">

    <div class="header">
        <h1 id="title" ><a href="/">algorithmas</a></h1>
        <div id="navbar">
            <a href="/about.html">About</a>
            <a href="/articles.html">Articles</a>
        </div>
    </div>

<div class="article" id="article">

<div class="contents" id="table-of-contents">
    <!-- This will be the table of contents -->
</div>
<script src="/js/sections.js"></script>
<div class="article-content" id="article-content">
"""

ENDING = """
    <script>
    setTimeout(() => {
        var script = document.createElement('script');
            script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
            script.id = "MathJax-script";
            script.async = true;
            document.getElementById('mathrendering').appendChild(script);
    }, 1)
    </script>
</div>
</div>
</body>
"""


"""
if __name__ == "__main__":
    markdown_file_path = "./knapsack_optimization.md"
    
    with open(markdown_file_path, "r") as markdown_file:
        markdown_content = markdown_file.read()
        
    article_content = convert_markdown_to_html(markdown_content)
    
    with open("output.html", "w") as output_file:
        output_file.write(HEADING + article_content + ENDING)
"""

import markdown
import os
import re

# Convert a markdown file (input_file) to the html page
def convert_markdown_to_html(input_file):

    def obsidian_to_python_admonition(match):
        adType, adTitle, adSuffix, adContent = match.group(1)[1:], match.group(3), match.group(2), match.group(4)
        adContent = "\n".join([line.replace(">", "\t", 1) for line in adContent.split("\n")])
        adContent = admonitions_convert(adContent)

        return f'???{adSuffix} {adType} "{adTitle}" \n {adContent} \n'

    
    # Convert obsidian admonitions to python admonitions
    def admonitions_convert(content):
        pattern = r'>\s*\[(.*?)\](.)\s*(.*?)\n((?:\s?>.*\n)*)'
        content = re.sub(pattern, obsidian_to_python_admonition, content)
        return content

    def code_block_replacement(match):
        s = '<div class="box"><pre class="prettyprint"><code class="language-{0}">'.format(match.group(1))
        code = match.group(2).replace("<", "&lt").replace(">", "&gt")
        e = "</code></pre></div>"
        return s + code + e

    def section_id_fill(match):
        s = match.group(1)[:-1] + ' id="{0}"'.format(match.group(2)) + '>'
        title = match.group(2)
        e = match.group(4)
        return s + title + e

    def latex_replace(match):
        s = match.group(0)
        return s.replace("\\", "\\\\").replace("_", "\\_").replace("*", "\\*").replace("[", "\[").replace("]", "\]");

    content = input_file.read()


    # Change the admonition syntax so it matches the expected syntax in the markdown.markdown() function
    content = admonitions_convert(content)

    # Replace code sections with appropriate html
    pattern = r'```\s?(\w+)\n((.|\n)*?)```'
    content = re.sub(pattern, code_block_replacement, content)

    # Replace in-line Latex segments
    pattern = r'\$(.|\n)*?\$'
    content = re.sub(pattern, latex_replace, content)

    # Replace display Latex segments
    # \$\$(.|\n)*?\$\$
    pattern = r'\$\$(.|\n)*?\$\$'
    content = re.sub(pattern, latex_replace, content)

    # Convert markdown to html
    html_content = HEADING + markdown.markdown(content, extensions=['pymdownx.details', 'footnotes']) + ENDING

    # Add ids to each section (for linking in the sections)
    pattern = r'(<h\d>)((\w|.)+)(</h\d>)'
    html_content = re.sub(pattern, section_id_fill, html_content)

    return html_content

# Iterate throught all the files in input_dir and for each .md file render a .html file inside output_dir
def convert_md_files(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for name in files:
            if name.endswith('.md'):
                print(name, end=':\n\t')
                file_path = os.path.join(root, name)
                output_path = os.path.join(output_dir, name[:-3] + ".html")
                with open(file_path, 'r') as input_file:
                    with open(output_path, 'w+') as output_file:
                        print('{0} -> {1}'.format(input_file.name, output_file.name))
                        output_file.write(convert_markdown_to_html(input_file))

if __name__ == "__main__":
    input_directory = 'articles-src'
    output_directory = 'articles'

    convert_md_files(input_directory, output_directory)

# THIS SCRIPT SHOULD BE RUN INSIDE THE ROOT DIRECTORY OF THE SERVER (so that posts/(..) are valid directories)