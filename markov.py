import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains, char_limit = 140):
    """Takes dictionary of markov chains; returns random text.

    Random text will begin with a capital letter.
    
    char_limit will stop word addition loosely (but possibly exceeding)
    the character count.  Text is then truncated, possibly mid word, to enforce that limit.

    """

    text = ""

    first_ngram = choice(chains.keys()) 
    #check to see if choice first index starts with capital letter and is camelcased
    while not ((first_ngram[1][0].isupper())): #and (first_ngram[1][1].islower())):
        first_ngram = choice(chains.keys())

    ngram = first_ngram
    text += ngram[1]
    char_count = 0
    while ((ngram in chains) and char_count < char_limit):
        end_words = ngram[1:] 
        new_word = choice(chains[ngram])
        new_key = end_words+(new_word,) 
        text += " {}".format(new_word)  
        ngram = new_key
        char_count+=len(new_word)
    
    text = text[:char_limit]

    return text


def clean_end(text):
    """Removes text after last occurance of end or near-end punctionation. Defaults to comma or last space if none found. """
 

    punct = (
        ".", 
        ";", 
        "?", 
        "!",
        ":",
        )

    punct_index = [text.rfind(p) for p in punct]
    print punct_index
    cleaned_end = max(punct_index)+1
    if cleaned_end < 1:
        # check for last comma
        comma_index = text.rfind(",")
        cleaned_end = comma_index+1
        #check for last space
        if comma_index < 1:
            space_index = text.rfind(" ")
            cleaned_end = space_index


    text_cleaned = text[:cleaned_end]

    return text_cleaned


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                      access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                      access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    #print api.VerifyCredentials()

    status = api.PostUpdate(chains)
    print status.text

# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

tweet_text = make_text(chains)

tweet_text_cleaned = clean_end(tweet_text)
#print tweet_text
#print type(tweet_text)
#print (tweet_text[:139])
# Your task is to write a new function tweet, that will take chains as input
tweet(tweet_text_cleaned)



