
import deepl
import csv
import english_words
from nltk.corpus import stopwords

# Insert your own deepl API key here as a string
APIkey = "166c5f45-43da-3ef1-a710-de69fadc7a2d:fx"

# Creates the translator object that will be used for the succeeding functions
translator = deepl.Translator(APIkey)

# Dictionary with DeepL language codes as string keys and english language names as values



langDict = {
    "BG": "Bulgarian",
    "CS": "Czech",
    "DA": "Danish",
    "DE": "German",
    "EL": "Greek",
    "EN-UK": "British English",
    "EN-US": "American English",
    "ES": "Spanish",
    "ET": "Estonian",
    "FI": "Finnish",
    "FR": "French",
    "HU": "Hungarian",
    "IT": "Italian",
    "JA": "Japanese",
    "LT": "Lithuanian",
    "LV": "Latvian",
    "NL": "Dutch",
    "PL": "Polish",
    "PT-BR": "Portuguese",
    "RO": "Romanian",
    "RU": "Russian",
    "SK": "Slovak",
    "SL": "Slovenian",
    "SV": "Swedish",
    "ZH": "Chinese"
}

# Dictionary with English language names as string keys and DeepL Language keys as values

keyDict = {
    "Bulgarian": "BG",
    "Czech": "CS",
    "Danish": "DA",
    "German": "DE",
    "Greek": "EL",
    "British English": "EN-UK",
    "American English": "EN-US",
    "Spanish": "ES",
    "Estonian": "ET",
    "Finnish": "FI",
    "French": "FR",
    "Hungarian": "HU",
    "Italian": "IT",
    "Japanese": "JA",
    "Lithuanian": "LT",
    "Latvian": "LV",
    "Dutch": "NL",
    "Polish": "PL",
    "Portuguese": "PT-BR",
    "Romanian": "RO",
    "Russian": "RU",
    "Slovak": "SK",
    "Slovenian": "SL",
    "Swedish": "SV",
    "Chinese": "ZH"
}
allLangList = ["BG", "CS", "DA", "DE", "EL", "EN-US", "ES", "ET", "FI", "FR", "HU", "IT", "JA", "LT", "LV",
               "NL", "PL", "PT-BR", "RO", "RU", "SK", "SL", "SV", "ZH"]

outputCsvHeadings = ["sourceWord", "transWord", "endWord", "sourceLang", "transLang", "result"]

englishStopwords = set(stopwords.words('english'))

# Translates string "text" into language "targetlang" and returns the result as a string. For list of language keys see
# dictionary keydict above

def translate(text, targetlang):
    text = str(text)
    result = translator.translate_text(text=text, target_lang=targetlang)
    return result.__str__()

# Returns True if word "word" is in the set of English words and returns False otherwise

def isEnglish(word):
    if word.lower() not in english_words.english_words_lower_set:
        return False
    return True

# Translates word "word" into language "transLang" and then back into language "sourceLang. Returns a dictionary containing
# the sourceWord, the value the word was translated to, whatever the word was translated back
# to, the starting language, the translation language, and the result (True or False). These are keyed (respectively) to
# "sourceWord", "transWord", "endWord", "sourceLang", "transLang", "result"

def tryWord(sourceWord, sourceLang, transLang):
    if sourceLang == transLang:
        return None
    if sourceLang == "EN-US" and sourceWord in englishStopwords:
        return None
    resultDict = {}
    resultDict["sourceLang"] = sourceLang
    resultDict["transLang"] = transLang
    resultDict["sourceWord"] = sourceWord
    sourceWord = stripInfPrep(sourceWord, sourceLang)   # Strip any known infinitive prefixes from verbs
    transWord = translate(sourceWord, transLang)  # Translate the word into the transLang
    resultDict["transWord"] = transWord
    if not checkForTransOccurence(sourceWord, transWord, transLang):   # Checks to make sure a translation has actually occurred
        resultDict["result"] = False                                   # (only effectively catches loan words when translating into English)
        resultDict["endWord"] = " "
    endWord = translate(transWord, sourceLang) # Translate the word back into sourceLange
    resultDict["endWord"] = endWord
    resultDict["result"] = checkTrans(sourceWord, endWord)     # Check the accuracy of the translation
    return resultDict

# Returns True if translation has occured (i.e. the text has changed). Returns False otherwise.

def checkForTransOccurence(sourceWord, transWord, transLang):
    if transLang == "EN-US" or transLang == "EN-UK":
        if sourceWord.lower() == transWord.lower() and transWord.lower() not in english_words.english_words_lower_set:
            return False
    if sourceWord.lower() == transWord.lower():
        return False
    return True

# Checks whether a translated word matches the original word, or is a plural form of the original word

def checkTrans(sourceWord, endWord):
    sourceWord = sourceWord.lower()
    endWord = endWord.lower()
    if sourceWord != endWord:
        if not checkForPluralForm(sourceWord, endWord):
            return False
    return True

# Takes string "word" and source language code "sourceLang". Returns word, stripped of any infinitival prepositions it may
# have ("att" for Swedish, "at" for Danish, "to" for English).

def stripInfPrep(word, sourceLang):
    if sourceLang == "SV":
        if word[0:4] == "att ":
            return word[4:]
    if sourceLang == "DA":
        if word[0:3] == "at ":
            return word[3:]
    if sourceLang == "EN-US" or sourceLang == "EN-UK":
        if word[0:3] == "to ":
            return word[3:]
    return word

# Returns True if either word1 or word2 is a plural form of the other. Returns False otherwise.
# Note that this works only for English, and does not work reliably for irregular plurals

def checkForPluralForm(word1, word2):
    if word1 + "s" == word2 or word1 == word2 + "s":
        return True
    return False

# Creates a list of dictionaries from a .csv file. The key values for the dictionary are determined by the first
# row of the .csv file.

def wordListFromCsv(fileName):
    wordList = []
    with open(fileName, "r", newline="", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            wordList.append(row)
    return wordList

# Given a fileName and a list of strings, creates a csv file with headings set to the values listed in the list

def createCsvFile(fileName, headingList):
    with open(fileName, "w", newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(headingList)

# Given a .csv filename, the original word input, the value the word was translated to, whatever the word was translated back
# to, the starting language, the translation language, and the result (True or False), inputs the result into the listed
# csv file

def addTransResultToCsv(fileName, tryData):
    with open(fileName, "a", newline="", encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        inputData = [tryData["sourceWord"], tryData["transWord"], tryData["endWord"], tryData["sourceLang"],
                     tryData["transLang"], tryData["result"]]
        print("Source word: " + tryData["sourceWord"])
        print("Trans word: " + tryData["transWord"])
        print("End word: " + tryData["endWord"])
        writer.writerow(inputData)

#

def testWordList(inputFileName, outputFileName, langList):
    wordList = wordListFromCsv(inputFileName)
    createCsvFile(outputFileName, outputCsvHeadings)
    for word in wordList:
        for lang in langList:
            tryData = tryWord(word["wordOrig"], word["langCode"], lang)
            if tryData != None:
                addTransResultToCsv(outputFileName, tryData)

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    # testWordList("jakarta-swadesh list.csv", "", allLangList)
    testWordList("untranslatable-words.csv", "untranslatable-words_list_all_langs.csv", allLangList)