# Core Idea

Every document loader implements the same BaseLoader interface and produces a list of Document objects. A Document has two key attributes:

```
from langchain_core.documents

doc = Document(
    page_content="the actual text",
    metadata={"source": "...", "page": 1}  # arbitrary dict
)
```

# Main Loaders

- from langchain_community.document_loaders import TextLoader - produces a single document where page_content is the whole file's text
- from langchain_community.document_loaders import PyPDFLoader - produces one document per page and metadata includes source and page
```
[
    Document(
        page_content="Q3 Financial Report\nRevenue grew 12% year over year...",
        metadata={"source": "./data/report.pdf", "page": 0}
    ),
    Document(
        page_content="Regional Breakdown\nNorth America: $4.2M...",
        metadata={"source": "./data/report.pdf", "page": 1}
    ),
    Document(
        page_content="Outlook for Q4\nWe expect continued growth...",
        metadata={"source": "./data/report.pdf", "page": 2}
    ),
]
```
- from langchain_community.document_loaders import CSVLoader - produces one document per row
```
[
    Document(
        page_content="id: 1\nname: Alice\ndepartment: Engineering",
        metadata={"source": "./data/data.csv", "row": 0}
    ),
    Document(
        page_content="id: 2\nname: Bob\ndepartment: Sales",
        metadata={"source": "./data/data.csv", "row": 1}
    ),
]
```
from langchain_community.document_loaders import Docx2txtLoader - produces a single document with entire document's text as page_content
```
[
    Document(
        page_content="Annual Report\n\nExecutive Summary\nThis year the company achieved...",
        metadata={"source": "./data/report.docx"}
    )
]
```
from langchain_community.document_loaders import DirectoryLoader, TextLoader
