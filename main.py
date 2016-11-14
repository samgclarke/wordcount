import re
import nltk
from collections import Counter
import click
import random


def make_html(path, common, total):

    colors = ['red', 'green', 'blue', 'cyan', 'orange', 'pink', 'teal', 'black', 'maroon']
    elements = []
    for k, v in common.items():
        font_size = 12 * int(round(float(v) / float(total) * 100))
        element = '<span style="font-size: {}px; color: {}; margin-right: 20px;">{}</span> '.format(
            font_size, random.choice(colors), k.encode('utf-8'))
        elements.append(element)

    #  write to file
    html_str = """
    <!doctype html>
      <html class="no-js" lang="">
        <head>
          <meta charset="utf-8">
          <meta http-equiv="x-ua-compatible" content="ie=edge">
          <title></title>
          <meta name="description" content="">
          <meta name="viewport" content="width=device-width, initial-scale=1">

          <link rel="apple-touch-icon" href="apple-touch-icon.png">
          <!-- Place favicon.ico in the root directory -->

        </head>
        <body style="text-align: center">
          <h1>Anna's Word Cloud</h1>
          <div style="margin: 20px; color: red; width: auto; border: 1px solid #888; padding: 20px;">
    """
    html_str += "".join(elements)
    html_str += """
          </div>
        </body>
      </html>
    """


    html_file = open(path, 'w')
    html_file.write(html_str)
    html_file.close()


@click.command()
@click.option('--path', default=None, help='Path to file.')
@click.option('--count', default=10, help='Number of results wanted.')
@click.option('--exclude', default=False, help='Exclude common small words.')
@click.option('--html', default=False, help='Generate html file with word cloud.')
def main(path, count, exclude, html):
    """Main."""
    exclusions = set()
    f = open(path, 'rb')
    text = f.read()
    text2 = unicode(text, errors='replace')
    tokens = nltk.word_tokenize(text2)
    if exclude:
        exclusions = set(
            ['a', 'and', 'or', 'this', 'is', 'the', 'be', 'of', 'to', 'that', 'as', 'are', 'in', 
            'on', 'for', 'not', 'by', 'which', 'has', 'their', 'et', 'al', 'it', 'al.'])
    nonPunct = re.compile('.*[A-Za-z0-9].*')
    filtered = [w for w in tokens if nonPunct.match(w) and w.lower() not in exclusions]
    counts = Counter(filtered)
    common = dict(Counter(counts).most_common(count))
    
    total = 0
    print "Anna's {} most common words: \n".format(count)
    i = 1
    for k, v in common.items():
        print "{}: {} ({})".format(i, k.encode('utf-8'), v)
        total += v
        i += 1
    
    #  make html file
    if html:
        make_html(path='index.html', common=common, total=total)


if __name__ == '__main__':
    main()