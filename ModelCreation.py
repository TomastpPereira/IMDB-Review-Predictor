from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re   # For preprocessing, removing punctuation
import math # For log10 function

review_list = pd.read_csv(r'C:\Users\tomas\PycharmProjects\472Assignment2\data.csv')['Reviews Link'].to_list()
positive_reviews = []
negative_reviews = []
positive_titles = []
negative_titles = []

# For loop to go through each link the data.csv and retrieves the review, review title and score
# All content is turned to lowercase and punctuation is removed
for episodeReviews in review_list:
    url = episodeReviews
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    review_containers = html_soup.find_all('div', class_='review-container')
    for review in review_containers:
        review_content = review.find('div', class_='text show-more__control').text
        review_content = re.sub(r"\W", ' ', review_content)
        review_content = re.sub(r"\s+", ' ', review_content)
        review_title = review.a.text
        review_title = re.sub(r'\W', ' ', review_title)
        review_title = re.sub(r"\s+", ' ', review_title)
        try:
            review_value = review.find('span', class_='rating-other-user-rating').span.text
        except:
            continue

        if int(review_value) >= 8:
            positive_reviews.append(review_content.lower())
            positive_titles.append(review_title.lower())
        else:
            negative_reviews.append(review_content.lower())
            negative_titles.append(review_title.lower())


negative_proportion = len(negative_reviews)/(len(negative_reviews)+len(positive_reviews))
positive_proportion = len(positive_reviews)/(len(negative_reviews)+len(positive_reviews))

negative_cutoff = negative_proportion*len(negative_reviews)
positive_cutoff = positive_proportion*len(positive_reviews)

test_negative_reviews = negative_reviews[:int(negative_cutoff)]
test_negative_titles = negative_titles[:int(negative_cutoff)]
training_positive_reviews = positive_reviews[:int(positive_cutoff)]
training_positive_titles = positive_titles[:int(positive_cutoff)]
training_negative_reviews = negative_reviews[int(negative_cutoff):]
test_positive_reviews = positive_reviews[int(positive_cutoff):]
training_negative_titles = negative_titles[int(negative_cutoff):]
test_positive_titles = positive_titles[int(positive_cutoff):]


#---- Building of Probabilistic Model Starts -----

# Reading the stopword file and saving the words to a list
stopwords = []
with open("remove.txt") as f:
    stopwords = [line.rstrip() for line in f]

# Creating the Dictionnary storing the words and their frequency
pos_wordFrequency = {}
pos_wordCount = 0
for sentence in positive_reviews:
    tokens = sentence.split(" ")
    for token in tokens:
        if token in stopwords:
            continue
        if token == '':
            continue
        if token not in pos_wordFrequency.keys():
            pos_wordFrequency[token] = 1
            pos_wordCount += 1
        else:
            pos_wordFrequency[token] += 1

neg_wordFrequency = {}
neg_wordCount = 0
for sentence in negative_reviews:
    tokens = sentence.split(" ")
    for token in tokens:
        if token in stopwords:
            continue
        if token == '':
            continue
        if token not in neg_wordFrequency.keys():
            neg_wordFrequency[token] = 1
            neg_wordCount += 1
        else:
            neg_wordFrequency[token] += 1

dictAllWords = dict(pos_wordFrequency, **neg_wordFrequency)

# To be modified or removed depending on which model is being created
#dictAllWords = {k:dictAllWords[k] for k in dictAllWords.keys() if len(k)<9}

# To be modified to change which file is being written to
writeFile = open("model.txt", "w")

total_wordCount = len(dictAllWords.keys())
probGivenPos = 0
probGivenNeg = 0
wordDoneCount = 1
for word in dictAllWords.keys():
    if len(word) <= 2:
        continue
    if pos_wordFrequency.get(word) == None:
        probGivenPos = math.log10(1/(pos_wordCount + total_wordCount))
    else:
        probGivenPos = math.log10((pos_wordFrequency.get(word)+1)/(pos_wordCount + total_wordCount))
    if neg_wordFrequency.get(word) == None:
        probGivenNeg = math.log10(1/(neg_wordCount + total_wordCount))
    else:
        probGivenNeg = math.log10((neg_wordFrequency.get(word)+1)/(neg_wordCount + total_wordCount))
    numberText = ("No. {} {}\n").format(wordDoneCount, word)
    dataText = ("{} {} {} {}\n").format(pos_wordFrequency.get(word), probGivenPos, neg_wordFrequency.get(word), probGivenNeg)
    writeFile.write(numberText)
    writeFile.write(dataText)
    wordDoneCount += 1
writeFile.close()

print("Model Creation has ended. Program Terminating")