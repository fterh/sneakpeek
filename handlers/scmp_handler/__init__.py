"""Handler for South China Morning Post."""

import requests
from bs4 import BeautifulSoup
from comment import Comment
from itertools import chain
from handlers.abstract_base_handler import AbstractBaseHandler, HandlerError

def get_text_from_children(children_element):
    child_body = ""
    
    for child in children_element:
        if child['type'] == "text":
            child_body += child['data']
        elif child['type'] == "a" or child['type'] == "em":
            child_body += get_text_from_children(child['children'])
    
    return child_body

class ScmpHandler(AbstractBaseHandler):
    """Handler for Scmp."""

    @classmethod
    def handle(cls, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        article_script = [script.text for script in soup.find_all("script") if script is not None and "window.__APOLLO_STATE__" in script.text.strip()]
        json_article = json.loads(article_script[0][ article_script[0].find("=")+1: ])
        json_content = json_article['contentService']

        content_key = [k for k in json_content.keys() if k.startswith("$ROOT_QUERY.content")][0]
        title = json_content[content_key]['headline']

        subheadlines_element = json_content[content_key]['subHeadline']['json'][0]['children']

        subheadlines = []
        for elem in subheadlines_element:
            if elem['type'] == "text":
                subheadlines.append(elem['data'])
            else:
                for elem_child in elem['children']:
                    if elem_child['type'] == "text":
                        subheadlines.append(elem_child['data'])

        subheadlines_md = "\n".join(["* " + subheadline.strip() for subheadline in subheadlines if subheadline.strip() != ""])

        body_key = [k for k in json_content[content_key].keys() if k.startswith("body")][0]

        body_list = []
        for j in json_content[content_key][body_key]['json']:
            if "children" not in j.keys():
                continue
                
            if j['type'] != "p":
                continue
                
            body_list.append(get_text_from_children(j['children']))

        body_list = [b.strip() for b in body_list if b.strip() != ""]
        body = subheadlines_md + "\n" + "\n".join(body_list)

        return Comment(title, body.strip())
