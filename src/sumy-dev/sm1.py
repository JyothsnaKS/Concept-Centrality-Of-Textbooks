#Import library essentials
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in

file1 = "4.txt" #name of the plain-text file
file2 = "h.txt"
parser1 = PlaintextParser.from_file(file1, Tokenizer("english"))
parser2 = PlaintextParser.from_file(file2, Tokenizer("english"))

#print parser.document
summarizer = LexRankSummarizer()

summary = summarizer(parser1.document,parser2.document,5) #Summarize the document with 5 sentences


for sentence in summary:
    print sentence
    

