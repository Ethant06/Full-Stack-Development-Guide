# What is a virtual environment

A virtual environment is an isolated Python installation for one project, so rather than installing packages globally on your computer, you install them only for that project.

### Typical Workflow

- Create the project: Backend/
- Create a virtual environment within that directory: python -m venv .venv
- Activate it. In git bash (Linux like) you do source .venv/Scripts/activate
- Then install packages such as pip install numpy or pandas or fastapi

# Biggest reason: version conflicts

- Imagine today we build a project using fastapi == 0.12. Then a year later
FastAPI is on fastapi == 0.16. We decide then to create a new project and install the newest version. If everything is global and we dont use venv, we just upgraded FastAPI for all our projects so then an older project might suddenly stop working because it relied on the old version.
- Hence with a venv, each project keeps using the version it developed with.
- Another great benefit is sharing our project. If we uploaded our project to GitHub and we include a requirements.txt that lists all the versions we used, someone else can run
```
pip install -r requirements.txt
```
into a fresh venv and they'll have the exact same setup we used. Without a virtual environment, it is hard to know exactly which packages and versions our project depends on.