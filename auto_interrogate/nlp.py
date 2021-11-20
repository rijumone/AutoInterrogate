import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

blacklisted_words = [
    'see',
    'interesting',
]

def get_tokens(txt):
    txt = re.sub(r"[^a-zA-Z0-9]", " ", txt.lower())
    tokens = word_tokenize(txt)
    modded_stopwords = [s  for s in stopwords.words("english") if not s.startswith('w')]
    tokens = [ w for w in tokens if w not in (modded_stopwords + blacklisted_words)]
    return tokens

if __name__ == '__main__':
    for sent in [
        'What were you doing the day of The Incident?',
        'What is your full name?',
        'I see. Where were you during The Incident?',
        'Who are you closest to?',
        'What is your occupation?',
        'What were you doing the day of The Incident?',
        'Interesting. What is your full name?',
        'Interesting. Where were you born?',
        ]:
        tokens = get_tokens(sent)
        print(tokens)
    # for w in stopwords.words("english"):
    #     print(w)