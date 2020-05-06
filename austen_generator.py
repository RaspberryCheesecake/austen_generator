import cPickle
import os
import random
import urllib2
import re


def get_online_text(url):
    try:
        website = urllib2.urlopen(url)
        text = website.read()
        return text
    except urllib2.HTTPError as e:
        print("Cannot retrieve text from url {} due to error: {}"
              .format(url, e))


def get_trigrams(sentence):
    sentence = sentence.replace('\r\n', '')  # remove stray line ends
    words = re.findall(r'[^\s]+', sentence)  # Don't match blank strings!

    trigrams = {}
    for i, w in enumerate(words):
        try:
            key = "{} {}".format(w, words[i+1])
            try:
                trigrams[key].append(words[i+2])
            except KeyError:
                # key doesn't exist yet
                trigrams[key] = [words[i+2]]
        except IndexError:
            pass  # Reached the end, ran out of i+1 words

    return trigrams


def generate_text(trigram_dict, first_words, string_so_far=''):

    if len(string_so_far) > 800 and string_so_far.endswith('.'):
        return string_so_far  # Don't go on forever with big texts, & end nicely on a full stop

    try:
        next_word_list = trigram_dict[first_words]
        next_word = random.choice(next_word_list)
    except KeyError:
        return string_so_far  # can't go any further

    result = "{} {}".format(first_words, next_word)
    next_key = get_next_key(result)

    string_so_far += " " + next_word

    return generate_text(trigram_dict, next_key, string_so_far)


def get_next_key(text):
    words = text.split(' ')
    return " ".join(words[-2:])


def fix_up_punctuation(my_text_string):
    words = re.findall(r'[^\s]+', my_text_string)
    words[0] = words[0].title()  # Capitalise first letter always
    return " ".join(words)


def trigramise_text_from_gutenberg(text_link="http://www.gutenberg.org/files/1342/1342-0.txt"):
    """
    Stores the trigram'd text in a pickled format to save downloading the novel each time.
    :param text_link: Defaults to using the link to Jane Austen's 'Pride and Prejudice'
    :return: A paragraph of plausible text using trigrams from the novel given
    """
    storage = 'trigram_storage.txt'
    if not os.path.exists(storage):
        print("Getting {} text online ...\n\n".format(text_link))
        novel = get_online_text(text_link)
        trigrams = get_trigrams(novel)

        with open(storage, 'wb') as my_file:
            cPickle.dump(trigrams, my_file)

    else:
        print("Using stored trigram data we prepared earlier\n\n")
        with open(storage) as my_file:
            trigrams = cPickle.load(my_file)

    seed = random.choice(trigrams.keys())
    generated_paragraph = generate_text(trigrams, seed)

    return generated_paragraph


if __name__ == "__main__":
    autogenerated_paragraph = trigramise_text_from_gutenberg()
    to_display = fix_up_punctuation(autogenerated_paragraph)
    print(to_display)

    with open('output.txt', 'w') as fout:
        fout.write(to_display)
