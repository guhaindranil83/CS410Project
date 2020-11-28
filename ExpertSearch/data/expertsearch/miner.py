import os
import re
import lxml
import cchardet
import numpy as np
from collections import OrderedDict
import gensim
import gensim.corpora as corpora
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, remove_stopwords, strip_tags, strip_numeric, strip_non_alphanum
from gensim.models import CoherenceModel, Phrases
from bs4 import BeautifulSoup

COMPILED_BIOS_DIR = '../compiled_bios'
FILTERS_PATH = '../'
TOPIC_MODEL_FILE = '/data/expertsearch/lda_mallet_model'
CORPUS_DICTIONARY_FILE = '/data/expertsearch/corpus_dictionary'
MALLET_PATH = '/data/expertsearch/mallet-2.0.8'

def get_top_words_from_query_topic(query):
    current_dir = os.getcwd()
    
    model = load_topic_model(current_dir + TOPIC_MODEL_FILE)
    corpus_dictionary = load_dictionary(current_dir + CORPUS_DICTIONARY_FILE)

    split_query = query.split(' ')

    topic_num = max(model[corpus_dictionary.doc2bow(split_query)], key=lambda x: x[1])[0]
    top_terms = [termscore[0].replace('_', ' ') for termscore in model.show_topic(topic_num)]

    yield top_terms

def load_topic_model(file_name):
    try :
        return gensim.utils.SaveLoad.load(file_name)
    except IOError as err:
        print(err)
    except:
        print("Something went wrong:", sys.exc_info()[0])

def load_dictionary(file_name):
    try:
        return gensim.utils.SaveLoad.load(file_name)
    except IOError as err:
        print(err)
    except:
        print("Something went wrong:", sys.exc_info()[0])

def get_array_from_file(filters_path):
    try:
        array_file = open(filters_path, 'r')
        array = re.split(' |\n|\t', array_file.read().lower())
        array_file.close()
        array = [arr.replace('\r', '') for arr in array if len(arr.replace('\r', '')) > 0]
        return set(array)
    except IOError as err:
        print(err)
    except:
        print("Something went wrong:", sys.exc_info()[0])

def iter_documents(top_directory, filters):
    custom_filter = [lambda x: x.lower(), strip_punctuation, remove_stopwords, strip_tags, strip_non_alphanum, strip_numeric]
    """Iterate over all documents, yielding a filtered document (=list of utf8 tokens) at a time."""
    for root, dirs, files in os.walk(top_directory):
        for file in filter(lambda file: file.endswith('.txt'), files):
            document = open(os.path.join(root, file)).read().lower() # read the entire document, as one big string
            soup = BeautifulSoup(document, "lxml")
            document = soup.get_text(separator='\n').split(' ') # remove html entities and tags
            document = preprocess_string(' '.join(document), custom_filter)
            document = [word for word in document if word not in filters]
            document = [word for word in document if len(word) > 4]
            
            yield document 
            

class CorpusContainer(object):
    def __init__(self, top_dir, filters_path):
        self.top_dir = top_dir
        filter_set = self.__construct_filter_set(filters_path) 
        self.docs = list(iter_documents(top_dir, filter_set))
        self.bigram = Phrases(self.docs, min_count=2)
        self.trigram = Phrases(self.bigram[self.docs], min_count=2)
        self.__append_bigrams_and_trigrams()
        self.dictionary = gensim.corpora.Dictionary(self.docs)
        self.dictionary.filter_extremes(no_below=10, no_above=.5, keep_n=30000) # check API docs for pruning params
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.docs]
        
    def __iter__(self):
        for tokens in iter_documents(self.top_dir, self.filters):
            yield self.dictionary.doc2bow(tokens)
            
    def __len__(self):
        return len(self.docs)
    
    def __construct_filter_set(self, filters_path):
        filters = get_array_from_file(filters_path + 'names.txt')
        filters.update(get_array_from_file(filters_path + 'unis'))
        filters.update(get_array_from_file(filters_path + 'urls'))
        filters.update(get_array_from_file(filters_path + 'emails'))
        #filters.update(get_array_from_file(filters_path + 'depts'))
        filters.update(get_array_from_file(filters_path + 'location'))
        filters.update(get_array_from_file(filters_path + 'unwanted_words.txt'))
        return filters
    
    
    def __append_bigrams_and_trigrams(self):
        for idx in range(len(self.docs)):
            bigrams = [bigram for bigram in self.bigram[self.docs[idx]] if bigram.count('_') == 1]
            trigrams = [trigram for trigram in self.trigram[self.bigram[self.docs[idx]]] if trigram.count('_') == 2]
        
            for token in bigrams:
                split_tokens = list(OrderedDict.fromkeys(token.split('_')))
                for tok in split_tokens:
                    self.docs[idx] = filter(lambda word: word != tok, self.docs[idx])
                self.docs[idx].append('_'.join(split_tokens))
                
            for token in trigrams:
                split_tokens = list(OrderedDict.fromkeys(token.split('_')))
                for tok in split_tokens:
                    self.docs[idx] = filter(lambda word: word != tok, self.docs[idx])
                self.docs[idx].append('_'.join(split_tokens))

if __name__ == '__main__':

    corpus_container = CorpusContainer(COMPILED_BIOS_DIR, FILTERS_PATH)
    ldamallet = gensim.models.wrappers.LdaMallet(MALLET_PATH, corpus=corpus_container.corpus, num_topics=22, id2word=corpus_container.dictionary)
    gensim.models.wrappers.LdaMallet.save(TOPIC_MODEL_FILE)
    corpus_container.dictionary.save(CORPUS_DICTIONARY_FILE)

