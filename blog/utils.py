from flask import session, request, redirect

from mistune import Markdown
from html_sanitizer import Sanitizer
from bs4 import BeautifulSoup

from functools import wraps
import datetime
import json

from . import html

def json_error(message, code=505):
    return json.dumps({
        "error": {
            "code": code,
            "message": message,
        }
    })

def build_next_page_url(page, topic=None, query_string=None):
    nextPage = '/posts?'
    if topic:
        nextPage += 'topic=' + topic
    if query_string:
        nextPage += '&q=' + query_string
    nextPage += '&page=' + str(page + 1)
    return nextPage

def parse_json_post_data(json_data, post_author):
    data = json.loads(json_data)

    if 'title' not in data:
        raise Exception("No title found in data")

    data["posted"] = datetime.datetime.utcnow()
    markdown = Markdown()
    content = markdown(data['content'])
    content = html.sanitize_html(content)

    data['preview'] = html.html_preview(content)
    data['markdown'] = data['content']
    data['content'] = content
    data['author'] = post_author
    data['img'] = html.get_first_img(content)
    
    if 'topics' in data:
        for count in range(0, len(data['topics'])):
            data['topics'][count] = data['topics'][count].lower()

    # recreate dictionary to remove any unwanted fields the client
    # could have included in the post
    return {
        "title": data["title"],
        "posted": data["posted"],
        "preview": data["preview"],
        "markdown": data["markdown"],
        "content": data["content"],
        "author": data["author"],
        "img": data["author"],
    }