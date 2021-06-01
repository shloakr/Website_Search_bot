from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True)
print('Chat bot: What is your name?')
user_input_name = input()
print('Chat bot: Which website do you want to make a bot on?')
user_input_website = input()
print('Chat bot: What is the topic of the website you want to make a bot on?')
user_input_topic = input()

# article = Article("https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521")
article = Article(user_input_website)
article.download()
article.parse()
article.nlp()
corpus = article.text

text = corpus
sentance_list = nltk.sent_tokenize(text)

def greeting_respone(text):
    text = text.lower()

    bot_greeting = ['hi', 'hey', 'hello', 'hey there!', 'hola']
    user_greeting = ['hi', 'hey', 'hello', 'hola', 'greetings', 'whatsup']
    for word in text.split():
        if word in user_greeting:
            return random.choice(bot_greeting)

def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] =  temp

    return list_index


def bot_respone(user_input):
    user_input = user_input.lower()
    sentance_list.append(user_input)
    bot_respone = " "
    cm = CountVectorizer().fit_transform(sentance_list)
    similarity_score = cosine_similarity(cm[-1], cm)
    similarity_score_list = similarity_score.flatten()
    index = index_sort(similarity_score_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_score_list[i]> 0.0:
            bot_respone = bot_respone+ ' ' + sentance_list[index[i]]
            response_flag = 1
            j +=1
        if j > 2:
            break

    if response_flag == 0:
        bot_respone = bot_respone + ' ' + 'I dont understand'

    sentance_list.remove(user_input)

    return bot_respone

print("Doc Bot: I am a bot that answers your queries about {}".format(user_input_topic))

exit_list = ['bye', 'quit', 'exit', 'break']



while True:
    user_input = input("{}:".format(user_input_name))
    if user_input.lower() in exit_list:
        print('Doc Bot: Thanks')
        break 
    else:
        if greeting_respone(user_input) != None:
            print('Doc Bot: ' + greeting_respone(user_input))
        else:
            print('Doc Bot: '+bot_respone(user_input))
