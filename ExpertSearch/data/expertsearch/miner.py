import os
import re
import lxml
import cchardet
import numpy as np
from collections import OrderedDict
import gensim
from ranker import load_ranker
from bs4 import BeautifulSoup



TOPIC_MODEL_FILE = '/data/expertsearch/lda_mallet_model'
CORPUS_DICTIONARY_FILE = '/data/expertsearch/corpus_dictionary'
BIOS_FILE = '/data/compiled_bios'
MODEL_FILES = '/data/expertsearch/model_files/'

def get_topics_from_many_documents(doc_names):

    for doc_name in doc_names:
        topic = get_topic_from_single_document(doc_name)

        yield topic

def get_topic_from_single_document(doc_name):
    current_dir = os.getcwd()

    doc = list(iter_documents(current_dir + BIOS_FILE, doc_name).next())
    corpus_dictionary = load_dictionary(current_dir + CORPUS_DICTIONARY_FILE)
    model = get_model()

    topic_num = max(model[corpus_dictionary.doc2bow(doc)], key=lambda x: x[1])[0]


    return clean_topic_terms(model.show_topic(topic_num))

def get_top_words_from_query_topic(query):
    current_dir = os.getcwd()
    
    model = get_model()
    corpus_dictionary = load_dictionary(current_dir + CORPUS_DICTIONARY_FILE)

    split_query = query.split(' ')

    topic_num = max(model[corpus_dictionary.doc2bow(split_query)], key=lambda x: x[1])[0]
    topic = model.show_topic(topic_num)
    top_terms = clean_topic_terms(topic)

    yield top_terms

def clean_topic_terms(topic):
    return[termscore[0].replace('_', ' ') for termscore in topic]

def iter_documents(top_directory, doc_name):
    """Iterate over all documents, yielding a document (=list of utf8 tokens) at a time."""
    for root, dirs, files in os.walk(top_directory):
        for file in filter(lambda file: file == doc_name, files):
            document = open(os.path.join(root, file)).read().lower()  # read the entire document, as one big string
            soup = BeautifulSoup(document, "lxml")
            document = soup.get_text(separator='\n').split(' ')
            document = gensim.utils.simple_preprocess(' '.join(document))
            document = [word for word in document if len(word) > 4]

            yield document

def get_model():
    current_dir = os.getcwd()
    model = load_topic_model(current_dir + TOPIC_MODEL_FILE)
    model.prefix = current_dir + MODEL_FILES
    return model

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


