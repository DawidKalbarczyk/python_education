import os
from celery import Celery
from groq import Groq
from pydantic import BaseModel

app = Celery(
    'movie_info',
    broker=os.environ.get('CELERY_BROKER_URL'),
    backend=os.environ.get('CELERY_BACKEND_URL')
)

client = Groq()

class MoviePartA(BaseModel):
    title: str
    release_year: int

class MoviePartB(BaseModel):
    director: str
    genre: str

class MoviePartC(BaseModel):
    actors: list[str]

@app.task
def movie_info_a(prompt):
    response = client.chat.completions.create(
        model = 'openai/gpt-oss-120b',
        messages = [
            {'role': 'system', 'content': "You are an assistant that provides movie information in a structured JSON format."},
            {'role': 'user', 'content': prompt}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "movie_part_a",
                "schema": MoviePartA.model_json_schema(),
            },
        }
    )

    movie_part_a = MoviePartA.model_validate_json(response.choices[0].message.content)

    return movie_part_a.model_dump()

@app.task
def movie_info_c(prompt):
    response = client.chat.completions.create(
        model = 'openai/gpt-oss-120b',
        messages = [
            {'role': 'system', 'content': "You are an assistant that provides movie information in a structured JSON format."},
            {'role': 'user', 'content': prompt}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "movie_part_c",
                "schema": MoviePartC.model_json_schema(),
            },
        }
    )

    movie_part_c = MoviePartC.model_validate_json(response.choices[0].message.content)

    return movie_part_c.model_dump()

@app.task
def movie_info_b(prompt):
    response = client.chat.completions.create(
        model = 'openai/gpt-oss-120b',
        messages = [
            {'role': 'system', 'content': "You are an assistant that provides movie information in a structured JSON format."},
            {'role': 'user', 'content': prompt}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "movie_part_b",
                "schema": MoviePartB.model_json_schema(),
            },
        }
    )

    movie_part_b = MoviePartB.model_validate_json(response.choices[0].message.content)

    return movie_part_b.model_dump()

@app.task
def combine_parts(parts):
    combined = {}
    for part in parts:
        combined.update(part)
    return combined