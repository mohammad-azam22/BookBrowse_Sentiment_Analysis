import nltk
import string

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.util import mark_negation

from nltk.corpus import stopwords
nltk.download('stopwords')

from nltk.corpus import opinion_lexicon
nltk.download('opinion_lexicon')

def getTextSentiment():

	writeFile = open("sentiments.txt", "w")

	readFile = open("reviews.txt", "r")
	text = readFile.readline()

	while text:
		
		tokens = word_tokenize(text)

		stop_words = set(stopwords.words('english')) 
		negations = {"not", "no", "never", "none", "nobody", "nothing", "neither", "nowhere", "hardly", "scarcely", "barely"} 
		filtered_stop_words = stop_words - negations
		
		filtered_tokens = []
		for token in tokens:
			if token not in filtered_stop_words and token not in string.punctuation:
				filtered_tokens.append(token)


		# Lemmatize the tokens

		lemmatizer = WordNetLemmatizer()
		lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
		
		negated_tokens = mark_negation(lemmatized_tokens)

		positive_words = opinion_lexicon.positive()
		negative_words = opinion_lexicon.negative()

		# Initialize counters 
		positive_count = 0
		negative_count = 0 

		# Check each token 
		for token in negated_tokens: 
			if token in positive_words: 
				positive_count += 1 
			elif token in negative_words: 
				negative_count += 1 
			elif token.endswith('_NEG'): 
				base_token = token[:-4] 
				if base_token in positive_words: 
					negative_count += 1 
				elif base_token in negative_words: 
					positive_count += 1 
					
		# Calculate Polarity Score 
		polarity_score = (positive_count - negative_count) / ((positive_count + negative_count) + 0.0000001) 

		# Determine Sentiment 
		if polarity_score < -0.3: 
			sentiment = 'Negative' 
		elif polarity_score > 0.3: 
			sentiment = 'Positive' 
		else: 
			sentiment = 'Neutral ' 

		writeFile.write(f"{sentiment} : {text}")
		# print(f"Polarity Score: {polarity_score} Sentiment: {sentiment}")

		text = readFile.readline()
	
	writeFile.close()
	readFile.close()
	
if __name__ == "__main__":
	getTextSentiment()