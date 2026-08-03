# 1. __init__.py Functionality
- In each folder we create such as routers/, schemas/, etc., we initialize inside each one an __init__.py file to tell Python "this folder is a package - something we are allowed to import from using dot notation.
- Without this practice, a folder is just a folder and python does not treat it as something importable. Hence even an empty __init__.py is the marker that flips from "just a directory sitting on disk to a legitimate Python Package we can import from". Just its existence is what matters.
```
app/
├── dependencies.py
├── database.py
├── models/
│   └── __init__.py     ← needed
├── schemas/
│   └── __init__.py     ← needed
├── routers/
│   └── __init__.py     ← needed
```