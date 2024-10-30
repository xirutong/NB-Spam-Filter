import unittest
from corpus import tokenize, read_file, read_dataset

class SpamFilter:
    def __init__(self):
        self.unknown = None

    def train(self, emails):
        """
        train the filter with training data
        :param emails: list of training instances
        :return: none
        """
        global p_wi_spam, p_wi_ham

        total_spam = 0  # count |{email | email ∈ "spam" }|
        total_ham = 0  # count |{email | email ∈ "ham" }|
        p_wi_spam = {}  # map each word to the P(w_i|“spam”)
        p_wi_ham = {}  # map each word to the P(w_i|“ham”)
        vocab = set()  # store the types of all training emails
        email_dict = {}

        for email in emails:
            if email[1] == "spam":
                total_spam += 1
            else:
                total_ham += 1
            for word in email[0]:
                vocab.add(word)
                if word not in email_dict:
                    email_dict[word] = []
                email_dict[word].append(email)

        for word in vocab:
            num_spam = sum(1 for email in email_dict[word] if email[1] == "spam")
            num_ham = sum(1 for email in email_dict[word] if email[1] == "ham")
            p_wi_spam[word] = num_spam / total_spam
            p_wi_ham[word] = num_ham / total_ham

        return

    def classify(self, email):
        """
        classify an email into spam or ham
        :param email: a token list of an email
        :return: a tuple consisting of spam score and the classification result
        """

        multi_spam = 1  # initiating the multiplication of P(w_i|“spam”) with 1
        multi_ham = 1  # initiating the multiplication of P(w_i|“ham”) with 1

        for word in email:
            if word in p_wi_spam.keys() and word in p_wi_ham.keys():
                if p_wi_spam[word] == 0:
                    multi_spam *= 0.1
                    if p_wi_ham[word] == 0:
                        multi_ham *= 0.1
                    else:
                        multi_ham *= p_wi_ham[word]
                else:
                    multi_spam *= p_wi_spam[word]
                    if p_wi_ham[word] == 0:
                        multi_ham *= 0.1
                    else:
                        multi_ham *= p_wi_ham[word]
            if word not in p_wi_spam.keys() and word in p_wi_ham.keys():
                multi_spam *= 0.5
                if p_wi_ham[word] == 0:
                    multi_ham *= 0.01
                else:
                    multi_ham *= p_wi_ham[word]
            if word not in p_wi_ham.keys() and word in p_wi_spam.keys():
                multi_ham *= 0.5
                if p_wi_spam[word] == 0:
                    multi_spam *= 0.01
                else:
                    multi_spam *= p_wi_spam[word]
            if word not in p_wi_ham.keys() and word not in p_wi_spam.keys():
                multi_ham *= 0.5
                multi_spam *= 0.5

        # calculate the spam score according to the formula
        try:
            spam_score = multi_spam / (multi_spam + multi_ham)
        except:
            spam_score = 0.5

        # classify the email into spam or ham
        if spam_score >= 0.47:
            return tuple([spam_score, 'spam'])
        else:
            return tuple([spam_score, 'ham'])


# -----------------------------------------------------UNIT TEST--------------------------------------------------------
class TestSpamFilter(unittest.TestCase):
    def setUp(self):
        self.spam_filter = SpamFilter()

    def test_train(self):
        # Test that training on an empty list does not raise an error
        self.spam_filter.train([])

        # Test that training on a non-empty list does not raise an error
        emails = [
            (["hello", "ham", "email"], "ham"),
            (["buy", "viagra", "now"], "spam")
        ]
        self.spam_filter.train(emails)

    def test_classify(self):
        # Test that classifying an email with all words in the dictionary returns "spam"
        emails = [
            (["hello", "ham", "email"], "ham"),
            (["buy", "viagra", "now"], "spam")
        ]
        self.spam_filter.train(emails)
        result = self.spam_filter.classify(["buy", "viagra", "now"])
        self.assertEqual(result[1], "spam")
