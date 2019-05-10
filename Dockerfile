FROM python:3
WORKDIR /
COPY . /
RUN pip install -r requirements.txt
ENV SUBREDDIT singapore
CMD ["python", "main.py"]
