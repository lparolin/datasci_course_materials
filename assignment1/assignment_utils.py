# Set of utils function for assignment 1
import re

def is_json_line_to_analyze(json_line):
    """Identifies if the json line given as input should be analyzed or not.
    A json line is analyzed if it is defined as either english or unknwon language.
    Also, the field text must be available.
    :param json_line Json line to analyze
    :return boolean variable
    """

    if 'text' not in json_line:
        return False

    # check if we are dealing with english characters
    if 'lang' in json_line:
        language_set = json_line.get('lang')
    else:
        language_set = 'en'  # guess

    return language_set == 'en'  # only parse english languages


def words_in_string(my_string):
    """Returns a list of words contained in the string.
    :param my_string String of words
    :return list of words.
    """

    pattern_to_skip = re.compile("(https?(! )*)|(#\w+)|(@\w+)")
    word_pattern = "([a-zA-Z]+-[a-zA-Z]+)|([a-zA-Z]+'[a-zA-Z]*)|([a-zA-Z]+)"

    my_words = []

    lower_case_string = my_string.lower()

    for token in lower_case_string.split():
        # remove everything that is not a letter or a number at either the beginning or end of word
        identified_pattern_to_skip = re.search(pattern_to_skip, token)
        if identified_pattern_to_skip:
            #print "  skipping token: " + token
            continue

        # look for words in this token
        #print "  considering token: " + token
        broken_parts = re.search(word_pattern, token)
        if broken_parts is None:
            #print "  No words identified, skipping token"
            continue

        #print "  identified tokens:",
        #print broken_parts.group(0)

        word = broken_parts.group(0)
        my_words.append(word)
    return my_words


def line_score(line, score_dict):
    """Computes the score of a line based on the values given in score_dict
    :param line: string
    :param score_dict: dictionary of (word, value) pair
    :return: Value of the string
    """

    word_list = words_in_string(line)
    return list_of_words_score(word_list, score_dict)


def list_of_words_score(list_of_words, score_dict):
    """Computes the score of a list of words based on the values given in score_dict
    :param list_of_words:
    :param score_dict:
    :return: Value of the list
    """

    score = 0
    for word in list_of_words:
        if word in score_dict:
            score += score_dict.get(word)

    return score
