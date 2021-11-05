import re   # For preprocessing, removing punctuation
import math
import matplotlib.pyplot as plt

print('Welcome to the Model Testing')
userIn = input("Enter 0 to test with base Model, 1 to test the different length models or 2 to test a custom title: ")
print("")

# If testing the review titles
if userIn == "0":
    modelFile = open("model.txt")
    modelLines = modelFile.readlines()
    # Forming a dictionary of Words and the data associated with them
    count = 0
    wordDict = {}
    # Storing the model info into a dictionnary for easy use
    for i in modelLines:
        if (count > 1 and count % 2 == 0):
            wordDict[keyWord] = wordData
        count += 1
        if (count % 2) == 1:
            splitLine = i.split(" ")
            keyWord = splitLine[-1]
            keyWord = keyWord.strip()
        else:
            wordData = i.split(" ")
            wordData = [word.strip() for word in wordData]

    # Files holding test titles are used to run faster and not require scrapping on every run
    positiveTitlesFile = open("PositiveTestTitles.txt")
    positiveTitles = positiveTitlesFile.readlines()
    positiveTitles = [title.strip() for title in positiveTitles]
    negativeTitlesFile = open("NegativeTestTitles.txt")
    negativeTitles = negativeTitlesFile.readlines()
    negativeTitles = [title.strip() for title in negativeTitles]

    probPos = math.log10(len(positiveTitles)/(len(positiveTitles) + len(negativeTitles)))
    probNeg = math.log10(len(negativeTitles)/(len(positiveTitles) + len(negativeTitles)))

    # Count A, B, D are used to later calculate accuracy measures
    countA = 0
    countB = 0
    countD = 0

    # Positive Reviews are tested by the model
    print("Testing Against Positive Reviews")
    reviewCount = 0
    # Going through each title in the list of positive titles and testing them
    for review_title in positiveTitles:
        reviewCount += 1
        print("No.", reviewCount, review_title)
        review_title = re.sub(r'\W', ' ', review_title)
        review_title = re.sub(r"\s+", ' ', review_title)
        title_to_list = review_title.split()
        # Breaks down the current title and calculates P(ri|positive) and P(ri|negative)
        currentRIPos = probPos
        currentRINeg = probNeg
        for word in title_to_list:
            # If a word is not in the vocabulary, it gets ignored
            if wordDict.get(word) == None:
                continue
            else:
                currentWordData = wordDict[word]
                currentRIPos += float(currentWordData[1])
                currentRINeg += float(currentWordData[3])
        if (currentRIPos > currentRINeg):
            print(currentRIPos, currentRINeg, "Positive", "Positive", "Correct")
            countA += 1
        else:
            print(currentRIPos, currentRINeg, "Negative", "Positive", "Incorrect")
            countB += 1

    # Negative Titles are tested by the model
    print("\n\nTesting Against Negative Reviews")
    reviewCount = 0
    # Going through each title in the list of positive titles and testing them
    for review_title in negativeTitles:
        reviewCount += 1
        print("No.", reviewCount, review_title)
        review_title = re.sub(r'\W', ' ', review_title)
        review_title = re.sub(r"\s+", ' ', review_title)
        title_to_list = review_title.split()
        # Breaks down the current title and calculates P(ri|positive) and P(ri|negative)
        currentRIPos = probPos
        currentRINeg = probNeg
        for word in title_to_list:
            # If a word is not in the vocabulary, it gets ignored
            if wordDict.get(word) == None:
                continue
            else:
                currentWordData = wordDict[word]
                currentRIPos += float(currentWordData[1])
                currentRINeg += float(currentWordData[3])
        algoAnswer = ""
        if (currentRIPos < currentRINeg):
            print(currentRIPos, currentRINeg, "Negative", "Negative", "Correct")
        else:
            print(currentRIPos, currentRINeg, "Positive", "Negative", "Incorrect")
            countD += 1

    # Accuracy Measures are calculated and output
    modelPrecision = countA/(countA+countB)
    modelRecall = countA/(countA+countD)
    fmeasure = ((1 + 1)*(modelRecall*modelPrecision))/(modelPrecision+modelRecall)
    print("\nPrecision: ", modelPrecision, "Recall: ",modelRecall)
    print("Model F-Measure with B=1: ", fmeasure)

    # Files are closed before program end
    modelFile.close()
    positiveTitlesFile.close()
    negativeTitlesFile.close()
    print("\nEnding the Program")



# ----------------------------------------------------------------------------------------------------
# The case where the length models are being tested
elif userIn == "1":
    print("Starting the comparison of different length models")
    lengthModels = ["model.txt", "length-2model.txt", "length-4model.txt", "length-9model.txt"]
    # Opening the files holding the test titles
    positiveTitlesFile = open("PositiveTestTitles.txt")
    positiveTitles = positiveTitlesFile.readlines()
    positiveTitles = [title.strip() for title in positiveTitles]
    negativeTitlesFile = open("NegativeTestTitles.txt")
    negativeTitles = negativeTitlesFile.readlines()
    negativeTitles = [title.strip() for title in negativeTitles]

    probPos = math.log10(len(positiveTitles) / (len(positiveTitles) + len(negativeTitles)))
    probNeg = math.log10(len(negativeTitles) / (len(positiveTitles) + len(negativeTitles)))
    accuracies = []
    wordsInModel = []

    # A loop is used so that all 4 models will be used in one run
    for model in lengthModels:
        modelFile = open(model)
        modelLines = modelFile.readlines()
        count = 0
        wordDict = {}
        # The current model is prepared to be used
        for i in modelLines:
            if (count > 1 and count % 2 == 0):
                wordDict[keyWord] = wordData
            count += 1
            if (count % 2) == 1:
                splitLine = i.split(" ")
                keyWord = splitLine[-1]
                keyWord = keyWord.strip()
            else:
                wordData = i.split(" ")
                wordData = [word.strip() for word in wordData]
        wordsInModel.append(int(count/2))
        print("\n\n---------------------------------------------------------------------------------------------------")
        print(model, "---> Words in model:", int(count/2))

        countA = 0
        countB = 0
        countD = 0
        print("\nTesting Against Positive Reviews")
        reviewCount = 0
        # Going through each title in the list of positive titles and testing them
        for review_title in positiveTitles:
            reviewCount += 1
            print("No.", reviewCount, review_title)
            review_title = re.sub(r'\W', ' ', review_title)
            review_title = re.sub(r"\s+", ' ', review_title)
            title_to_list = review_title.split()
            # Breaks down the current title and calculates P(ri|positive) and P(ri|negative)
            currentRIPos = probPos
            currentRINeg = probNeg
            for word in title_to_list:
                # If a word is not in the vocabulary, it gets ignored
                if wordDict.get(word) == None:
                    continue
                else:
                    currentWordData = wordDict[word]
                    currentRIPos += float(currentWordData[1])
                    currentRINeg += float(currentWordData[3])
            if (currentRIPos > currentRINeg):
                print(currentRIPos, currentRINeg, "Positive", "Positive", "Correct")
                countA += 1
            else:
                print(currentRIPos, currentRINeg, "Negative", "Positive", "Incorrect")
                countB += 1

        print("\nTesting Against Negative Reviews")
        reviewCount = 0
        # Going through each title in the list of positive titles and testing them
        for review_title in negativeTitles:
            reviewCount += 1
            print("No.", reviewCount, review_title)
            review_title = re.sub(r'\W', ' ', review_title)
            review_title = re.sub(r"\s+", ' ', review_title)
            title_to_list = review_title.split()
            # Breaks down the current title and calculates P(ri|positive) and P(ri|negative)
            currentRIPos = probPos
            currentRINeg = probNeg
            for word in title_to_list:
                # If a word is not in the vocabulary, it gets ignored
                if wordDict.get(word) == None:
                    continue
                else:
                    currentWordData = wordDict[word]
                    currentRIPos += float(currentWordData[1])
                    currentRINeg += float(currentWordData[3])
            algoAnswer = ""
            # If the model prediction is that the title is negative
            if (currentRIPos < currentRINeg):
                print(currentRIPos, currentRINeg, "Negative", "Negative", "Correct")
                e=1
            # If the model preiction is that the title is positive
            else:
                countD += 1
                f=1
                print(currentRIPos, currentRINeg, "Positive", "Negative", "Incorrect")

        # Calculation of accuracy measures and then outputs them
        modelPrecision = countA / (countA + countB)
        modelRecall = countA / (countA + countD)
        fmeasure = ((1 + 1) * (modelRecall * modelPrecision)) / (modelPrecision + modelRecall)
        print("\nPrecision: ", modelPrecision, "Recall: ", modelRecall)
        print("Model F-Measure with B=1: ", fmeasure)
        accuracies.append(fmeasure)
        modelFile.close()

    # Plotting the Graph
    t = wordsInModel
    s = [x*100 for x in accuracies]
    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.set(xlabel='Number of Words in Vocab', ylabel='Accuracy', title='Accuracy vs Length Model')
    ax.grid()
    plt.show()

    # Closing files before program end
    positiveTitlesFile.close()
    negativeTitlesFile.close()
    print("The program has ended")

#------------------------------------------------------------------------------------------------------
# If testing a specific title
elif userIn == "2":
    # Opening model file to use it
    modelFile = open("model.txt")
    modelLines = modelFile.readlines()

    titleToTest = input("Enter the title to be tested: ")

    count = 0
    wordDict = {}
    # Putting the model information into dictionnary for easy use
    for i in modelLines:
        if (count > 1 and count % 2 == 0):
            wordDict[keyWord] = wordData
        count += 1
        if (count % 2) == 1:
            splitLine = i.split(" ")
            keyWord = splitLine[-1]
            keyWord = keyWord.strip()
        else:
            wordData = i.split(" ")
            wordData = [word.strip() for word in wordData]

    adjustedTitle = titleToTest.strip().lower()
    titleToList = adjustedTitle.split()

    currentRIPos = 0.0
    currentRINeg = 0.0
    # The input string is broken down and tested word by word
    for word in titleToList:
        # If a word is not in the vocabulary, it gets ignored
        if wordDict.get(word) == None:
            continue
        else:
            currentWordData = wordDict[word]
            currentRIPos += float(currentWordData[1])
            currentRINeg += float(currentWordData[3])

    if (currentRIPos > currentRINeg):
        print(currentRIPos, currentRINeg, "Prediction: Positive")
    else:
        print(currentRIPos, currentRINeg, "Prediction: Negative")

    # File is closed before program end
    modelFile.close()
    print("Program has ended")

# -----------------------------------------------------------------------------------------------------
# If user puts in an incorrect value
else:
    print("Incorrect Value Entered: Ending the Testing")

