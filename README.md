# About

`extract.py` takes as input a list of URLs to download and parse. It will
attempt to extract the main body text of each HTML document using a super fun
child weighting algorithm and split the body text into three types of elements:
headers, paragraphs, and list items.

After parsing each document, it opens an interface to manually check and correct
the annotations for each input document. Finally, it saves the output
annotations for each of these documents in a specified output directory.

# Installation

This project uses Python 3. After cloning the repository, switch into the
project's directory and run the following:

```sh
pyvenv env
source env/bin/activate
pip install -r requirements.txt
```

# Usage

```sh
python extract.py <paragraph word limit> <output directory>
```

The script expects a URL list from standard input.

# Running

Make sure to activate the environment first:

```sh
source env/bin/activate
```

Then, run `extract.py` with the parameters from above:

```sh
python extract.py 120 output_dir < url_list.txt
```

The script will print a message telling you to visit `http://localhost:8080` to
begin checking annotations. The script downloads and parses the HTML documents
between page loads, so expect a couple seconds of delay between each annotation
task.

When you reach the end screen, you can switch back to the terminal and kill the
web server. The output documents will be available in the output folder
specified on the command line.

# Output

Output files are annotated used `<span>` elements with different classes.
Headers have class `coded_h`, paragraphs have class `coded_p` and list items
have class `coded_l`. Text not contained within a `<span>` was considered
extraneous text by the manual annotator and can be removed from the document.

While the interface does turn paragraphs over the word limit an irritating shade
of red, it will not prevent the user from allowing overly long paragraphs.
Paragraphs that are still red after the user submits the task will still show up
as `coded_p` in the output document.
