from nltk import word_tokenize
import nltk


nltk.download('stopwords')

stop_words = nltk.corpus.stopwords.words('english')


def stopwords_d(data):
    tokens = word_tokenize(data)
    tokens_deleted = [x for x in tokens if x not in stop_words]
    prompt_item = " ".join(tokens_deleted)
    return prompt_item, len(tokens_deleted)
