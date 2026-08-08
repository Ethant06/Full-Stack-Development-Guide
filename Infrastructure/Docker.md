# What is Docker

Docker is a tool for packaging an application and everything it needs to run into a standardized environment called a container. Put simply,, it makes our application portable and predictable. Rather than say install python 3.12, install these 15 packages, install PostgreSQl, set this env variable, you can package much of that environment into Docker configuration so someone else can run our application in a consistent way.
###### Docker Isolates an entire application environment

# Problem Docker Solves

Imagine we built our FastAPI application on our computer - Python 3.12, PostgreSQL 18 FastAPI, SQLAlchemy. Everything works good, until we give our project to another developer. They have - Python 3.11, PostgreSQL 17, different configs. They run our application and get: ModuleNotFoundError, Database Connection failed.

# Container

Container is an isolated environment where our application runs.
```
Your Computer
│
├── Docker
│
├── Container: FastAPI
│   ├── Python
│   ├── FastAPI
│   ├── SQLAlchemy
│   └── Your backend
│
├── Container: PostgreSQL
│   └── PostgreSQL database
│
└── Container: Next.js
    ├── Node.js
    └── Your frontend
```
The containers are separated from each other but can communicate over a network.

# Docker Image vs Docker Container
- An image is the blueprint.
```
FastAPI Image
├── Python
├── dependencies
├── application code
└── configuration
```

- A container is a running instance of that image.
```
Image
  ↓
"Blueprint"
  ↓
Container
  ↓
"Running application"
```
You can create multiple containers from the same image. In programming analogy, an image is like a class, and a container is an Object instantiated from that class.

# What is Docker Compose

Our application is not just one thing, we potentially have:
```
- Next.js
- FastAPI
- PostgreSQL
```
Managing these individually can be annoying. Compose lets us describe our entire application architecture in one file

For example:
```
services:

  frontend:
    ...

  backend:
    ...

  database:
    ...
```
Then you can run something like:
```
docker compose up

and Docker can start:

Next.js container
        +
FastAPI container
        +
PostgreSQL container

and connect them together.
```

# Docker and Cloud deployment

Eventually when we want to deploy our application to AWS, our architecture could become:

```
 Internet
                       │
                       ↓
                 AWS infrastructure
                       │
              ┌────────┴────────┐
              ↓                 ↓
       Next.js container   FastAPI container
                                │
                                ↓
                         PostgreSQL
```
Then cloud platforms run our containers

# The Big Picture:
With docker:

```
Your computer
│
└── Docker
     │
     ├── FastAPI container
     │    └── Python + dependencies
     │
     ├── Next.js container
     │    └── Node + dependencies
     │
     └── PostgreSQL container
          └── PostgreSQL
```