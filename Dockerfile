FROM python:3.7
WORKDIR /
COPY . /
RUN pip install pipenv
RUN pipenv install
RUN pipenv run pip freeze > requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
