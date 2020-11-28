import os
import re
import lxml
import cchardet
import numpy as np
from collections import OrderedDict
import gensim



TOPIC_MODEL_FILE = '/data/expertsearch/lda_mallet_model'
CORPUS_DICTIONARY_FILE = '/data/expertsearch/corpus_dictionary'

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


