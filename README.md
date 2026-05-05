# Alnura Abdyrova — Portfolio

Live site: [alnuraabd.github.io/portfolio](https://alnuraabd.github.io/portfolio)

## About

Personal portfolio built as part of course. The site showcases data science projects and demonstrates object-oriented programming principles in Python.

## Projects

- **Computer Games Industry Analysis** — exploring 70,000+ Steam games to understand how real-world events shape gaming trends, with an interactive Tableau dashboard
- **Democracy and Economic Perception** — cross-country analysis using World Values Survey data showing that subjective economic perception predicts satisfaction with democracy better than GDP or unemployment

## OOP Structure

The portfolio is built around a Python class hierarchy:

```
Project (ABC — abstract base class)
├── DashboardProject   # adds embedded interactive dashboard
├── ProductProject     # adds problem/solution structure
└── VisualProject      # adds static data visualizations

Portfolio              # container class managing all projects
```

Key OOP concepts implemented:

- **Abstraction** — `Project` is abstract, cannot be instantiated directly
- **Encapsulation** — private attributes with `@property` validation
- **Inheritance** — all project types extend `Project` via `super()`
- **Polymorphism** — `render_markdown()` behaves differently per subclass
- **Class variables** — `Project.project_count` tracks total projects created
- **Dunder methods** — `__str__`, `__repr__`, `__iter__`, `__len__` implemented across classes

## Tech Stack

- **Quarto** — static site generation
- **Python** — OOP models, data processing
- **Shiny** — interactive data explorer hosted on Posit Connect
- **Tableau** — games industry dashboard
- **GitHub Pages** — site hosting

## File Structure

```
portfolio/
├── index.qmd            # home page with music player
├── projects.qmd         # projects page, renders via OOP models
├── about.qmd            # about page
├── models.py            # OOP class hierarchy (Project, DashboardProject, VisualProject)
├── data.py              # Portfolio container class + project data
├── app.py               # Shiny interactive data explorer
├── styles.css           # site styling
├── _quarto.yml          # quarto site configuration
└── images/              # project visualizations and assets
```

## OOP Class Details

### `Project` (abstract base class)
- Cannot be instantiated directly
- Defines shared `__init__`, properties with validation, and `_render_base_markdown()`
- Declares `render_markdown()` as `@abstractmethod` — every subclass must implement it
- Tracks total project count via class variable `project_count`

### `DashboardProject(Project)`
- Inherits from `Project`
- Adds `dashboard_link` property with validation
- `render_markdown()` appends an embedded iframe

### `VisualProject(Project)`
- Inherits from `Project`
- Adds `image_paths` for static visualizations
- `render_markdown()` appends images with captions

### `ProductProject(Project)`
- Inherits from `Project`
- Adds `problem` and `solution` properties
- `render_markdown()` renders a problem/solution layout

### `Portfolio`
- Container class managing all projects
- `add_project()` validates input type before adding
- Implements `__iter__` and `__len__` so it behaves like a collection
- `export_qmd()` writes all projects to a `.qmd` file

### `DataProcessor` and `Visualizer` (in `app.py`)
- `DataProcessor` encapsulates data generation logic with mode validation
- `Visualizer` stores plot configuration as instance state, with class-level defaults

## Running Locally

```bash
git clone https://github.com/alnuraabd/portfolio.git
cd portfolio
quarto preview
```