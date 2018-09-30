from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
import nltk

from sumy._compat import to_unicode
import re

def path(p):
    global pdfpath
    pdfpath = p
    create_addon_list()

def create_addon_list():
    global l
    
    # Open a PDF file.
    fp = open(pdfpath, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    document = PDFDocument(parser, " ")

    l=list()
    i=0
    # Get the outlines of the document.
    outlines = document.get_outlines()

    for (level,title,dest,a,se) in outlines:
         i+=1

         temp=list()
         #title = to_unicode(title).strip()
         #title = re.sub(u"(\u2018|\u2019)", "'", title)
         temp.append((str)(level))
         temp.append((title.encode('utf-8')).strip('\x00'))
         #temp.append(title)
         l.append(temp)
         #print temp
    #print l
     
