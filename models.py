
# importing ABC and abstractmethod to enable abstract base class pattern
from abc import ABC, abstractmethod


class Project(ABC):
    """
    Abstract base class for all portfolio projects.

    Demonstrates:
    - Abstraction: cannot be instantiated directly, only through subclasses
    - Encapsulation: attributes stored as private (_attr) with public @property accessors
    - Polymorphism: render_markdown() is defined differently in each subclass
    """

    # class variable — shared across ALL instances of Project and its subclasses
    # tracking how many project objects have been created in total
    project_count = 0

    def __init__(self, title, description, dataset=None, questions=None, insights=None, tools=None):
        # incrementing class variable every time a new project is created
        Project.project_count += 1

        # using setters here so validation runs on init too (encapsulation)
        self.title = title
        self.description = description

        # storing optional fields as private instance variables
        self._dataset = dataset
        self._questions = questions or []
        self._insights = insights or []
        self._tools = tools or []

    # --- properties with validation (encapsulation) ---
    # exposing private attributes through @property with type and value checks

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # validating title is a non-empty string
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        self._title = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        # validating description is a non-empty string
        if not value or not isinstance(value, str):
            raise ValueError("Description must be a non-empty string")
        self._description = value.strip()

    @property
    def tools(self):
        # exposing as read-only — no setter, set at construction time only
        return self._tools

    @property
    def questions(self):
        return self._questions

    @property
    def insights(self):
        return self._insights

    @property
    def dataset(self):
        return self._dataset

    # --- dunder methods ---

    def __str__(self):
        # returning human-readable string — used when print() is called on a project
        return f"{self.__class__.__name__}: {self.title}"

    def __repr__(self):
        # returning developer representation — used in debugging and logs
        return f"{self.__class__.__name__}(title='{self.title}')"

    # --- abstract method (abstraction + polymorphism) ---

    @abstractmethod
    def render_markdown(self):
        """
        Rendering the project as a markdown string.

        Marked @abstractmethod — every subclass MUST implement this.
        Each subclass implements it differently (polymorphism).
        Python raises TypeError if a subclass forgets to implement it.
        """
        pass

    # --- shared protected helper ---

    def _render_base_markdown(self):
        """
        Shared markdown rendering logic for all subclasses.

        Prefixed with _ to indicate internal/subclass use only.
        Subclasses calling this via self._render_base_markdown() to reuse
        shared structure without duplicating code (inheritance + code reuse).
        """
        # building base div with shared project info
        md = f"""<div style="background:#f8f9fa; padding:25px; margin-bottom:40px; border-radius:12px;">

## {self.title}

#### Overview
{self.description}
"""
        # appending optional sections only if data exists
        if self.dataset:
            md += f"\n#### Dataset\n{self.dataset}\n"

        if self.questions:
            md += "\n#### Key Questions\n"
            for q in self.questions:
                md += f"- {q}\n"

        if self.insights:
            md += "\n#### Key Insights\n"
            for i in self.insights:
                md += f"- {i}\n"

        if self.tools:
            md += "\n#### Tools Used\n"
            for t in self.tools:
                md += f"- {t}\n"

        return md


class DashboardProject(Project):
    """
    A project that includes an embedded interactive dashboard.

    Inheriting from Project and extending with dashboard_link property.
    render_markdown() calls _render_base_markdown() then appends iframe.
    """

    def __init__(self, title, description, dataset, questions, insights, tools, dashboard_link):
        # calling parent __init__ to reuse shared initialisation logic
        super().__init__(title, description, dataset, questions, insights, tools)
        self.dashboard_link = dashboard_link

    @property
    def dashboard_link(self):
        return self._dashboard_link

    @dashboard_link.setter
    def dashboard_link(self, value):
        # validating dashboard link is a non-empty string
        if not value or not isinstance(value, str):
            raise ValueError("Dashboard link must be a non-empty string")
        self._dashboard_link = value.strip()

    def render_markdown(self):
        # calling shared base rendering first, then appending dashboard iframe
        md = self._render_base_markdown()
        md += f"""
#### Interactive Dashboard

<iframe 
  src="{self.dashboard_link}"
  width="100%" 
  height="750"
  style="border: none;">
</iframe>

</div>

---

"""
        return md


class ProductProject(Project):
    """
    A project focused on a product or engineering solution.

    Inheriting from Project and extending with problem and solution fields.
    render_markdown() builds its own layout — not using _render_base_markdown().
    """

    def __init__(self, title, description, problem, solution):
        # calling parent __init__ with only title and description
        super().__init__(title, description)
        self.problem = problem
        self.solution = solution

    @property
    def problem(self):
        return self._problem

    @problem.setter
    def problem(self, value):
        # validating problem is a non-empty string
        if not value or not isinstance(value, str):
            raise ValueError("Problem must be a non-empty string")
        self._problem = value.strip()

    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, value):
        # validating solution is a non-empty string
        if not value or not isinstance(value, str):
            raise ValueError("Solution must be a non-empty string")
        self._solution = value.strip()

    def render_markdown(self):
        # building its own markdown layout with problem/solution structure
        md = f"""<div style="background:#f8f9fa; padding:25px; margin-bottom:40px; border-radius:12px;">

## {self.title}

#### Overview
{self.description}

**Problem:** {self.problem}

**Solution:** {self.solution}

</div>

---
"""
        return md


class VisualProject(Project):
    """
    A project showcasing data analysis through static visualizations.

    Inheriting from Project and extending with image_paths for chart display.
    render_markdown() calls _render_base_markdown() then appends images.
    """

    def __init__(self, title, description, dataset, questions, insights, tools, image_paths):
        # calling parent __init__ to reuse shared initialisation logic
        super().__init__(title, description, dataset, questions, insights, tools)
        # storing image paths as private instance variable
        self._image_paths = image_paths

    @property
    def image_paths(self):
        # exposing as read-only — no setter needed
        return self._image_paths

    def render_markdown(self):
        # calling shared base rendering first, then appending visualization images
        md = self._render_base_markdown()

        md += "\n#### Visualizations\n"
        # iterating over image paths and rendering each with caption
        for img in self._image_paths:
            md += f'\n<img src="{img["path"]}" alt="{img["caption"]}" style="width:100%; border-radius:8px; margin-bottom:12px;">\n'
            md += f'<p style="color:#888; font-size:0.85em; margin-top:-8px;">{img["caption"]}</p>\n'

        md += "\n</div>\n\n---\n"
        return md