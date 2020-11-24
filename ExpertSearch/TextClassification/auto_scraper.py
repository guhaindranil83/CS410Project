from data_handler import *
from scraper import *
from text_classifier import *

data_handler = DataHandler()

def add_parser_arguments(parser):
    parser.add_argument('-d', '--datagen', action='store_true', help='Add new training and test data')
    parser.add_argument('-t', '--train', action='store_true', help='Train model before classify task')


def prep_data_for_dir_classification():
    open(CLASSIFIED_DIRECTORY_URLS_FILE, 'w').close()

    data_handler.prepare_data_source()
    data_handler.prepare_corpus(DATA_TYPE_TRAINING)
    data_handler.prepare_corpus(DATA_TYPE_TESTING)


def prep_data_for_bio_classification():
    open(CLASSIFIED_FACULTY_URLS_FILE, 'w').close()

    # data_handler.prepare_train_bio_data_source()
    # data_handler.prepare_train_bio_corpus()
    data_handler.prepare_test_bio_data_source()
    data_handler.prepare_test_bio_corpus()


def main():
    # 0. If data_gen is requested or data is not yet generated, then do data prepartion first in #1 and #2 below
    # 1. Given the faculty urls and alexa urls, prepare the mix of urls for training and testing
    # 2. Prepare the corpus files for training and testing
    # 3. Use the TextClassifier to classify the faculty directory pages from the test set
    # 4. Use the Scraper to scrape each of the classified directory url to be used as test set
    # 5. Use the existing faculty url contents and some alexa page contents as training set
    # 6. Use the TextClassifier to classify the faculty homepages from the test set
    # 7. Use the classified faculty homepages and save them to individual bio file for each faculty
    arg_parser = argparse.ArgumentParser()
    add_parser_arguments(arg_parser)
    args = arg_parser.parse_args()
    gen_data = args.datagen if args.datagen else False
    train_model = args.train if args.train else False

    # # add new training and test data if gen_data is true or if the dataset doesn't exist yet
    # if gen_data or not (os.path.exists(TRAIN_DATASET_FILE) or os.path.exists(TEST_DATASET_FILE)):
    #     prep_data_for_dir_classification()
    #
    # # classify the directory urls from the test dataset
    # text_classifier = TextClassifier(TASK_DIRECTORY_CLASSIFICATION, train_model, gen_data)
    # text_classifier.classify_directory_urls()

    # add new training and test bio data if gen_data is true or if the dataset doesn't exist yet
    if gen_data or not (os.path.exists(TRAIN_BIO_DATASET_FILE) or os.path.exists(TEST_BIO_DATASET_FILE)):
        prep_data_for_bio_classification()

    # classify the faculty urls from the test dataset
    text_classifier = TextClassifier(TASK_FACULTY_CLASSIFICATION, train_model, gen_data)
    text_classifier.classify_faculty_urls()

    # now scrape the bios from each classified faculty url from the file CLASSIFIED_FACULTY_URLS_FILE
    # and save each individual bio file under the compiled_bios folder
    scraper = Scraper(DATA_TYPE_BIO_TESTING)
    scraper.scrape_faculty_pages_for_bio()


if __name__ == '__main__':
    main()