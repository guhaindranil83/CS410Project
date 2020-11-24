import shutil
from scraper import *

BIO_URLS_SPLIT_POINT = 500
ALEXA_BIO_URLS_SAMPLE_SIZE = 20

class DataHandler:

    def build_faculty_urls(self, file_name, corpus_type):
        """
        Build the faculty directory urls from the MP 2.1 sign up sheet csv
        """
        print "\nPreparing faculty directory urls ..."
        tmp_file = os.path.join(os.path.dirname(file_name), 'tmp_' + os.path.basename(file_name))
        if not os.path.exists(tmp_file):
            open(tmp_file, 'w').close()

        with open(tmp_file, 'w') as fo:
            with open(file_name, 'r') as fi:
                lines = fi.readlines()
                for line in lines:
                    parts = line.split(',')
                    last_part = parts[-1]
                    if last_part and last_part != '"' and last_part != '\r' and last_part != '\n' and last_part != '\r\n':
                        if not (last_part.startswith('"') and not last_part.endswith('"')):
                            if re.findall("\.", last_part):
                                data_string = ""
                                if corpus_type == DATA_TYPE_TRAINING:
                                    data_string += TAG_DIRECTORY + '\t'
                                data_string += parts[-1]
                                fo.write(data_string)

        cleaned_data_file = os.path.splitext(file_name)[0] + '.cor'
        shutil.move(tmp_file, cleaned_data_file)

    def build_alexa_train_urls(self):
        """
        Build the alexa train urls set from the country specific alexa urls
        """
        print "\nPreparing alexa train urls ..."
        alexa_train_files = ['./data/original/Alexa_Top_50.cor', './data/original/Alexa_Top_50_CA.cor',
                             './data/original/Alexa_Top_50_India.cor', './data/original/Alexa_Top_50_Kenya.cor',
                             './data/original/Alexa_Top_50_NZ.cor', './data/original/Alexa_Top_50_SA.cor',
                             './data/original/Alexa_Top_50_Singapore.cor', './data/original/Alexa_Top_50_UK.cor',
                             './data/original/Alexa_Top_50_US.cor', './data/original/Alexa_Top_50_Zim.cor'
                             ]

        unique_urls = set([])

        for train_file in alexa_train_files:
            with open(train_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    unique_urls.add(line)

        # Populate the Alexa training urls file
        if not os.path.exists(ALEXA_TRAIN_URLS_FILE):
            open(ALEXA_TRAIN_URLS_FILE, 'w').close()

        with open(ALEXA_TRAIN_URLS_FILE, 'w') as f:
            for url in unique_urls:
                data_string = TAG_ALEXA + '\t' + url
                f.write(data_string)

    def build_alexa_test_urls(self):
        """
        Build the alexa test urls set from the country specific alexa urls
        """
        print "\nPreparing alexa test urls ..."
        alexa_test_files = ['./data/original/Alexa_Top_50_Australia.cor', './data/original/Alexa_Top_50_Jamaica.cor',
                            './data/original/Alexa_Top_50_Nigeria.cor', './data/original/Alexa_Top_50_TrinTob.cor',
                            './data/original/Alexa_Top_50_Uganda.cor'
                            ]
        with open(ALEXA_TRAIN_URLS_FILE, 'r') as f:
            alexa_train_urls = f.readlines()

        # Unique Alexa test urls excluding any urls in the Alexa training urls
        unique_urls = set([])

        for test_file in alexa_test_files:
            with open(test_file, 'r') as f:
                test_urls = f.readlines()
                for test_url in test_urls:
                    if test_url not in alexa_train_urls:
                        unique_urls.add(test_url)

        # Populate the Alexa test urls file
        if not os.path.exists(ALEXA_TEST_URLS_FILE):
            open(ALEXA_TEST_URLS_FILE, 'w').close()

        with open(ALEXA_TEST_URLS_FILE, 'w') as f:
            for url in unique_urls:
                f.write(url)

    def mix_train_urls(self):
        """
        Mix the urls from alexa url train set and faculty directory url train set
        """
        print "\nMixing train urls ..."
        unique_urls = set([])
        with open(ALEXA_TRAIN_URLS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                unique_urls.add(line)

        with open(FACULTY_DIR_TRAIN_URLS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                unique_urls.add(line)

        if not os.path.exists(TRAIN_URLS_FILE):
            open(TRAIN_URLS_FILE, 'w').close()

        with open(TRAIN_URLS_FILE, 'w') as f:
            for url in unique_urls:
                f.write(url)

    def mix_test_urls(self):
        """
        Mix the urls from alexa url test set and faculty directory url test set
        """
        print "\nMixing test urls ..."
        unique_urls = set([])
        with open(ALEXA_TEST_URLS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                unique_urls.add(line)

        with open(FACULTY_DIR_TEST_URLS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                unique_urls.add(line)

        if not os.path.exists(TEST_URLS_FILE):
            open(TEST_URLS_FILE, 'w').close()

        with open(TEST_URLS_FILE, 'w') as f:
            for url in unique_urls:
                f.write(url)

    def prepare_data_source(self):
        """
        Prepare the train and test urls for the directory url classification task
        """
        print "\nPreparing faculty directory urls from both sources ..."
        self.build_faculty_urls("./data/original/Faculty_Directory_Train.csv", DATA_TYPE_TRAINING)
        self.build_alexa_train_urls()
        self.mix_train_urls()

        self.build_faculty_urls("./data/original/Faculty_Directory_Test.csv", DATA_TYPE_TESTING)
        self.build_alexa_test_urls()
        self.mix_test_urls()

    def prepare_corpus(self, corpus_type):
        """
        Prepare the corpus for the directory url classification task
        """
        print "\nPreparing corpus of directory urls for {} ...".format(corpus_type)
        scraper = Scraper(corpus_type)
        scraper.create_output_file()
        scraper.extract_url_contents()

    def prepare_train_bio_data_source(self):
        """
        Prepare the urls file for training the bio classifier
        """
        print "\nPreparing train bio urls ..."
        if not os.path.exists(TRAIN_BIO_URLS_FILE):
            open(TRAIN_BIO_URLS_FILE, 'w').close()

        this_file_dir = os.path.dirname(os.path.abspath(__file__))
        existing_bio_urls_file = os.path.join(os.path.dirname(this_file_dir), 'data/urls')
        # "CourseProject/ExpertSearch/data/urls"
        with open(TRAIN_BIO_URLS_FILE, 'w') as fo:
            # take the first 2000 urls as training data
            with open(existing_bio_urls_file, 'r') as fi:
                lines = fi.readlines()
                for i in range(BIO_URLS_SPLIT_POINT):
                    faculty_bio_url = lines[i].strip()
                    fo.write(TAG_FACULTY + '\t' + faculty_bio_url)
                    fo.write('\n')

        with open(TRAIN_BIO_URLS_FILE, 'a') as fo:
            alexa_test_files = ['./data/original/Alexa_Top_50_Australia.cor', './data/original/Alexa_Top_50_Uganda.cor',
                                './data/original/Alexa_Top_50_Jamaica.cor', './data/original/Alexa_Top_50_Nigeria.cor',
                                './data/original/Alexa_Top_50_TrinTob.cor'
                                ]
            test_urls = set([])
            for test_file in alexa_test_files:
                with open(test_file, 'r') as fi:
                    test_file_urls = fi.readlines()
                    test_urls.update(test_file_urls)

            for url in test_urls:
                url = url.strip()
                if not self.is_non_ascii(url):
                    fo.write(TAG_ALEXA_OTHER + '\t' + url)
                    fo.write('\n')

        # with open(TRAIN_BIO_URLS_FILE, 'a') as fo:
        #     # with open(ALEXA_TRAIN_URLS_FILE, 'r') as fi:
        #     with open('./data/original/Alexa_Top_50.cor', 'r') as fi:
        #         lines = fi.readlines()
        #         for i in range(ALEXA_BIO_URLS_SAMPLE_SIZE):
        #             alexa_train_url = lines[i].strip()
        #             scraper = Scraper(DATA_TYPE_BIO_TRAINING)
        #             alexa_sub_urls = scraper.get_links_from_url(alexa_train_url)
        #             # for i in range(len(alexa_sub_urls)):
        #             for j, alexa_sub_url in enumerate(alexa_sub_urls):
        #                 if j < ALEXA_BIO_URLS_SAMPLE_SIZE and not self.is_non_ascii(alexa_sub_url):
        #                     # fo.write(TAG_ALEXA_OTHER + '\t' + alexa_sub_urls[i].strip())
        #                     fo.write(TAG_ALEXA_OTHER + '\t' + alexa_sub_url.strip())
        #                     fo.write('\n')

    def prepare_train_bio_corpus(self):
        """
        Prepare the bio corpus for training the bio classifier
        """
        print "\nPreparing train bio corpus ..."
        scraper = Scraper(DATA_TYPE_BIO_TRAINING)
        scraper.create_output_file()

        # The first 2000 urls are from the existing bio urls,
        # so copy their corresponding bio file contents to our output file
        this_file_dir = os.path.dirname(os.path.abspath(__file__))
        with open(TRAIN_BIO_DATASET_FILE, 'w') as fo:
            for i in range(BIO_URLS_SPLIT_POINT):
                # "CourseProject/ExpertSearch/data/compiled_bios/6524.txt"
                bio_file_name = str(i) + '.txt'
                existing_bio_file = os.path.join(os.path.dirname(this_file_dir), 'data/compiled_bios', bio_file_name)
                with open(existing_bio_file, 'r') as fi:
                    bio_text = fi.readlines()[0].strip()
                    fo.write(TAG_FACULTY + '\t' + bio_text)
                    fo.write('\n')

        # For the remaining urls, extract the content from TRAIN_BIO_URLS_FILE and write to the output file
        scraper.extract_url_contents(start_idx=BIO_URLS_SPLIT_POINT)

    def prepare_test_bio_data_source(self):
        """
        Prepare the urls file (TEST_BIO_URLS_FILE) for testing the bio classifier
        """
        print "\nPreparing test bio urls ..."
        if not os.path.exists(TEST_BIO_URLS_FILE):
            open(TEST_BIO_URLS_FILE, 'w').close()

        with open(TEST_BIO_URLS_FILE, 'w') as fo:
            with open(TEST_URLS_FILE, 'r') as fi:
                lines = fi.readlines()
                # for i in range(20):
                for i, line in enumerate(lines):
                    if i == 50:
                        break
                    test_url = line.strip()
                    scraper = Scraper(DATA_TYPE_BIO_TESTING)
                    test_sub_urls = scraper.get_links_from_url(test_url)
                    for j, test_sub_url in enumerate(test_sub_urls):
                        # range(len(test_sub_urls)):
                        # if j < 10 and not self.is_non_ascii(test_sub_url):
                        if not self.is_non_ascii(test_sub_url):
                            # fo.write(TAG_TEST_FACULTY + '\t' + test_sub_urls[i].strip())
                            # fo.write(test_sub_urls[i].strip())
                            fo.write(test_sub_url.strip())
                            fo.write('\n')

    def prepare_test_bio_corpus(self):
        """
        Prepare the bio corpus for testing the bio classifier
        """
        print "\nPreparing test bio corpus ..."
        scraper = Scraper(DATA_TYPE_BIO_TESTING)
        scraper.create_output_file()
        scraper.extract_url_contents()

    def is_non_ascii(self, string):
        for c in string:
            if ord(c) >= 128:
                return True
        return False
