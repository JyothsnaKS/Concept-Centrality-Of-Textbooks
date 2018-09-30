#to calculate centrality score
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in
from sumy._compat import to_unicode

#to read pdf
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
import bookmark_page_v4
import nltk
import addonv2
import codecs
import os,io

#to create a graph
import networkx as nx

#regex
import re

from fuzzywuzzy import fuzz


def check(str_a,str_b):
     for i in range(0,len(q)-1):
          if q[i][1]==str_a and q[i+1][1]==str_b:
               if (int)(q[i][0])+1 == (int)(q[i+1][0]):
                    print 'Add a node here'
                    return 1


def func(txt_tokens,t,l,tokens):
     flag=0
     k=0
     r=''
     for i in range(l,l+len(tokens)):
          r=''
          if txt_tokens[i]==tokens[0]:
               r+=txt_tokens[i]

               for k in range(1,len(tokens)):
                    i+=1
                    r+=' '+txt_tokens[i]
                         
               #print ''.join(r),' '.join(tokens),'   ',fuzz.ratio(''.join(r),' '.join(tokens))         
               #print txt_tokens[i+1],'  out k'
               
               if len(tokens)>3 and fuzz.ratio(''.join(r),' '.join(tokens))>92:
                    #print 'works!!'
                    if not txt_tokens[i+1].isdigit() or not txt_tokens[i+1][0].isalpha():
                         #print 'x print'
                         return 0
                    else:
                         #print 'print'
                         return 1
               elif len(tokens)<=3 and fuzz.ratio(r,' '.join(tokens))==100:
                    if not txt_tokens[i+1].isdigit() or not txt_tokens[i+1][0].isalpha():
                         #print 'x print'
                         return 0
                    else:
                         #print 'print'
                         return 1
               else:
                    return 1
                    
                    
          else:
               return 1

def convert_page_to_txt(path, st, en):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    fp = file(path, 'rb')
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
  
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set(range(st-1, en))
   

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def  remove_badtag(i):
     
     no=len(net_graph.successors(q[i][1]))

     #print 'i - ',i
     #print 'no - ',no

     return i+no
	
def get_data(badtags):
     # i is a variable used to iterate over the list of titles
     i=-1
     #while i<len(q)-1:
     while i<83:
             i+=1
             print "\n***********************************************************************************"
             print i
             if i== len(q)-1:
                  break
             pageno=(int)(q[i][2])
             endpageno=(int)(q[i+1][2])
             title_tokenscopy=q[i][1].split()

             if q[i][1].lower() in badtags:
                  
                   print q[i][1],' - skipped'
                   i=remove_badtag(i)
                   continue 
            
             nxttitle_tokenscopy=q[i+1][1].split()
             found=0
             txt_tokens=[]
             k=0
        
             text = convert_page_to_txt(pdfname,pageno,endpageno)
             
             text = to_unicode(text).strip()
             
             text = re.sub(u'(\u2018|\u2019|\u201c|\u201d)', "", text)
             text = re.sub(u'cid:10|cid:9|cid:8|cid:7|cid:13|cid:14|cid:15', "", text)
             text = re.sub(u'\ufb01', "fi", text)
             text = re.sub(u'\ufb02', "fl", text)
             text = re.sub(u'\xa0', ' ', text)
             
             text = text.replace('()','')
             
             txt_tokens=text.split()

             for a in range (0,len(txt_tokens)-1):
                 r=''
                 #print "-------", txt_tokens[a], title_tokenscopy[0]
                 if txt_tokens[a]==title_tokenscopy[0]:
                     r+=txt_tokens[a]
                     for k in range(1,len(title_tokenscopy)):
                             a+=1
                             r+=' '+txt_tokens[a]


                     k+=1
                     #print ''.join(r),q[i][1],'   ',fuzz.ratio(''.join(r),q[i][1])


                     if (len(title_tokenscopy)>3 and fuzz.ratio(''.join(r),q[i][1])>92) or (len(title_tokenscopy)<=3 and fuzz.ratio(''.join(r),q[i][1])==100):
                             #print txt_tokens[a:a+11]
                             if not txt_tokens[a+1].isdigit() and (txt_tokens[a+1][0].isalpha() or '.' in txt_tokens[a+1]):
                                  eflag=0
                                  add_node = 0
                                  no_lines=1
                                  print q[i][1]
                                  print 'Match Found'
                                  string=""
                                  a+=1
                                  for y in range(a,len(txt_tokens)):
                                          if func(txt_tokens,txt_tokens[y],y,nxttitle_tokenscopy)==1:
                                                  #print txt_tokens[y]
                                                  string+=txt_tokens[y]+" "
                                          else:
                                                  found=1
                                                  break
                                  # to remove exact repitition of title in content caused due to the problem with the pdf format        
                                  for z in net_graph.predecessors(q[i][1])+net_graph.successors(q[i][1]):
                                       print z
                                       string=''.join(string.split(z))

                                  string=''.join(string.split(q[i][1]))
                                  
                                  if not string.isspace() and string!='' :
                                       add_node = check(q[i][1],q[i+1][1])
                                  else:
                                       eflag=1
                                  
                                  parser1 = PlaintextParser.from_file(string, Tokenizer("english"))
                                  parser2 = PlaintextParser.from_file(q[i][1]+book_name+' '+' '.join(net_graph.predecessors(q[i][1])+net_graph.successors(q[i][1])), Tokenizer("english"))

                                  #print parser.document
                                  summarizer = LexRankSummarizer()

                                  lr_score = summarizer(parser1.document,parser2.document,5)

                                  #print ' '.join(net_graph.predecessors(q[i][1])+net_graph.successors(q[i][1]))

                                  no_lines = len(string.split('.'))
                                  #print no_lines
                                  
                                  if add_node:
                                       graph_list.append([(int)(q[i][0]),q[i][1],0])
                                       graph_list.append([(int)(q[i][0])+1,'Chapter Introduction',lr_score/no_lines])
                                  else:
                                       if eflag==1:
                                           lr_score=0
                                       graph_list.append([(int)(q[i][0]),q[i][1],lr_score/no_lines])

                                  #print q[i][1]+book_name+' '+' '.join(net_graph.predecessors(q[i][1])+net_graph.successors(q[i][1]))
                                  print string
                                  #print lr_score
                                  #print lr_score/no_lines                                 
                             
                     if found==1:
                              break
                         
             #print [z[1] for z in graph_list]
                     
             if q[i][0] == '1' and q[i][1] not in [z[1] for z in graph_list]:
                  print 'added'
                  graph_list.append([(int)(q[i][0]),q[i][1],0])
                       
              
                         
     #print i ,"last"
     
     #for the last bookmark
     lastindex=len(q)-1
     #print skip,' last'
     if q[i][1].lower() in badtags:
         print q[i][1],' - skipped'
     if i==lastindex and q[i][1].lower() not in badtags:
          
          fp=open(pdfname,"rb")
          pdf = PdfFileReader(fp)
          totalPages = pdf.getNumPages()
          pageno=page_title[(str)(q[lastindex][1])]
          title_tokenscopy=q[i][1].split()
          text=convert_page_to_txt(pdfname,pageno,totalPages)
          txt_tokens=text.split()
          for a in range(0,len(txt_tokens)):
               #print"entry 1"
               found=0
               if txt_tokens[a]==title_tokenscopy[0]:
                    #print "entry entry"
                    k=0
                    for k in range(1,len(title_tokenscopy)):
                         #print "entry 2"
                         a+=1
                         if txt_tokens[a]==title_tokenscopy[k]:
                              #print "entry 3"
                              continue
                         else:
                              #print "entry 4"
                              break
                         #if len(titlee_tokens)
                         #k+=1
                    print k
                    if k+1==len(title_tokenscopy) or (len(title_tokenscopy)==1 and k==1):
                         if not txt_tokens[a+1].isdigit() and txt_tokens[a+1][0].isalpha():
                              print 'Match Found'
                              found=1
                              string=""
                              a+=1
                              for y in range(a,len(txt_tokens)):
                                   string+=txt_tokens[y]+" "
                              print string
                              print("\t\t********************************************************************************************************\n")
                         if found:
                              print"the end"
                              break
                      
     for i in range(0,len(graph_list)):
          print graph_list[i]
     #return graph_list
     
def gFunc2(l):
     net_graph.add_node(book_name)
     net_graph.add_node(l[0][1])
     for i in range(1,len(q)):
               if l[i][0] >l[i-1][0]:
                    #print l[i][1],i,'sub','  -->  ',l[i-1][1]
                    net_graph.add_node(l[i][1])
                    net_graph.add_edge(l[i-1][1],l[i][1])
               elif  l[i][0] <= l[i-1][0] and l[i][0]!='1':
                    s=str((int)(l[i][0])-1)
                    for j in range(i-1,0,-1):
                         if l[j][0]!=s:
                              j-=1
                         else:
                              #print l[i][1],i,'seq','  -->  ',l[j][1]
                              net_graph.add_node(l[i][1])
                              net_graph.add_edge(l[j][1],l[i][1])
                              break
                              
               else :
                    #print l[i][1],i,'root'
                    net_graph.add_node(l[i][1])
                    net_graph.add_edge(book_name,l[i][1])

     
def accept_name(pn,bn):
    
    global pdfname,book_name
    pdfname = pn
    book_name = bn
    create_list()

def create_list():

    global page_title,l,title_tokens,net_graph,graph_list,q,badtags

    addonv2.path(pdfname)
    page_title,l,title_tokens = bookmark_page_v4.bkpage(pdfname)
    badtags = ['cover','notes and further reading''title page','copyright page','contents','new to the third edition','review questions','laboratory exercises','epilogue: algorithms that run forever','brief contents','about the authors','exercises','solved exercises','about the author','preface','selected bibliography','acknowledgments','references','index','brief contents','foreword','bibliography','table of contents','foreword','appendix','epilogue','about the cd']                          

    net_graph=nx.DiGraph()
    graph_list=list()

    for i in range(0,len(badtags)):
     badtags[i].encode('utf-8')
    q=list()
    k=-1

    for i in range(0,len(addonv2.l)):
     flag=0
     for j in range(0,len(l)):
          
          if addonv2.l[i][1]==l[j] and addonv2.l[i][0]!='3':
               k+=1
               t=list()
               t.extend([addonv2.l[i][0],addonv2.l[i][1],page_title[addonv2.l[i][1]]])
               print t,' ',k
               q.append(t)
               flag=1
     if flag==0:
          if int(addonv2.l[i][0])==1:
               t=list()
               t.extend([addonv2.l[i][0],addonv2.l[i][1],""])
               q.append(t)
               
    for i in range(0,len(q)-1):
     if q[i][2]=="":
          q[i][2]=q[i+1][2]        

    for i in range(0,len(q)):
        q[i][1]=to_unicode(q[i][1]).strip()
        q[i][1] = re.sub(u"(\u2018|\u2019|\u201c|\u201d)", "", q[i][1])
        q[i][1] = re.sub(u"\xa0", " ", q[i][1])
        print q[i],i
       
    print len(q)

    gFunc2(q)
    get_data(badtags)



