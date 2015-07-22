from bs4 import BeautifulSoup
import sys, queue, operator


def find_root(soup, k=0.5):

    blacklist = {"[document]", "html", "script", "style", "head", "meta",
            "link", "title", "noscript", "select", "form", "a", "input", "nav"}
    root_blacklist = {"p", "ul", "ol", "a", "h1", "h2", "h3", "h4", "h5",
            "li", "span", "em", "strong", "i", "bold"}

    scores = {}

    elements = queue.Queue()
    for e in soup.find_all(text=True): elements.put(e)

    while not elements.empty():
        element = elements.get()
        parent = element.parent

        if element.parent.name in blacklist:
            continue

        try:
            score = scores[element] * k + 1
        except:
            score = 1

        try:
            scores[parent] += score
        except:
            scores[parent] = score
            elements.put(parent)

    class Result:
        def __init__(self, result):
            self.element = result[0]
            self.score = result[1]
            
    return [Result(e) for e
            in sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
            if e[0].name not in root_blacklist]


def find_root_element(soup, k=0.5):

    return find_root(soup, k)[0].element
