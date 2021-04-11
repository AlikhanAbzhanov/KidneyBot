import nltk
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import string
import warnings
warnings.filterwarnings("ignore")

nltk.download("punkt", quiet=True)

article = Article("https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521")
article.download()
article.parse()
article.nlp()

corpus = article.text
text = corpus
sentence_list = nltk.sent_tokenize(text)


def greeting_response(text):
    text = text.lower()

    bot_greetings = ["hello", "hi", "hey", "howdy", "hola", "greetings", "welcome", "good day"]
    user_greetings = ["hello", "hi", "hey", "howdy", "hola"]

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var

    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)

    bot_resp = ""

    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]

    response_flag = 0
    j = 0

    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_resp = bot_resp + " " + sentence_list[index[i]]
            
            response_flag = 1
            j += 1

        if j > 2:
            break

    if response_flag == 0:
        bot_resp = bot_resp + " I apologize, I didn't understand your request."

    sentence_list.remove(user_input)

    return bot_resp


print("KidneyBot: I am KidneyBot. I will answer your requests about Chronic Kidney Disease. If you want to quit, type 'bye'.")

exit_list = ["bye", "goodbye", "exit", "see you", "see you later", "quit", "break"]

while True:
    user_input = input()

    if user_input.lower() in exit_list:
        print("KidneyBot: See you later!")

        break

    else:
        if greeting_response(user_input) != None:
            print("KidneyBot: " + greeting_response(user_input))

        else:
            print("KidneyBot: " + bot_response(user_input))
