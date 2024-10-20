import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
from textblob import TextBlob
import contractions

nltk.download('punkt')
nltk.download('wordnet')


threatening_keywords = [ "suicide", "911","ambulance","kill", "die", "murder", "help", "danger", "threat", "hurt", "cut", "blood", "emergency","crisis", "poison", "overdose","attack", "stab", "knife", "gun", "shoot", "hostage","bomb", "death", "hanging", "drowning", "strangle", "torture", "panic", "despair", "risk","sexual harassment", "assault", "harass", "creepy", "pervert", "threatening", "exposure", "rape", "sexual assault", "penetration", "violence", "unconscious", "helpless", "victim", "predator", "abduction", "scream", "trap", "chase", "cornered", "drugged", "subdued", "immobilized","trauma", "panic", "desperation", "scared", "terrified",]

def find_threatening_token(sentence):
    sentence = sentence.lower()
    sentence = str(TextBlob(sentence).correct())
    tokens = word_tokenize(sentence)
    lemmatizer = WordNetLemmatizer()
    tokenized_keywords = [lemmatizer.lemmatize(word) for word in tokens]
    threaten_word = ""
    
    for token in tokenized_keywords:
        for word in threatening_keywords:
            if token == word:
                threaten_word = word
                return True, threaten_word
    return False,""

if __name__ == "__main__":
    print(find_threatening_token("get help right now"))
