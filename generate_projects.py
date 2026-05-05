# generate_projects.py
# importing portfolio container from data.py
from data import portfolio

# calling export_qmd() on the Portfolio instance
# this method encapsulates all file-writing logic inside the Portfolio class
# each project's render_markdown() is called differently depending on type (polymorphism)
portfolio.export_qmd("generated_projects.qmd")