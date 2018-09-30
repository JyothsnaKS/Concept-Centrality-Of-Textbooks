# ConceptCentralityOfTextbooks

This repository consists of the implementation for generating graphical visualization of e-books using the concept of centrality

A textbook is a collection of concepts and principles of a selected topic or course. They are one of the important resources available to readers. Readers have a tough time when it comes to selecting a book from thousands of them written on the same subject.

We hardly ever find a single book which explains all the concepts without deviating from what is actually to be covered. This makes the readers look at various reference books in search of content which is central to the concept / topic to be covered. It is also not unusual for readers to reject textbooks simply because of what they are collections of large amount of data. These textbooks may fail to arouse reader's interest. Readers may find it difficult to understand the relevance of so much data to what they were actually expecting from the book. Readers would want to be suggested with the best books that are available for a particular subject /course.

In order to solve the above mentioned problems, we will be mainly working on the concept of centrality. Graphical visualisation will be created for a textbook which will give the reader percentage of centrality for various topics covered in the book. This will help the reader to select the topic/s which he would like to study from the book. He could choose to refer a different book for the other topics.

Similarly, the centrality percentages of different books can be computed and compared to suggest the best books (on a specific subject) to the reader. A dependency graph generated will suggest readers which topics should be covered before studying particular topics. Centrality scores of the textbooks will help readers pick different books to study each of those topics.

## What we are not addressing?
This implementation does not delve into deep learning algorithms to model the topic relevance of various textbooks.

## Assumption
1. Sentences which are similar to each other sentence in a cluster are more salient or central to the topic. 
2. Words present in the glossary are significant to the content of the book.
3. Sentences with more number of terms from the glossary are more significant to the subject.
4. Heading of the topics and subtopics are relevant to the book title.
5. EBooks are available in Pdf format that have bookmarks.
6. Glossary is present in the EBook.

## Tools Required
1. Python
2. For data extraction, ‘pdfminer’ is used to get outlines i.e. The title, level and subtopics of the book as well as convert pdf to text. 
3. ‘PyPDF’ is used to extract the page number from the bookmarks. 
4. ‘nltk’ is used to perform various text mining functions such as stemming and removal of stop words.
5. Data processing tools used to calculate centrality and relevance of each topic are ‘numpy’, ‘scipy’, ‘sumy’ and ‘n-grams’.
6. Data representation tools used to graphically represent the organization and content level of the text include ‘MatPlotLib’, and ‘Networkx’. ‘ete3’ is used for the generating the tree of table of contents in the book.

## Mathematical concepts involved 

### Graph theory

A graph is a representation of a set of objects (vertices) where some pairs of objects are connected by links (edges).
Mathematically, a graph is an ordered pair G = (V, E) comprising a set V of vertices, nodes or points together with a set E of edges, arcs or lines, which are 2-element subsets of V.

Sentence graph for each topic in the book is created to calculate its centrality. This graph will be an undirected graph (a graph in which edges have no orientation. The edge (x, y) is identical to the edge (y, x). The maximum number of edges in an undirected graph without a loop is n (n − 1)/2)

For each textbook, a graphical visualisation will be given using a tree which is an acyclic connected graph.

### TF-IDF
https://en.wikipedia.org/wiki/Tf%E2%80%93idf

### Cosine Similarity
https://en.wikipedia.org/wiki/Cosine_similarity

### Lex Rank formula

Lex Rank is an algorithm based on Google’s Page Rank algorithm. While the Page Rank algorithm is used to rank webpages, Lex Rank algorithm is used as a measure in network analysis to analyse text. It is in actuality a variation of eigenvector centrality. It has been found to be more efficient in in calculating the importance of sentences and thus we have chosen to use it. It assigns a numerical weighting of by taking the result of the sentences own PageRank divided by the number of similar sentences (Number of outbound links for a directed graph).

## References
1. Text Summarization using Centrality Concept
2. LexRank: Graph-based Lexical Centrality as Salience in Text Summarization
3. Research on Extension LexRank in Summarization for Opinionated Texts
4. Automatic Topic detection from Learning Material: An Ontological Approach
5. Using Random Walks for Question-focused Sentence Retrieval
