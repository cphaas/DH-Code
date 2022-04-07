
import deepl
import csv
import english_words

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
    "PT": "Portuguese",
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
    "Portuguese": "PT",
    "Romanian": "RO",
    "Russian": "RU",
    "Slovak": "SK",
    "Slovenian": "SL",
    "Swedish": "SV",
    "Chinese": "ZH"
}

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

# Translates word "word" into language "translang" and then back into language "sourcelang. Returns True if the words match, returns False if not

def tryWord(word, sourcelang, translang):
    print("Attempting to translate " + word + " from " + langDict[sourcelang] + " into " + langDict[translang])
    transword = translate(word, translang)
    if sourcelang == "EN":
        if word.lower()==transword.lower() and not isEnglish(word):
            print("Could not find a translation of " + word + " in " + langDict[translang])
            print("Translation unsuccessful")
            return False
    if word.lower() == transword.lower():
        print("Could not find a translation of " + word + " in " + langDict[translang])
        print("Translation unsuccessful")
        return False
    print(word + " in " + langDict[translang] + " is " + transword)
    print("Attempting to translate " + transword + " back to " + langDict[sourcelang] + " " + word)
    retransword = translate(transword, sourcelang)
    if word.lower() == retransword.lower():
        print(transword + " translated back to " + word)
        print("Translation successful")
        return True
    else:
        print(transword + " translated back to " + retransword + ", not " + word)
        print("Translation unsuccessful")
        return False

# Returns True if translation has occured (i.e. the text has changed). Returns False otherwise

def checkForTranslation(sourceWord, transWord, sourceLang, transLang):
    if sourceWord.lower() == transWord.lower():
        return False
    return True


# Creates a list of dictionaries from a .csv file. The key values for the dictionary are determined by the first
# row of the .csv file.

def wordListFromCsv(fileName):
    wordList = []
    with open(fileName) as file:
        reader = csv.DictReader(file)
        for row in reader:
            wordList.append(row)
    return wordList

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    # print(translate(translate("go", "DE").text, "EN-US"))
    # tryWord("go", "EN-US", "DE")
    # tryWord("Kummerspeck", "DE", "EN-US")
    # tryWord("treiben", "DE", "EN-US")
    # print(type(translate("go", "DE")))
    testLangList = ["DE", "ZH", "SV", "CS"]
    testWordList = wordListFromCsv('jakarta list.csv')
    for word in testWordList:
        for lang in testLangList:
            tryWord(word['wordOrig'], word['langCode'], lang)
            print("")
