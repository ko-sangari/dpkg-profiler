FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app

WORKDIR /home/app

COPY ./pyproject.toml ./poetry.lock* ./

RUN pip install poetry
RUN poetry install

COPY . /home/app

CMD ["poetry", "run", "streamlit", "run", "src/main.py", "--logger.level=debug"]
