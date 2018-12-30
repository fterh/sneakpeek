from invoke import task


@task
def start(c):
    """Start in production mode."""
    c.run("ENV=prod python main.py")

@task
def run(c):
    """Start in development mode."""
    c.run("python main.py")

@task
def test(c):
    c.run("ENV=test python -m unittest discover")
