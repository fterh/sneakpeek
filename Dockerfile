FROM python:3
WORKDIR /
COPY . /
RUN pip install pipenv
RUN pipenv run pip freeze > requirements.txt
RUN pip install -r requirements.txt
ENV SUBREDDIT singapore
CMD ["python", "main.py"]
