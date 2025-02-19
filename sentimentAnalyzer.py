# imports from ntlk that must be present to interface with ntlk
#pip install ntlk
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.probability import FreqDist
from nltk.corpus import stopwords

#defines global variables which will be used 
sentPositivity = []
sentNegativity = []
sentNeutrality = []
sentOverall = []
#startList = []
#wordTokens= []
#stemmer = PorterStemmer()
#lammanizer = WordNetLemmatizer()
#stopwordSet = set(stopwords.words('english'))
#filteredWords = []
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt_tab')
fdist = FreqDist()

#function performing sentiment analysis
def sentimentAnalysis(analysisSent):
    sidObj = SentimentIntensityAnalyzer()

    #generates an overall polarity score which we can divide into a composite score of pos, neg, and neu
    #appends each score to their respective bins
    sentimentDict = sidObj.polarity_scores(analysisSent)
    sentPositivity.append(sentimentDict['pos'])
    sentNegativity.append(sentimentDict['neg'])
    sentNeutrality.append(sentimentDict['neu'])
    
    #based on the outcome, makes a definitive determination of sentiment
    #numbers can be tweaked to fine tune (.05 acts as default)
    if sentimentDict['compound'] >= 0.05 :
        sentOverall.append("Positive")
 
    elif sentimentDict['compound'] <= - 0.05 :
        sentOverall.append("Negative")
 
    else :
        sentOverall.append("Neutral")

def sentimentAnalyzerMain(inputFile):
    #sentPositivity = []
    #sentNegativity = []
    #sentNeutrality = []
    startList = []
    wordTokens= []
    stemmer = PorterStemmer()
    lammanizer = WordNetLemmatizer()
    stopwordSet = set(stopwords.words('english'))
    #sentOverall = []
    filteredWords = []
    fdist = FreqDist()
    #opens text file and filters everything into a list where each element ([]) is a line from the input file
    with open(inputFile, encoding="utf8") as f:
        #reads input as string with no newline characters
        readInStr = f.read().replace('\n', ' ')
        f.close()

    #splits string into list on custom ENDOFCOMMENT deliminator 
    startList = readInStr.split("ENDOFCOMMENT ")

    #prints list for debugging purposes
    #for i in range(len(startList)):
        #print(startList[i])

    #tokenizes StartList creating a 2d list where each element is a line and each sub element is a word
    for i in range(len(startList)):
        wordTokens.append(word_tokenize(startList[i].lower()))

    #Filters out words based on the default list of stop words to perform frequency distribution 
    for i in range(len(wordTokens)):
        for j in range(len(wordTokens[i])):
            if wordTokens[i][j] not in stopwordSet:
                filteredWords.append(wordTokens[i][j])

    #removes common punctuation from frequency analysis
    listToRemove = ['.', '?', ',', '!', ':', ';']
    filteredWords = [i for i in filteredWords if i not in listToRemove]

    for word in filteredWords:
            fdist[word.lower()] += 1

    #most_common could be changed to fine tune.  Larger output probably better the larger the dataset gets
    fdist1 = fdist.most_common(20)


    #stems and lemmatizes each lines in wordTokens
    #Both of these steps are crucial in reducing workload of sentiment analysis model 
    for i in range(len(wordTokens)):
        for j in range(len(wordTokens[i])):
                wordTokens[i][j] = stemmer.stem(wordTokens[i][j])

    for i in range(len(wordTokens)):
        for j in range(len(wordTokens[i])):
            wordTokens[i][j] = lammanizer.lemmatize(wordTokens[i][j])

    #joins all subelements of each element together in a string to feed through the sentiment analyzer
    for i in range(len(wordTokens)):
        tempSent = " ".join(wordTokens[i])
        sentimentAnalysis(tempSent)

    writeFile = open("analysisResults.txt", "w")

    writeFile.write("Frequency Distribution: \n")
    writeFile.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in fdist1))

    writeFile.write("\n\nPositive Sentiment: ")
    for i in range(len(sentPositivity)):
        writeFile.write(str(sentPositivity[i]))
        writeFile.write(" ")

    writeFile.write("\n\nNeutral Sentiment: ")
    for i in range(len(sentNeutrality)):    
        writeFile.write(str(sentNeutrality[i]))
        writeFile.write(" ")

    writeFile.write("\n\nNegative Sentiment: ")
    for i in range(len(sentNegativity)):
        writeFile.write(str(sentNegativity[i]))
        writeFile.write(" ")

    writeFile.write("\n\nOverall Sentiment: ")
    for i in range(len(sentOverall)):
        writeFile.write(sentOverall[i])
        writeFile.write(" ")

    writeFile.close()
    print("done")