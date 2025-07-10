import html.parser

import requests


class LinkTitleParser(html.parser.HTMLParser):
    last_content = ''
    title_content = ''

    def __init__(self, url):
        super().__init__()
        self.url = url
        response = requests.get(self.url, allow_redirects=True)
        if 199 < response.status_code < 300:
            # Got it! go ahead and parse. Hopefully this creates a title
            self.feed(response.text)
        else:
            self.title_content = ''

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        self.last_content = ''

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
        if tag == 'title' and self.title_content == '':
            self.title_content = self.last_content

    def handle_data(self, data):
        print("Encountered some data  :", data)
        self.last_content += data
