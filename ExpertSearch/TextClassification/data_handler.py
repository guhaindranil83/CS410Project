import shutil
from scraper import *


class DataHandler:

    def build_faculty_urls(self, file_name, corpus_type):
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
                                    data_string += TAG_FACULTY + '\t'
                                data_string += parts[-1]
                                fo.write(data_string)

        cleaned_data_file = os.path.splitext(file_name)[0] + '.cor'
        shutil.move(tmp_file, cleaned_data_file)

    def build_alexa_train_urls(self):
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
        self.build_faculty_urls("./data/original/Faculty_Directory_Train.csv", DATA_TYPE_TRAINING)
        self.build_alexa_train_urls()
        self.mix_train_urls()

        self.build_faculty_urls("./data/original/Faculty_Directory_Test.csv", DATA_TYPE_TESTING)
        self.build_alexa_test_urls()
        self.mix_test_urls()

    def prepare_corpus(self, corpus_type):
        scraper = Scraper(corpus_type)
        scraper.extract_url_contents()
