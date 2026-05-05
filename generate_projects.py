# importing project list
from data import projects

# opening file for writing generated content
with open("generated_projects.qmd", "w") as f:

    # writing page title
    f.write("# Projects\n\n")

    # looping through all projects
    for project in projects:

        # rendering each project and writing to file
        f.write(project.render_markdown())