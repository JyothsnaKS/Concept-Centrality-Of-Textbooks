# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import math

try:
    import numpy
except ImportError:
    numpy = None

from ._summarizer import AbstractSummarizer
from .._compat import Counter


class LexRankSummarizer(AbstractSummarizer):
    """
    LexRank: Graph-based Centrality as Salience in Text Summarization
    Source: http://tangra.si.umich.edu/~radev/lexrank/lexrank.pdf
    """
    threshold = 0.1
    epsilon = 0.1
    _stop_words = frozenset()

    @property
    def stop_words(self):
        return self._stop_words

    @stop_words.setter
    def stop_words(self, words):
        self._stop_words = frozenset(map(self.normalize_word, words))


    def __call__(self, document, sentences_count):
        self._ensure_dependencies_installed()

        #print (LexRankSummarizer._stop_words)

        fp=open('C:/Python27/sumy-dev/sumy/data/stopwords/english.txt','r')
        txt=fp.read()
        self._stop_words=txt.splitlines()

        #print (self._stop_words)

        sentences_words = [self._to_words_set(s) for s in document.sentences]
        if not sentences_words:
            return tuple()

        tf_metrics = self._compute_tf(sentences_words)
        idf_metrics,rel_sq = self._compute_idf(sentences_words,tf_metrics)

        matrix = self._create_matrix(sentences_words, self.threshold, tf_metrics, idf_metrics)
        matrix2 = self._create_rel_matrix(sentences_words, rel_sq)
        
        scores = self.power_method((matrix+matrix2)/2, self.epsilon)
        scores_a = self.power_method(matrix, self.epsilon)
        ratings = dict(zip(document.sentences, scores))
        #print(matrix)
        #print(matrix2)
        #print(matrix+matrix2)

        '''
        print (scores_a)
        print ('\n\n')
        print (rel_sq)
        print ('\n\n')
        print(scores_a+rel_sq)
        print ('\n\n')
        print (scores)
        '''

        print(scores_a.sum())

        return self._get_best_sentences(document.sentences, sentences_count, ratings)

    
    def _ensure_dependencies_installed(self):
        if numpy is None:
            raise ValueError("LexRank summarizer requires NumPy. Please, install it by command 'pip install numpy'.")

    def _to_words_set(self, sentence):
        words = map(self.normalize_word, sentence.words)
        #print ([self.stem_word(w) for w in words if w not in self._stop_words])
        
        return [self.stem_word(w) for w in words if w not in self._stop_words]

    def _compute_tf(self, sentences):
        tf_values = map(Counter, sentences)
        
        tf_metrics = []
        for sentence in tf_values:
            metrics = {}
            max_tf = self._find_tf_max(sentence)

            for term, tf in sentence.items():
                metrics[term] = tf / max_tf

            tf_metrics.append(metrics)
        return tf_metrics


    def _find_tf_max(self,terms):
        return max(terms.values()) if terms else 1

   
    def _compute_idf(self,sentences,tf_metrics):
        idf_metrics = {}
        
        rel_sq=[]
        t=0
        i=0
        idf_metrics2={}
        s=['computer', 'virus','malware']
        
        sentences_count = len(sentences)

        #print (tf_metrics)

        for sentence in sentences:
            t=0
            for term in sentence:
                if term not in idf_metrics:
                    n_j = sum(1 for s in sentences if term in s)
                    idf_metrics[term] = math.log(sentences_count / (1 + n_j))
                    
                if term.lower() in s:
                    idf_metrics2[term] = math.log((sentences_count+1) / (0.5 + n_j))
                    t+=idf_metrics2[term]*math.log(2)*math.log(tf_metrics[i][term]+1)
                
            rel_sq.append(t)            
            i+=1            
        #print (idf_metrics)               
        return idf_metrics,rel_sq
    

    def _create_matrix(self, sentences, threshold, tf_metrics, idf_metrics): # cosine matrix
        """
        Creates matrix of shape |sentences|×|sentences|.
        """
        # create matrix |sentences|×|sentences| filled with zeroes
        sentences_count = len(sentences)
        matrix = numpy.zeros((sentences_count, sentences_count))# returns an array of the specified size filled with zeroes
        degrees = numpy.zeros((sentences_count, )) # diagonal matrix --> degree of the nodes

        # sentence1 --> list of words in the sentence
        # tf1 --> dictionary of words and their frequency
        
        for row, (sentence1, tf1) in enumerate(zip(sentences, tf_metrics)):
            for col, (sentence2, tf2) in enumerate(zip(sentences, tf_metrics)):
                matrix[row, col] = self._compute_cosine(sentence1, sentence2, tf1, tf2, idf_metrics) # sentence similarity

                if matrix[row, col] > threshold:
                    matrix[row, col] = 1.0
                    degrees[row] += 1 # degree is incremented since a new edge is formed the 2 sentences
                else:
                    matrix[row, col] = 0
        #print (matrix)
        #print (degrees)
        
        for row in range(sentences_count):
            for col in range(sentences_count):
                if degrees[row] == 0:
                    degrees[row] = 1

                matrix[row][col] = matrix[row][col] / degrees[row]
                
        #print (matrix)
        return matrix

    def _create_rel_matrix(self, sentences, rel_sq): 
        """
        Creates matrix of shape |sentences|×|sentences|.
        """
        sentences_count = len(sentences)
        matrix = numpy.zeros((sentences_count, sentences_count),dtype=float)
        
        for row in range(0,sentences_count):
            for col in range(0,sentences_count):
                matrix[row, col] = rel_sq[col]
 
        for row in range(sentences_count):
            sum_row=matrix[row].sum()
            if sum_row==0:
                sum_row=1.0
            for col in range(sentences_count):
                matrix[row][col] = matrix[row][col] / sum_row
                
        return matrix
    
    
    def _compute_cosine(self,sentence1, sentence2, tf1, tf2, idf_metrics):
        common_words = frozenset(sentence1) & frozenset(sentence2) # set intersection

        numerator = 0.0
        for term in common_words:
            numerator += tf1[term]*tf2[term] * idf_metrics[term]**2

        denominator1 = sum((tf1[t]*idf_metrics[t])**2 for t in sentence1)
        denominator2 = sum((tf2[t]*idf_metrics[t])**2 for t in sentence2)

        if denominator1 > 0 and denominator2 > 0:
            return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))
        else:
            return 0.0

   
    def power_method(self,matrix, epsilon): # to compute LexRank score
        transposed_matrix = matrix.T
        sentences_count = len(matrix)
        p_vector = numpy.array([1.0/sentences_count] * sentences_count)
        #p_vector = numpy.array([rel_sq] * sentences_count,dtype=float)
        #p_vector/=p_vector.sum()
        lambda_val = 1.0

        while lambda_val > epsilon:
            next_p = numpy.dot(transposed_matrix, p_vector)
            lambda_val = numpy.linalg.norm(numpy.subtract(next_p, p_vector))
            p_vector = next_p

        return p_vector
