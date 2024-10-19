import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
from textblob import TextBlob
import contractions

# nltk.download('punkt')
# nltk.download('wordnet')


threatening_keywords = [
    "suicide", "kill", "die", "murder", "help", "danger", "threat", "hurt", "cut", "blood", "emergency",
    "crisis", "poison", "overdose","attack", "stab", "knife", "gun", "shoot", "hostage",
    "bomb", "death", "hanging", "drowning", "strangle", "torture", "panic", "despair", "risk",
    "sexual harassment", "assault", "harass", "creepy", "pervert", "threatening", "exposure", "rape", "sexual assault",
    "penetration", "violence", "unconscious", "helpless", "victim", "predator", "abduction", "scream", "trap", "chase", "cornered", "drugged", "subdued", "immobilized",
    "trauma", "panic", "desperation", "scared", "terrified",]


def find_threatening_token(sentence):
    sentence = sentence.lower()
    sentence = str(TextBlob(sentence).correct())
    tokens = word_tokenize(sentence)
    lemmatizer = WordNetLemmatizer()
    threatening_keywords = [lemmatizer.lemmatize(word) for word in tokens]
    
    for token in tokens:
        for keyword in threatening_keywords:
            if token == keyword.lower() or keyword.lower() in token:
                return True
    return False

if __name__ == "__main__":
    # print(find_threatening_token("he is so creepy"))