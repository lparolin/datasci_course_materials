import sys
import json
import re
import nltk

def compute_score(tweet_file, my_dic):
    """Computes score for each line of the tweet file based on the initial file.
    :param tweet_file File to parse
    :param my_dic Dictionary to use to compute the value of each line
    :return list of scores, one per line of the file"""

    score_data = []
    for iline in tweet_file:
        my_data = json.loads(iline)
        score_data.append(compute_json_line_score(my_data, my_dic))
    return score_data


def lines(fp):
    print str(len(fp.readlines()))


def compute_word_line_association(tweet_file):
    word_lines = {}
    line_idx = 0
    pattern = re.compile("(https?(! )*)|(#\w+)|(@\w+)")
    is_word = re.compile("\w+")
    #(\w+-\w+)|(\w+'\w+)|(\w+)
    word_pattern = "([a-zA-Z]+-[a-zA-Z]+)|([a-zA-Z]+'[a-zA-Z]*)|([a-zA-Z]+)"

    for iline in tweet_file:
        my_data = json.loads(iline)

        if 'text' in my_data:
            message = my_data.get('text').lower()
            print "\nMessage: ",
            print message

            # check if we are dealing with english characters
            if 'lang' in my_data:
                language_set = my_data.get('lang')
                print "identified language: ",
                print language_set
            else:
                print "unknown language"
                language_set = 'en' # guess
            if not language_set == 'en':
                print "Skipping message, not english"
                continue

            for token in message.split():
                # remove everything that is not a letter or a number at either the beginning or end of word
                identified_part = re.search(pattern, token)
                #if pattern.match(token):
                if identified_part is not None:
                    print "  skipping token: " + token
                    continue

                # get parts that is word only
                print "  considering token: " + token
                broken_parts = re.search(word_pattern, token)
                if broken_parts is None:
                    print "  No words identified, skipping token"
                    continue

                print "  identified tokens:",
                print broken_parts.group(0)
                #word = re.sub("^\W+", "", token)
                #word = re.sub("\W+$", "", token)


                word = broken_parts.group(0)
                print "  - modified token: " + word

                if is_word.match(word):
                    if word in word_lines:
                        word_lines.get(word).append(line_idx)
                        print "  New use of the word '" + word + "' found."
                        print "  New list:",
                        print word_lines.get(word)
                    else:
                        print "  New word found: " + word
                        word_lines[word] = [line_idx]
                else:
                    print "  Skipping token: " + word
        line_idx += 1
    return word_lines



def main():
    afinnfile = open(sys.argv[1], "r")
    tweet_file = open(sys.argv[2], "r")

    #my_dic = init_dic(afinnfile)
    # compute tweet value
    #initial_values = compute_score(tweet_file, my_dic)


    # Put the pointer back to the beginning of the file
    tweet_file.seek(0)
    # find which word is in which line
    word_line_association = compute_word_line_association(tweet_file)

    #hw(tweet_file, my_dic)


if __name__ == '__main__':
    main()


def compute_json_line_score(json_line, my_dic):
    """Computes the score of a json object based on the values given by my_dict.
    Only the 'text' field is considered for the json object
    :param json_line: json object for which the value is to be computed
    :param my_dic: (word, value) pairs
    :return value of the line
    """

    if 'text' in json_line:
        text_to_read = json_line.get('text')
        score = line_score(text_to_read, my_dic)
    else:
        score = 0
    return score


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


