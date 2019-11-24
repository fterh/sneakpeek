from config import bot_config


class Comment:
    def __init__(self, title: str, body: str, byline: str = "", attribution: str = ""):
        self.title = title
        self.body = body
        self.byline = byline
        self.attribution = attribution

    def length(self) -> int:
        return sum(
            map(len, [self.title, self.body, self.byline, self.attribution])
        )

    def _title_as_md(self) -> str:
        return "> # " + self.title

    def _body_as_md(self) -> str:
        body_md = "> " + self.body  # Insert first blockquote (>) Markdown symbol
        return body_md.replace("\n\n", "\n\n> ")

    @staticmethod
    def footer() -> str:
        return f"---\n{bot_config.version} | [Source code]({bot_config.repo}) | [Contribute]({bot_config.repo})"

    def format_as_md(self) -> str:
        return '\n\n'.join(
            [
                self._title_as_md(),
                self._body_as_md(),
                self.footer()
            ]
        )
