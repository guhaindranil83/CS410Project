import os
import re
import lxml
import cchardet
import numpy as np
from collections import OrderedDict
import gensim
import gensim.corpora as corpora
from ranker import load_ranker
from bs4 import BeautifulSoup


CORPUS_FILE = '/data/expertsearch/lda_corpus'
TOPIC_MODEL_FILE = '/data/expertsearch/lda_mallet_model'
CORPUS_DICTIONARY_FILE = '/data/expertsearch/corpus_dictionary'
BIOS_FILE = '/data/compiled_bios'
MODEL_FILES = '/data/expertsearch/model_files/'
INFERENCES = '/data/expertsearch/model_files/doctopics.txt'


def get_topics_from_many_documents(doc_names):
    """ A function that extracts a list of terms associated with each document's inferred topic.

    Parameters
    ----------
    doc_names: list
        A list of document filenames
    """
    relevant_terms = []
    for doc_name in doc_names:
        relevant_terms.append(get_topic_from_single_document(doc_name))

    return relevant_terms

def get_topic_from_single_document(doc_name):
    """ A function that extracts a list of terms associated with a document's inferred topic.

    Parameters
    ----------
    doc_name: str
        The document's filename
    """

    current_dir = os.getcwd()
    model = get_model()
    corpus = corpora.MmCorpus(current_dir + CORPUS_FILE)
    doc_id = int(doc_name.replace('.txt', ''))
    print(doc_id)
    print(doc_id >= len(corpus))
    if doc_id >= len(corpus): # Do inference on new document

        doc = get_document(current_dir + BIOS_FILE, doc_name)
        corpus_dictionary = load_dictionary(current_dir + CORPUS_DICTIONARY_FILE)

        topic_num = max(model[corpus_dictionary.doc2bow(doc)], key=lambda x: x[1])[0]
    else: 

        with open(current_dir + INFERENCES) as f:
            for i, line in enumerate(f):
                if i == doc_id:
                    topic_distribution = list(map(float,line.replace('\n','').split('\t')[2:]))
                    topic_num = topic_distribution.index(max(topic_distribution))

    return clean_topic_terms(model.show_topic(topic_num))

def get_top_words_from_query_topic(query):
    """ A function that extracts a list of terms associated with a query's inferred topic.

    Parameters
    ----------
    query: str
        The query
    """

    current_dir = os.getcwd()
    
    model = get_model()

    corpus_dictionary = load_dictionary(current_dir + CORPUS_DICTIONARY_FILE)

    split_query = query.split(' ')

    topic_num = max(model[corpus_dictionary.doc2bow(split_query)], key=lambda x: x[1])[0]
    topic = model.show_topic(topic_num)
    top_terms = clean_topic_terms(topic)

    yield top_terms

def clean_topic_terms(topic):
    """ A function that replaces '_' with ' ' for each term in a list of top-10 terms associated with a topic cluster.

    Parameters
    ----------
    topic: list
        The top-10 terms associated with a topic
    """
    return[termscore[0].replace('_', ' ') for termscore in topic]

def get_document(top_directory, doc_name):
    """ Processes specified document to yield a list of utf-8 tokens.

    Parameters
    ----------
    top_directory: str
        Path to folder containing documents

    doc_name: str
        Filename for document
    """

    fp = open(os.path.join(top_dir, file))
    document = fp.read().lower()  # read the entire document, as one big string
    
    #soup = BeautifulSoup(document, "lxml")
    #document = soup.get_text(separator='\n').split(' ')
    document = gensim.utils.simple_preprocess(' '.join(document))
    document = [word for word in document if len(word) > 4]

    fp.close()
    return document

def get_model():
    """ Gets a loaded topic model. """
    current_dir = os.getcwd()
    model = load_topic_model(current_dir + TOPIC_MODEL_FILE)
    model.prefix = current_dir + MODEL_FILES
    return model

def load_topic_model(file_name):
    """ Attempts to load a topic model from disk.

    Parameters
    ----------
    file_name: str
        Name of the file that holds the topic model
    """
    try :
        return gensim.utils.SaveLoad.load(file_name)
    except IOError as err:
        print(err)
    except:
        print("Something went wrong:", sys.exc_info()[0])

def load_dictionary(file_name):
    """ Attempts to load a gensim dictionary from disk.

    Parameters
    ----------
    file_name: str
        Name of the file that holds the dictionary
    """

    try:
        return gensim.utils.SaveLoad.load(file_name)
    except IOError as err:
        print(err)
    except:
        print("Something went wrong:", sys.exc_info()[0])


