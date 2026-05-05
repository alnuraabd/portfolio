# models.py

from abc import ABC, abstractmethod


# defining abstract base class for all projects
class Project(ABC):
    """Abstract base class for all portfolio projects."""

    # tracking number of created projects (class variable)
    project_count = 0

    # initializing project with basic attributes
    def __init__(self, title, description, dataset=None, questions=None, insights=None, tools=None):
        Project.project_count += 1
        self.title = title
        self.description = description
        self._dataset = dataset
        self._questions = questions or []
        self._insights = insights or []
        self._tools = tools or []



    # properties with validation

    # getting and validating title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # ensuring title is non-empty string
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        self._title = value.strip()

    # getting and validating description
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        # ensuring description is non-empty string
        if not value or not isinstance(value, str):
            raise ValueError("Description must be a non-empty string")
        self._description = value.strip()

    # returning tools list
    @property
    def tools(self):
        return self._tools

    # returning questions list
    @property
    def questions(self):
        return self._questions

    # returning insights list
    @property
    def insights(self):
        return self._insights

    # returning dataset info
    @property
    def dataset(self):
        return self._dataset


    # dunder methods


    # returning readable string for users
    def __str__(self):
        return f"{self.__class__.__name__}: {self.title}"

    # returning debug-friendly representation
    def __repr__(self):
        return f"{self.__class__.__name__}(title='{self.title}')"


    # abstract method


    # forcing subclasses to implement rendering logic
    @abstractmethod
    def render_markdown(self):
        pass


    # shared rendering logic


    # building common markdown structure for all projects
    def _render_base_markdown(self):
        md = f"""<div style="background:#f8f9fa; padding:25px; margin-bottom:40px; border-radius:12px;">

## {self.title}

#### Overview
{self.description}
"""

        # adding dataset section if exists
        if self.dataset:
            md += f"\n#### Dataset\n{self.dataset}\n"

        # adding questions list
        if self.questions:
            md += "\n#### Key Questions\n"
            for q in self.questions:
                md += f"- {q}\n"

        # adding insights list
        if self.insights:
            md += "\n#### Key Insights\n"
            for i in self.insights:
                md += f"- {i}\n"

        # adding tools list
        if self.tools:
            md += "\n#### Tools Used\n"
            for t in self.tools:
                md += f"- {t}\n"

        return md


# defining dashboard project (inherits from Project)
class DashboardProject(Project):
    """Project with embedded dashboard."""

    # initializing with dashboard link
    def __init__(self, title, description, dataset, questions, insights, tools, dashboard_link):
        super().__init__(title, description, dataset, questions, insights, tools)
        self.dashboard_link = dashboard_link

    # validating dashboard link
    @property
    def dashboard_link(self):
        return self._dashboard_link

    @dashboard_link.setter
    def dashboard_link(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Dashboard link must be a non-empty string")
        self._dashboard_link = value.strip()

    # rendering project with embedded iframe
    def render_markdown(self):
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


# defining product-focused project
class ProductProject(Project):
    """Project describing product solution."""

    # initializing with problem and solution
    def __init__(self, title, description, problem, solution):
        super().__init__(title, description)
        self.problem = problem
        self.solution = solution

    # validating problem text
    @property
    def problem(self):
        return self._problem

    @problem.setter
    def problem(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Problem must be a non-empty string")
        self._problem = value.strip()

    # validating solution text
    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Solution must be a non-empty string")
        self._solution = value.strip()

    # rendering product project block
    def render_markdown(self):
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


# defining visual project with static images
class VisualProject(Project):
    """Project showing visual outputs."""

    # initializing with list of images
    def __init__(self, title, description, dataset, questions, insights, tools, image_paths):
        super().__init__(title, description, dataset, questions, insights, tools)
        self._image_paths = image_paths

    # returning image list
    @property
    def image_paths(self):
        return self._image_paths

    # rendering images with captions
    def render_markdown(self):
        md = self._render_base_markdown()

        md += "\n#### Visualizations\n"

        # looping through images and adding them
        for img in self._image_paths:
            md += f'\n<img src="{img["path"]}" alt="{img["caption"]}" style="width:100%; border-radius:8px; margin-bottom:12px;">\n'
            md += f'<p style="color:#888; font-size:0.85em; margin-top:-8px;">{img["caption"]}</p>\n'

        md += "\n</div>\n\n---\n"
        return md