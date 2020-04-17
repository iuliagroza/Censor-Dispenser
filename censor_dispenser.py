'''
Created by Iulia Groza, April 2020
'''

# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()


#censoring the phrase by maintaining its length and spaces
def censored(phrase):
    censor = ""
    for char in phrase:
        if char == " ":
            censor += " "
        else:
            censor += "*"
    return censor

#rudimental function to censor this phrase into this specific email
#replace is used, so I have not taken into consideration a general approach where capital letters could be used
def censor_phrase(text, phrase):
    return text.replace(phrase, censored(phrase))

print(censor_phrase(email_one, "learning algorithms"))


proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithms", "her", "herself", "Helena"]
#in order to censor any variation of the phrases in terms of capitalization, we should compare the lower version of them (otherwise, "Helena" would have been a special case)
lower_proprietary_terms = []
for term in proprietary_terms:
    term = term.lower()
    lower_proprietary_terms.append(term)
proprietary_terms = lower_proprietary_terms

#check if index i is in range
def in_range(text, i, phrase):
    return ((i>0 and text[i-1].isalpha() == False) or i==0) and (i+len(phrase)==len(text) or text[i+len(phrase)].isalpha() == False)

#function to censor a list of phrases into a given text
def censor_list_of_phrases(text, phrases_list):
    for phrase in phrases_list:
        censor = censored(phrase)
        #manually verifying each character assures us we are solving special cases, such as capitalization, not censoring words that contain the given words, preserving the spaces, newlines and punctuation of the original text
        for i in range(len(text)-len(phrase)+1):
            phrase_to_verify = text[i:i+len(phrase)].lower()
            #by using .isalpha() we're making sure we are not censoring insides of words containing the given words to censor - we're basically verifying whole words
            if phrase_to_verify == phrase and in_range(text, i, phrase):
                text = text[:i]+censor+text[i+len(phrase):]
    return text

print(censor_list_of_phrases(email_two, proprietary_terms))


negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressed", "concerning", "horrible", "horribly", "questionable"]
#there is no need to lower this list

#function to censor a list of phrases and a list of negative words, starting from their second appearance
def extensive_censor(text, phrases_list, bad_words):
    text = censor_list_of_phrases(text, proprietary_terms)
    for word in bad_words:
        censor = censored(word)
        count = 0
        for i in range(len(text)-len(word)+1):
            word_to_verify = text[i:i+len(word)].lower()
            if word_to_verify == word and in_range(text, i, word):
                count += 1
                #censoring phrases starting from their second appearances
                if count >= 2:
                    text = text[:i]+censor+text[i+len(word):]
    return text

print(extensive_censor(email_three, proprietary_terms, negative_words))


def censor_word_before(text, i):
    finish = i - 1
    while finish > 0 and text[finish].isalpha() == False:
        finish -= 1
    start = finish
    while start > 0 and text[start].isalpha() == True:
        start -= 1
    start += 1
    censor_before = censored(text[start:finish+1])
    return text[:start] + censor_before + text[finish + 1:]

def censor_word_after(text, i, phrase):
    start = i + len(phrase)
    while start < len(text) and text[start].isalpha() == False:
        start += 1
    finish = start
    while finish < len(text) and text[finish].isalpha() == True:
        finish += 1
    censor_after = censored(text[start:finish])
    return text[:start] + censor_after + text[finish:]

#function to censor phrases from two given lists (not necessarily from their second appearance) and the words before and after them
def extensive_censor_two(text, phrases_list, bad_words):
    for phrase in phrases_list:
        censor = censored(phrase)
        for i in range(len(text)-len(phrase)+1):
            phrase_to_verify = text[i:i + len(phrase)].lower()
            if phrase_to_verify == phrase and in_range(text, i, phrase):
                text = text[:i] + censor + text[i + len(phrase):]
                text = censor_word_before(text, i)
                text = censor_word_after(text, i, phrase)
    for word in bad_words:
        censor = censored(word)
        for i in range(len(text)-len(word)+1):
            word_to_verify = text[i:i+len(word)].lower()
            if word_to_verify == word and in_range(text, i, word):
                text = text[:i]+censor+text[i+len(word):]
                text = censor_word_before(text, i)
                text = censor_word_after(text, i, word)
    return text

print(extensive_censor_two(email_four, proprietary_terms, negative_words))
