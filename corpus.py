# download and import nltk library
# pip install nltk
import nltk
from nltk.corpus import stopwords
import unittest
# nltk.download('punkt')
# nltk.download('stopwords')

# import os to deal with files and directories
import os
from os.path import join

stop_words = stopwords.words('english')
punkt = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '-', "'", '>', '#', '_', '/']


def tokenize(text):
    """
    convert a text into a list of tokens
    :param text: input text
    :return: token list of the input text
    """
    # sentence tokenizer
    sent_list = nltk.sent_tokenize(text)
    # word tokenizer
    token_list = []
    for sent in sent_list:
        token_list += nltk.word_tokenize(sent)
    # filter out stopwords, punctuations and digital numbers
    filtered_words = [w for w in token_list if w not in stop_words and w not in punkt and not w.isdigit()]
    return filtered_words


def read_file(path):
    """
    preprocess an original email and tokenize it
    :param path: path to an email
    :return: token list of email body
    """
    mail_body = ''
    f = open(path, 'r', encoding='utf-8', errors='ignore')
    for line in f.readlines():
        # discard the subject
        if not line.startswith('subject') and not line.startswith('Subject') and not line.startswith('cc'):
            mail_body += line
    f.close()
    # tokenize the mail body with the function "tokenize(text)"
    mail_body_tokens = tokenize(mail_body)
    return mail_body_tokens


def read_dataset(path):
    """
    convert an email dataset to a list of training instances consisting of token lists and labels
    :param path: path to a data set
    :return: a list of training instances
    """
    training_ls = []
    # a path pointing to the dataset
    dataset = os.listdir(path)
    for dirt in dataset:
        # directory path pointing to the ham and spam directories
        dir_path = join(path, dirt)
        dirt = os.listdir(dir_path)
        for each_file in dirt:
            # generate file path pointing to each email
            file_path = join(dir_path, each_file)
            # tokenize each email with the function "read_file(path)"
            mail_body_tokens = read_file(file_path)
            # label the token list with "ham" or "spam" and form training instances
            if file_path.endswith('.ham.txt'):
                training_instance = tuple([mail_body_tokens, "ham"])
            else:
                training_instance = tuple([mail_body_tokens, "spam"])
            # store all the training instances in a list
            training_ls.append(training_instance)
    return training_ls

# ---------------------------------------------UNIT TEST----------------------------------------------------------------
class TestCorpus(unittest.TestCase):

    def test_tokenize(self):
        # Test that the tokenize function correctly removes stopwords and punctuation
        input_text = "this is a sample sentence for testing the tokenizer."
        expected_output = ["sample", "sentence", "testing", "tokenizer"]
        self.assertEqual(tokenize(input_text), expected_output)

    def test_read_file(self):
        # Test that the read_file function correctly extracts the body of the email
        input_path = r"E:\Codes\Programming for CL\project\data\test\ham\0688.2000-03-22.farmer.ham.txt"
        expected_output = ['written', 'record', 'nom', 'following', 'nomination', 'eastrans', 'mmbtu', 'since', 'pg',
                           'e', 'cut', 'hpl', 'contract', 'effective', 'redeliveries', 'follows', 'pg', 'e', 'mobil',
                           'beaumont', 'int', 'cartwheel', 'carthage']

        self.assertEqual(read_file(input_path), expected_output)

    def test_read_dataset(self):
        # Test that the read_dataset function correctly reads all email files in a directory and labels them as spam or ham
        input_path = r"E:\Codes\Programming for CL\project\xiaopiliang"
        expected_output = [(['would', 'recommend', 'anywhere', 'b'], 'ham'),
                           (['paliourg', 'iit', 'demokritos', 'grpaliourgqfzzyfp', 'recoletos', 'esharry',
                             'ramosmagnanimohs', 'nracelet', 'fztgcrze', 'evo', 'mp', 'uqsgwz', 'wmrdvil', 'da',
                             'jqwjt', 'zzlm', 'rvxrqewlerswq', 'ordvvydqn', 'tuv', 'v', 'alghtrdtdsl'], 'spam')]

        self.assertEqual(read_dataset(input_path)[:2], expected_output)

if __name__ == '__main__':
    unittest.main()
