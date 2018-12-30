import config


class Comment:
    def __init__(self, title, body, byline="", attribution=""):
        self.title = title
        self.body = body
        self.byline = byline
        self.attribution = attribution


def generate_title_markdown(title):
    return "> # " + title


def generate_body_markdown(body):
    body = "> " + body # Insert first blockquote (>) Markdown symbol
    body = body.replace("\n\n", "\n\n> ")
    return body


COMMENT_FOOTER = "---\n{} | [Source code]({}) | [Contribute]({})".format(
    config.BOT["VERSION"],
    config.BOT["REPO_LINK"],
    config.BOT["CONTRIBUTE_LINK"]
)


def format_comment(comment):
    return generate_title_markdown(comment.title) + \
        "\n\n" + generate_body_markdown(comment.body) + \
        "\n\n" + COMMENT_FOOTER
