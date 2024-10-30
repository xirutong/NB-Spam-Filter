
from nb import *
import os
from os.path import join

# train a spam filter
to_spam_filter = SpamFilter()
print(r'Please enter the path to the training data. Example: E:\Codes\Programming for CL\project\data\train.')
to_spam_filter.train(read_dataset(input()))

# classify an email/a batch of emails
while True:
    print(
        'What do you want to classify? (Enter A, B or E)\n(A) an email\n(B) a batch of emails\n(E) terminate the whole program')
    answer = input()
    # SINGLE mode
    if answer == 'A':
        print('Please enter the path to a testing email:')
        try:
            path = input()
            spam_score = to_spam_filter.classify(read_file(path))[0]
            cat = to_spam_filter.classify(read_file(path))[1]
            print('Do you want to save the result to a file?\n(A) yes\n(B) no')
            save = input()
            if save == 'A':
                filename = 'spamfilter.txt'
                with open(filename, 'w') as file_object:
                    for row in os.path.basename(path), spam_score, cat:
                        file_object.write(str(row) + ' ')
                print('Result saved. File name: spamfilter.txt.')
            elif save == 'B':
                print(os.path.basename(path), spam_score, cat)
            else:
                print("Only 'A' or 'B' is allowed.")
        except:
            print('Please enter a valid path.')

    # BATCH mode
    elif answer == 'B':
        print('Please enter the path to the testing directory. Make sure that only .txt files exist in this directory.')
        try:
            path = input()
            files = os.listdir(path)
            rs = []
            for file in files:
                file_path = join(path, file)
                spam_score = to_spam_filter.classify(read_file(file_path))[0]
                cat = to_spam_filter.classify(read_file(file_path))[1]
                rs.append([os.path.basename(file_path), spam_score, cat])
            print('Do you want to save the result to a file?\n(A) yes\n(B) no, only print it')
            save = input()
            if save == 'A':
                filename = 'spamfilter.txt'
                with open(filename, 'w') as file_object:
                    for row in rs:
                        file_object.write("%s\n" % (str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2])))
                print('Result saved. File name: spamfilter.txt.')
            elif save == 'B':
                for i in rs:
                    print(i[0], i[1], i[2])
            else:
                print("Only 'A' or 'B' is allowed.")
        except:
            print('Please enter a valid path.')

    # terminate the program
    elif answer == 'E':
        break

    # wrong entry
    else:
        print("Only 'A', 'B' or 'E' is allowed.")
