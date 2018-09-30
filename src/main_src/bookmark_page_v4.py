#from __future__ import unicode_literals
from pyPdf import PdfFileReader, PdfFileWriter, PdfFileReader
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
import pyPdf
import PyPDF2
import nltk
import codecs
import io


def _setup_page_id_to_num(pdf, pages=None, _result=None, _num_pages=None):
    if _result is None:
        _result = {}
    if pages is None:
        _num_pages = []
        pages = pdf.trailer["/Root"].getObject()["/Pages"].getObject()
    t = pages["/Type"]
    if t == "/Pages":
        for page in pages["/Kids"]:
            _result[page.idnum] = len(_num_pages)
            _setup_page_id_to_num(pdf, page.getObject(), _result, _num_pages)
    elif t == "/Page":
        _num_pages.append(1)
    return _result

def outlines_pg_zoom_info(outlines, pg_id_num_map, result=None):
    if result is None:
        result = dict()
    if type(outlines) == list:
        for outline in outlines:
            result = outlines_pg_zoom_info(outline, pg_id_num_map, result)
    elif type(outlines) == pyPdf.pdf.Destination:
        title = outlines['/Title']
        result[title.split()[0]] = dict(title=outlines['/Title'],page=(pg_id_num_map[outlines.page.idnum]+1))
    return result


# main

def bkpage(pdf_name):
    
    f =open(pdf_name,'rb')
    pdf = PdfFileReader(f)

    # map page ids to page numbers
    pg_id_num_map = _setup_page_id_to_num(pdf)
    outlines = pdf.getOutlines()
    bookmarks_info = outlines_pg_zoom_info(outlines, pg_id_num_map)
    
    #print bookmarks_info
    page_title={}

    for key in bookmarks_info.keys():
        a=bookmarks_info[key]
        page_title[a['title'].encode('utf-8')]=int(a['page'])
    #print page_title

    a=sorted(page_title.items(), key=lambda (k, v):(v, k))
    #print a
    l=[]
    title_tokens=[]

    for x in a:
        l.append(x[0])
        title_tokens.append(x[0].split())
        #print x[1], ":", x[0]

    return (page_title,l,title_tokens)


