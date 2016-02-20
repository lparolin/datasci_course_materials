import sys
import json
import re

AFINN_FILE = "AFINN-111.txt"


def init_dic(filename):
    """Initialize the dictionary
    :param filename: String to the file name to parse
    :rtype: dict
    """

    afinnfile = open(filename)
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores


def hw(file_to_parse, my_dic):
    counter = 0

    for iline in file_to_parse:
        counter += 1
        my_data = json.loads(iline)
        # n_words = len(iline)
        # print "Line: {line_number} ".format(line_number=counter),
        my_score = compute_score(my_data, my_dic)
        print my_score


def compute_score(json_line, my_dic):
    """:param line: dict"""

    score = 0
    if 'text' in json_line:
        text_to_read = json_line.get('text')
        text_to_read = text_to_read.lower()
        my_sequence = text_to_read.split()
        for my_word in my_sequence:
            if my_word in my_dic:
                score += my_dic.get(my_word)
    else:
        score = 0
    return score

def lines(fp):
    """

    :rtype: Null
    """
    print str(len(fp.readlines()))


def main():
    # dictionary_file = open(sys.argv[1])
    my_dic = init_dic(sys.argv[1])
    #print my_dic

    tweet_file = open(sys.argv[2])
    hw(tweet_file, my_dic)
    #lines(sent_file)
    #lines(tweet_file)

if __name__ == '__main__':
    main()
