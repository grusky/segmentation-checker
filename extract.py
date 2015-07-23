import sys, os
from bottle import get, post, run, template, request

from bs4 import BeautifulSoup
from make_sections import make_sections, Heading, Paragraph, List
from find_root import find_root_element

from urllib.request import urlopen
from urllib.parse import urlparse


def main():

    urls = [line.strip() for line in sys.stdin]
    extract = Extract(sys.argv[2], urls, int(sys.argv[1]))

    get("/")(extract.start_page)
    post("/")(extract.annotate_page)

    print("Hello human annotator. Visit http://localhost:8080 in your browser.")
    run(host='localhost', port=8080, quiet=True)


class Extract:

    def __init__(self, output_dir, urls, word_limit):

        self.dir = os.path.dirname(__file__)

        self.output_dir = os.path.abspath(output_dir)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        self.help_temp = os.path.join(self.dir, "templates/help.html")
        self.start_temp = os.path.join(self.dir, "templates/start.html")
        self.annotate_temp = os.path.join(self.dir, "templates/annotate.html")
        self.done_temp = os.path.join(self.dir, "templates/done.html")

        self.urls = urls
        self.word_limit = word_limit


    def start_page(self):

        url_list = "\n".join(["<li>" + url + "</li>" for url in self.urls])

        return template(self.start_temp,
                        urls=url_list,
                        help=self.__help_page())


    def annotate_page(self):

        self.__write_annotations()

        if self.__has_next_url():

            url = self.__next_url()
            body = self.__process_url(url)

            filename = urlparse(url).netloc + ".html"

            return template(self.annotate_temp,
                            text=body,
                            file=filename,
                            words=self.word_limit,
                            help=self.__help_page())
        else:

            return self.done_page()
        

    def done_page(self):

        return template(self.done_temp, output=self.output_dir)


    def __help_page(self):

        return template(self.help_temp, words=self.word_limit)


    def __write_annotations(self):

        try:
            result = request.forms.get("result")
            filename = request.forms.get("file")

            with open(os.path.join(self.output_dir, filename), "w") as f:
                f.write(result.replace("<br>", ""))

        except:
            pass


    def __has_next_url(self):

        return len(self.urls) > 0


    def __next_url(self):

        return self.urls.pop()


    def __process_url(self, url):

        page = urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        root = find_root_element(soup)

        html = ""

        for section in make_sections(root):

            if type(section) is Heading:
                html += "<span class=\"coded_h\">" \
                     + section.text + "</span><br><br>"

            elif type(section) is List:
                for item in section.items:
                    html += "<span class=\"coded_l\">" \
                         + item + "</span><br><br>"

            elif type(section) is Paragraph:
                html += "<span class=\"coded_p\">" \
                     + section.text + "</span><br><br>"

        return html


if __name__ == "__main__":
    main()
