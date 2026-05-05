# data.py

# importing project classes
from models import DashboardProject, ProductProject, VisualProject, Project


# defining portfolio container class
class Portfolio:
    """Container class for all portfolio projects."""

    # initializing portfolio with owner name and empty project list
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self._projects = []

    # validating and setting owner name
    @property
    def owner_name(self):
        return self._owner_name

    @owner_name.setter
    def owner_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Owner name must be a non-empty string")
        self._owner_name = value.strip()

    # adding project to portfolio
    def add_project(self, project):
        # checking project type
        if not isinstance(project, Project):
            raise TypeError(f"Expected a Project instance, got {type(project).__name__}")
        self._projects.append(project)
        return self  # allowing method chaining

    # filtering projects by type (e.g. DashboardProject)
    def get_by_type(self, project_type):
        return [p for p in self._projects if isinstance(p, project_type)]

    # enabling iteration over portfolio
    def __iter__(self):
        return iter(self._projects)

    # returning number of projects
    def __len__(self):
        return len(self._projects)

    # returning debug representation
    def __repr__(self):
        return f"Portfolio(owner='{self.owner_name}', projects={len(self._projects)})"

    # exporting portfolio to qmd file
    def export_qmd(self, filepath="generated_projects.qmd"):
        with open(filepath, "w") as f:
            f.write(f"# {self.owner_name}'s Projects\n\n")
            for project in self._projects:
                f.write(project.render_markdown())
        print(f"Exported {len(self._projects)} projects to {filepath}")


# building portfolio instance
portfolio = Portfolio(owner_name="Alnura Abdyrova")


# adding dashboard project
portfolio.add_project(DashboardProject(
    title="Computer Games Industry Analysis",
    description="Analysis of gaming trends using Steam data",
    dataset="70,000+ games (2013–2025)",
    questions=[
        "How do real-world events affect gaming activity?",
        "What caused the rise of indie games?",
        "Do violent games follow real-world trends?"
    ],
    insights=[
        "Gaming activity increased during COVID-19",
        "Indie games grew after Steam policy changes",
        "Violent games remain consistently popular"
    ],
    tools=["Tableau", "Python"],
    dashboard_link="https://public.tableau.com/views/Book1_17653119185000/Dashboard3?:showVizHome=no&:embed=true"
))


# adding visual analysis project
portfolio.add_project(VisualProject(
    title="Democracy and Economic Perception",
    description="Do people judge democracy by GDP numbers or by how their wallet actually feels? "
                "Using World Values Survey data across 60+ countries, this study finds that "
                "subjective economic perception — not objective indicators like GDP or unemployment — "
                "is the only statistically significant predictor of satisfaction with democracy.",
    dataset="World Values Survey, World Bank, V-Dem — 88,499 respondents",
    questions=[
        "Do people judge democracy based on GDP or perception?",
        "Does democracy quality predict satisfaction?",
        "Which individual factors matter?"
    ],
    insights=[
        "Economic perception is the only significant predictor",
        "GDP and unemployment show no significant effect",
        "Older and more educated people report higher satisfaction",
        "Perception drives democratic legitimacy"
    ],
    tools=["Python", "pandas", "OLS Regression"],
    image_paths=[
        {"path": "images/dem_satisfaction_dist.png", "caption": "Distribution of Satisfaction"},
        {"path": "images/dem_econ_perception_dist.png", "caption": "Economic Perception Distribution"},
        {"path": "images/dem_econ_perception_scatter.png", "caption": "Perception vs Satisfaction"},
        {"path": "images/dem_gdp_scatter.png", "caption": "GDP vs Satisfaction"},
        {"path": "images/dem_correlation_matrix.png", "caption": "Correlation Matrix"},
    ]
))