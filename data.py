
# importing project classes from models and base Project class for type checking
from models import DashboardProject, ProductProject, VisualProject, Project


class Portfolio:
    """
    Container class managing all portfolio projects.
    
    Demonstrates:
    - Encapsulation: projects stored privately, exposed via iteration
    - Dunder methods: __iter__, __len__, __repr__ make it behave like a collection
    """

    def __init__(self, owner_name):
        # storing owner name via setter so validation runs immediately
        self.owner_name = owner_name
        # storing projects as private list — not accessible directly from outside
        self._projects = []

    @property
    def owner_name(self):
        return self._owner_name

    @owner_name.setter
    def owner_name(self, value):
        # validating that owner name is a non-empty string
        if not value or not isinstance(value, str):
            raise ValueError("Owner name must be a non-empty string")
        self._owner_name = value.strip()

    def add_project(self, project):
        """Adding a project — only accepting Project instances."""
        # enforcing type safety — only real Project subclasses allowed
        if not isinstance(project, Project):
            raise TypeError(f"Expected a Project instance, got {type(project).__name__}")
        self._projects.append(project)
        # returning self to allow method chaining: portfolio.add_project(...).add_project(...)
        return self

    def get_by_type(self, project_type):
        """Returning only projects matching a specific subclass type."""
        # filtering projects by type using isinstance (polymorphism awareness)
        return [p for p in self._projects if isinstance(p, project_type)]

    def __iter__(self):
        """Making Portfolio directly iterable — enables: for project in portfolio."""
        return iter(self._projects)

    def __len__(self):
        """Making len(portfolio) work like a list."""
        return len(self._projects)

    def __repr__(self):
        """Returning developer-friendly string representation."""
        return f"Portfolio(owner='{self.owner_name}', projects={len(self._projects)})"

    def export_qmd(self, filepath="generated_projects.qmd"):
        """Exporting all projects to a .qmd file — replaces generate_projects.py."""
        with open(filepath, "w") as f:
            f.write(f"# {self.owner_name}'s Projects\n\n")
            # calling render_markdown() on each project — polymorphism in action
            for project in self._projects:
                f.write(project.render_markdown())
        print(f"Exported {len(self._projects)} projects to {filepath}")


# --- building the portfolio ---

# instantiating Portfolio with owner name
portfolio = Portfolio(owner_name="Alnura Abdyrova")

# adding DashboardProject — extends Project with embedded Tableau dashboard
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
# chaining add_project — returns self so next call can be added directly
)).add_project(VisualProject(
    title="Democracy and Economic Perception",
    description="Do people judge democracy by GDP numbers or by how their wallet actually feels? "
                "Using World Values Survey data across 60+ countries, this study finds that "
                "subjective economic perception — not objective indicators like GDP or unemployment — "
                "is the only statistically significant predictor of satisfaction with democracy. "
                "The vibes, it turns out, win.",
    dataset="World Values Survey Wave 7 (2017-2022), World Bank, V-Dem Institute — 88,499 respondents across 60+ countries",
    questions=[
        "Do people judge democracy based on GDP, or how they personally feel about the economy?",
        "Does democracy quality actually predict satisfaction with democracy?",
        "Which individual factors (age, education, income) matter for democratic satisfaction?"
    ],
    insights=[
        "Economic perception is the only statistically significant predictor across all three models",
        "GDP, unemployment, and democracy quality score show no significant effect once perception is controlled",
        "Older and more educated people report higher satisfaction with democracy",
        "The perception gap — not the numbers — is what drives democratic legitimacy"
    ],
    tools=["Python", "pandas", "OLS Regression", "World Values Survey", "World Bank Data", "V-Dem"],
    # passing image paths with captions — rendered by VisualProject.render_markdown()
    image_paths=[
        {"path": "images/dem_satisfaction_dist.png", "caption": "Distribution of Satisfaction with Democracy"},
        {"path": "images/dem_econ_perception_dist.png", "caption": "Distribution of Economic Perception across countries"},
        {"path": "images/dem_econ_perception_scatter.png", "caption": "Economic Perception vs Satisfaction with Democracy"},
        {"path": "images/dem_gdp_scatter.png", "caption": "GDP vs Satisfaction with Democracy"},
        {"path": "images/dem_correlation_matrix.png", "caption": "Correlation Matrix of Key Variables"},
    ]
))