import re
import nltk
from collections import Counter
import click


@click.command()
@click.option('--path', default=None, help='Path to file.')
@click.option('--count', default=10, help='Number of results wanted.')
@click.option('--exclude', default=False, help='Exclude common small words.')
def main(path, count, exclude):
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

    print "Anna's {} most common words: \n".format(count)
    i = 1
    for k, v in common.items():
        print "{}: {} ({})".format(i, k.encode('utf-8'), v)
        i += 1

if __name__ == '__main__':
    main()