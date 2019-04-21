import scraperwiki, urllib3
from bs4 import BeautifulSoup

def send_Request(url):
#Get content, regardless of whether an HTML, XML or PDF file
    pageContent = urllib3.urlopen(url)
    return pageContent

def process_PDF(fileLocation):
#Use this to get PDF, covert to XML
    pdfToProcess = send_Request(fileLocation)
    pdfToObject = scraperwiki.pdftoxml(pdfToProcess.read())
    return pdfToObject

def parse_HTML_tree(contentToParse):
#returns a navigatibale tree, which you can iterate through
    soup = BeautifulSoup(contentToParse)
    return soup

pdf = process_PDF('11800.pdf')
pdfToSoup = parse_HTML_tree(pdf)
soupToArray = pdfToSoup.findAll('text')
for line in soupToArray:
    print(line)