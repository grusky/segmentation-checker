from bs4 import BeautifulSoup
import bs4


class Heading:
    def __init__(self, text):
        self.text = text

class Paragraph:
    def __init__(self, text):
        self.text = text

class List:
    def __init__(self, items=[]):
        self.items = items

    def add_item(self, item):
        self.items.append(item)


def make_sections(root):
    sections = []

    # unwrap unnecessary inline elements (other than b or strong)
    # sometimes people put crazy tags in body elements (like script) that
    # shouldn't be there -- must delete these from the document

    unwrap = {"i", "u", "em", "a", "span", "font"}
    delete = {"script", "style", "head", "meta", "link", "title", "noscript", "select", "form", "input", "nav", "iframe"}

    for tag in unwrap: 
        try:
            for match in root(tag):
                match.unwrap()
        except:
            pass

    for tag in delete: 
        try:
            for match in root(tag):
                match.extract()
        except:
            pass

    root = BeautifulSoup(" ".join(str(root).split()), "html.parser")

    for child in root.recursiveChildGenerator():
        if type(child) is bs4.element.NavigableString:

            # find all of a child node's parent names

            parents = set()
            element = child
            while element.name != "[document]":
                if element.name != None:
                    parents.add(element.name)
                element = element.parent

            # eliminate all h* headers

            h_header = False
            for parentTag in parents:
                if parentTag[0] == "h" and parentTag[1].isdigit():
                    h_header = True
                    break

            # get the body text of the child, stripping whitespace

            text = child.string.strip()

            # record h* or bold-type headers (if requested)

            if h_header or "b" in parents or "strong" in parents:
                if text != "":
                    sections.append(Heading(text))
                continue

            # record list items

            elif "li" in parents:
                if len(text) > 0:
                    if len(sections) == 0 or type(sections[-1]) is not List:
                        sections.append(List([text]))
                    else:
                        sections[-1].add_item(text)
                continue

            # record non-list paragraphs

            if len(text) > 10 and ("." in text or text[-1] == ":"):
                if text.count("}") + text.count("{") < 5 and text.count("=") < 2:
                    if text[0] == "." or text[0] == ":":
                        text = text[1:].strip()
                    sections.append(Paragraph(text))

    return sections
