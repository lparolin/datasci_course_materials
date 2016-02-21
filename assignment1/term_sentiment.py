import sys
import json
import re
import nltk

from assignment_utils import is_json_line_to_analyze, words_in_string, list_of_words_score, line_score


def json_line_score(json_line, score_dict):
    """Computes the score of a json object based on the values given by my_dict.
    Only the 'text' field is considered for the json object
    :param json_line: json object for which the value is to be computed
    :param my_dic: (word, value) pairs
    :return value of the line
    """

    if is_json_line_to_analyze(json_line):
        score = line_score(json_line.get('text'), score_dict)
    else:
        score = 0

    return score


def compute_word_line_association(tweet_file, score_dict):
    word_lines = {}
    line_idx = 0

    for iline in tweet_file:
        my_data = json.loads(iline)

        if not is_json_line_to_analyze(my_data):
            continue

        print "Considering message: ",
        print my_data.get('text')
        list_of_words = words_in_string(my_data.get('text'))

        print "Idenfied words: ",
        print list_of_words

        print " Value of the string: {}".format(list_of_words_score(list_of_words, score_dict))

        for word in list_of_words:
            if word in word_lines:
                word_lines.get(word).append(line_idx)
                print "  New use of the word '" + word + "' found."
                print "  New list:",
                print word_lines.get(word)
            else:
                print "  New word found: " + word
                word_lines[word] = [line_idx]
        line_idx += 1
    return word_lines


def init_dic(file_obj):
    """Initialize the dictionary
    :param file_obj: File object containing the (word, value) pairs
    :rtype: dict
    """

    scores = {}
    for line in file_obj:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores


def main():
    afinnfile = open(sys.argv[1], "r")
    tweet_file = open(sys.argv[2], "r")

    my_dic = init_dic(afinnfile)

    counter = 0
    for iline in tweet_file:
        counter += 1
        my_data = json.loads(iline)
        print json_line_score(my_data, my_dic)
    # compute tweet value
    #initial_values = compute_score(tweet_file, my_dic)


    # Put the pointer back to the beginning of the file
    #tweet_file.seek(0)
    # find which word is in which line
    #word_line_association = compute_word_line_association(tweet_file, my_dic)

    #hw(tweet_file, my_dic)


if __name__ == '__main__':
    main()





def line_score(line, my_dic):
    """Computes the score of a string based on the values given by my_dict.
    :param line: string for which the value is to be computed
    :param my_dic: (word, value) pairs
    :return value of the line
    """

    lower_line = line.lower()
    word_sequence = lower_line.split()
    score = 0
    for my_word in word_sequence:
        if my_word in my_dic:
            score += my_dic.get(my_word)
    return score





