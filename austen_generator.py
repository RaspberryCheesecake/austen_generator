import random
import urllib2

def get_online_text(url):
    try:
        website = urllib2.urlopen(url)
        text = website.read()
        return text
    except urllib2.HTTPError as e:
        print("Cannot retrieve text from url {} due to error: {}".format(
            url, e))


def get_trigrams(sentence):
    words = sentence.split(' ')
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
            pass  # When we reach the end and run out of i+1 words

    return trigrams


def generate_text(trigram_dict, first_words, string_so_far=''):

    if len(string_so_far) > 800:
        return string_so_far  # Don't go on forever with big texts

    try:
        next_word_list = trigram_dict[first_words]
        next_word = random.choice(next_word_list)
    except KeyError:
        return string_so_far  # can't go any further

    result = "{} {}".format(first_words, next_word)
    next_key = get_next_key(result)

    # Remove those annoying musical notes
    # It's a DOS/unix line endings thing
    string_so_far += " " + next_word.replace('\r\n', ' ')

    return generate_text(trigram_dict, next_key, string_so_far)


def get_next_key(text):
    words = text.split(' ')
    return " ".join(words[-2:])


if __name__ == "__main__":
    pride_and_prejudice = get_online_text("http://www.gutenberg.org/files/1342/1342-0.txt")
    prejudice_grams = get_trigrams(pride_and_prejudice)

    first_words = random.choice(prejudice_grams.keys())
    prejudice_rand = generate_text(prejudice_grams, first_words)
    
    print(prejudice_rand)
