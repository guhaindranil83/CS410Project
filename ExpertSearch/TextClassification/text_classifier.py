import argparse
import pprint
import smart_open
from gensim.models import doc2vec
from gensim import utils
from data_handler import *
from sklearn.metrics import accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression


data_handler = DataHandler()

tags_index = {
    TAG_TEST: 0,
    TAG_FACULTY: 1,
    TAG_ALEXA: 2
}


def add_parser_arguments(parser):
    parser.add_argument('-d', '--datagen', action='store_true', help='Add new training and test data')
    parser.add_argument('-t', '--train', action='store_true', help='Train model before classify task')


class TextClassifier():

    _mode = MODE_TRAIN_MODEL
    _datagen = False

    def __init__(self, train_mode, datagen):
        self._mode = MODE_TRAIN_MODEL if train_mode else MODE_LOAD_MODEL
        self._datagen = datagen

    def read_test_corpus(self, file_name):
        with smart_open.open(file_name, encoding='iso-8859-1') as f:
            lines = f.readlines()
            for line in lines:
                # preprocess each doc
                tokens = utils.simple_preprocess(line)
                yield doc2vec.TaggedDocument(tokens[1:], [tags_index[TAG_TEST]])

            # for i, line in enumerate(f):
            #     # preprocess each doc
            #     tokens = utils.simple_preprocess(line)
            #     yield doc2vec.TaggedDocument(tokens, [i])

    def read_train_corpus(self, file_name):
        train_corpus = []
        with smart_open.open(file_name, encoding='iso-8859-1') as f:
            lines = f.readlines()
            for line in lines:
                # preprocess each doc
                tokens = utils.simple_preprocess(line)
                tag_name = tokens[0]
                # yield doc2vec.TaggedDocument(tokens[1:], [tags_index[tag_name]])
                train_corpus.append(doc2vec.TaggedDocument(tokens[1:], [tags_index[tag_name]]))
        return train_corpus

    def vector_for_learning(self, model, input_docs):
        tags, feature_vectors = zip(*[(doc.tags[0], model.infer_vector(doc.words, steps=20)) for doc in input_docs])
        return tags, feature_vectors

    def get_key_from_value(self, dict, value):
        for k, v in dict.items():
            if v == value:
                return k

    def get_doc_from_corpus(self, doc_idx, corpus_file):
        with open(corpus_file, 'r') as f:
            lines = f.readlines()
            return lines[doc_idx][1:]

    def classify_directory_urls(self):
        open(CLASSIFIED_DIRECTORY_URLS_FILE, 'w').close()

        # add new training and test data if _datagen is true
        if self._datagen or not (os.path.exists(TRAIN_DATASET_FILE) or os.path.exists(TEST_DATASET_FILE)):
            data_handler.prepare_data_source()
            data_handler.prepare_corpus(DATA_TYPE_TRAINING)
            data_handler.prepare_corpus(DATA_TYPE_TESTING)

        # read the train corpus
        # train_corpus = list(self.read_train_corpus(TRAIN_DATASET_FILE))
        train_corpus = self.read_train_corpus(TRAIN_DATASET_FILE)
        # print a sample of the train corpus
        # pprint.pprint(train_corpus[1:5])

        if self._mode == MODE_LOAD_MODEL and os.path.exists('d2v.model'):
            # load the saved model
            model = doc2vec.Doc2Vec.load('d2v.model')
        else:
            # if self._mode == MODE_TRAIN_MODEL or not os.path.exists('d2v.model'):
            # build and train the model
            model = doc2vec.Doc2Vec(vector_size=100, min_count=2, epochs=50)
            model.build_vocab(train_corpus)
            model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)

            # save the model
            model.save('d2v.model')

        # read the test corpus
        test_corpus = list(self.read_test_corpus(TEST_DATASET_FILE))
        # print a sample of the test corpus
        # pprint.pprint(test_corpus[:2])

        y_train, X_train = self.vector_for_learning(model, train_corpus)
        y_test, X_test = self.vector_for_learning(model, test_corpus)
        # logreg = LogisticRegression(n_jobs=1, C=1e5)
        logreg = LogisticRegression(solver='liblinear', n_jobs=1, C=1e5)
        logreg.fit(X_train, y_train)
        y_pred = logreg.predict(X_test)

        # now save all the classified directory urls to the file
        with open(CLASSIFIED_DIRECTORY_URLS_FILE, 'w') as fo:
            with open(TEST_URLS_FILE, 'r') as fi:
                lines = fi.readlines()
                for i in range(len(lines)):
                    test_url = lines[i].strip()
                    label = self.get_key_from_value(tags_index, y_pred[i])
                    print "Label: ", label, ", URL: ", test_url
                    if label == TAG_FACULTY and self.get_doc_from_corpus(i, TEST_DATASET_FILE) != ERROR_CONTENT:
                        fo.write(test_url)
                        fo.write('\n')

            # also save the training directory urls
            with open(FACULTY_DIR_TRAIN_URLS_FILE, 'r') as fi:
                lines = fi.readlines()
                for i in range(len(lines)):
                    line = lines[i].strip()
                    if self.get_doc_from_corpus(i, TRAIN_DATASET_FILE) != ERROR_CONTENT:
                        line_parts = line.split()
                        if len(line_parts) > 1:
                            train_url = line_parts[1]
                            fo.write(train_url)
                            fo.write('\n')

    def classify_faculty_urls(self):
        pass


if __name__ == '__main__':
    # Run it as:
    #
    # To add new train/test data and train the model
    # python ./text_classifier.py -t -d
    #
    # For subsequent runs to do only classification
    # python ./text_classifier.py

    parser = argparse.ArgumentParser()
    add_parser_arguments(parser)
    args = parser.parse_args()
    datagen = args.datagen if args.datagen else False
    train_model = args.train if args.train else False

    text_classifier = TextClassifier(train_model, datagen)
    text_classifier.classify_directory_urls()
    text_classifier.classify_faculty_urls()
