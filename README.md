# 🤖 dpkg Profiler
[![forthebadge made-with-python](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-390/) [![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)

![Screenshot from 2024-02-27 12-31-01](https://github.com/ko-sangari/dpkg-profiler/assets/38611172/6c89f5e7-3531-4b3e-af6d-8c08f7fff193)


## ⭕ Contents
- [The project's purpose](#-the-project's-purpose)
- [What tools were used to create this project](#-what-tools-were-used-to-create-this-project)
- [Before you begin](#-before-you-begin)
- [how to run the project](#-how-to-run-the-project)
- [how to run tests](#-how-to-run-tests)
- [Final step](#-final-step)


## ⭕ The project's purpose
The purpose of the project is to develop a Python program that provides details about installed packages on a Debian or Ubuntu operating system via a JSON REST API. This program will read information from the `/var/lib/dpkg/status` file, which contains data about software packages. The Python script will parse this file and expose the package details through a JSON API, allowing users to retrieve information about installed packages programmatically. Also, a Streamlit-based frontend serves as an interface for the APIs.

## ⭕ What tools were used to create this project
| Technology         |    🔗             |
| -----------------  | ----------------- |
| fastapi            | [[Github Link](https://github.com/tiangolo/fastapi)] |
| fastapi-pagination | [[Github Link](https://github.com/uriyyo/fastapi-pagination)] |
| uvicorn            | [[Github Link](https://github.com/encode/uvicorn)] |
| pydantic           | [[Github Link](https://github.com/pydantic/pydantic)] |
| pydantic-settings  | [[Github Link](https://github.com/pydantic/pydantic-settings)]  |
| streamlit          | [[Github Link](https://github.com/streamlit/streamlit)] |
| httpx              | [[Github Link](https://github.com/encode/httpx/)] |
| sqlalchemy         | [[Github Link](https://github.com/sqlalchemy/sqlalchemy)] |
| aiosqlite          | [[Github Link](https://github.com/omnilib/aiosqlite)] |
| asyncio            | [[Github Link](https://github.com/python/cpython/blob/main/Doc/library/asyncio.rst) ] |
| poetry             | [[Github Link](https://github.com/python-poetry/poetry)] |
| docker             | [[Github Link](https://github.com/docker-library/python)] |
| docker-compose     | [[Github Link](https://github.com/docker/compose)] |
| pytest             | [[Github Link](https://github.com/pytest-dev/pytest)] |
| pytest-asyncio     | [[Github Link](https://github.com/pytest-dev/pytest-asyncio)] |
| coverage           | [[Github Link](https://github.com/nedbat/coveragepy?tab=readme-ov-file)] |
| mypy               | [[Github Link](https://github.com/python/mypy)] |


## ⭕ Before you begin
Before you begin, please follow these steps:

1. Create a folder named `secret` within both the `frontend` and `backend` directories.
2. Move the `.env.template` file which is in the root directory into the each `secret` folder.
3. Rename the `.env.template` file to `.env`.
4. Update the variables in the `.env` file according to your local environment.

Additionally, make sure you have another `.env` file named `.env.docker`, which should contain Docker-related variables. (Check the `.env.template` file for more details.)

<br>🌟 To import the packages from /var/lib/dpkg/status into the database, you can run the command below.
<br>However, note that this task will run each time you try to build the Docker images.
```commandline
cd backend
poetry run python src/utils/parser.py
```


## ⭕ How to Run the Project
Navigate to the root of the project. <br>
To build the image from the Dockerfile, run:
```commandline
docker compose up --build -d
```

<br>Or, there's a `Makefile` for your convenience, so just run: (Check other commands too!)
```commandline
make run
```

<br>Or, If you want to run the project locally, you need to have `poetry` installed first.
```commandline
pip install poetry
poetry install
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

<br>Now, you can check the **Swagger** URL for API documentation.
```commandline
http://localhost:8000/
```

<br>And for the **Streamlit** frontend dashboard, please redirect to the link below.
```commandline
http://localhost:8501/
```


## ⭕ How to run tests
Run _pytest_ command to run the tests separately.<br>
```commandline
make tests
```

<br>And, what about Test Coverage?
```commandline
make coverage

# Backend Directory               Stmts   Miss  Cover
# -----------------------------------------------------
# Test Coverage TOTAL              369     28    92%
```

<br>🌟 This project has been thoroughly checked with `mypy` for type consistency, and it currently passes all mypy checks without any issues.
```commandline
make mypy
```

## ⭕ Final step
```commandline
make coffee
```
#### Be Happy Even if Things Aren’t Perfect Now. 🎉🎉🎉
#### Enjoy your coffee! ☕

![](https://i1.wp.com/justmaths.co.uk/wp-content/uploads/2016/10/celebration-gif.gif)
