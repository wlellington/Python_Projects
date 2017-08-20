# Tutorial provided at http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
# All credits due to original creator

import random
import math
import csv
import string


class Classifier:
	vocabulary = []
	prob_data = {}
	num_classes = 0
	num_samples = 0
	class_counts = {}
	working_data = None

	def __init__(self):
		pass

	def process_data(self, filename):
		dataset = self.loadText(filename)
		tokenization = self.tokenize(dataset)
		self.working_dataset = tokenization[0]
		self.vocabulary = tokenization[1]
		print "Loaded %s entries" % (len(self.working_dataset))
		class_info = self.seperateClass(self.working_dataset)
		class_data = class_info[0]
		self.class_counts = class_info[1]
		words = self.classAllWords(class_data)
		self.prob_data = self.calculateProbs(words, self.vocabulary)
		print "Classifier created with %s words in vocabulary" % (len(self.vocabulary))
	
	# Create classifications for list of strings
	def classify_list(self, strings):
		results = []
		for phrase in strings:
			results.append(self.classify_string(phrase))

		return results

	# Get total sentiment for list of queries
	def get_sentiments(self, queries):
		class_types = []
		scores = {}
		curr_class = None
		results = self.classify_list(queries)
		# determine winning class for each result
		for sentiment in results:
			curr_high = 0
			for classification in self.class_counts.keys():
				if sentiment[classification] > curr_high:
					curr_high = sentiment[classification]
					curr_class = classification
			class_types.append(curr_class)
		# calculate sentiment percentages
		for classification in self.class_counts.keys():
			count = 0
			for entry in class_types:
				if entry  == classification:
					count += 1

			scores[classification] = float(count) / float (len(queries))

		return scores


	# Get classification prediction for a string
	def classify_string(self, text):
		return self.predict(self.cleanInput(text))
	
	# Loads in text for input
	def loadText(self, filename):
		inputfile = open(filename, "rb")
		reader = csv.reader(inputfile)
		dataset = []	
		for row in reader:
			dataset.append([row[1], row[0]])
		return dataset

	#Cleans input of non data set input and returns in usable list form
	def cleanInput(self, phrase):
		clean_phrase = phrase.lower()
		clean_phrase =  "".join(c for c in clean_phrase if c.isalnum() or c == ' ')

		# Cut entries by space
		tokens = clean_phrase.split(' ')
		# Clean illigal length items
		tokens = [x for x in tokens if len(x) >= 1]

		return tokens

	# Divides by spaces, cleans punctuation and converts to lower case
	# returns collection of clean_data entries and vocabulary for set
	def tokenize(self, dataset):
		clean_data = []
		vocabulary = []
		for entry in dataset:
			# Standardize text format
			clean_words = entry[1].lower()
			clean_words =  "".join(c for c in clean_words if c.isalnum() or c == ' ')

			# Cut entries by space
			tokens = clean_words.split(' ')
			# Clean illigal length items
			tokens = [x for x in tokens if len(x) >= 1]

			#Add cleaned tokens into vocab
			for token in tokens:
				if token not in vocabulary:
					vocabulary.append(token)

			clean_entry = []
			clean_entry.append(entry[0])
			clean_entry.append(tokens)
			clean_data.append(clean_entry)
	
		return [clean_data, vocabulary]
		
	def seperateClass(self, dataset):
		classified_data = {}
		class_counts = {}
		for entry in dataset:
			# seperate items by key in map
			if entry[0] not in classified_data.keys():
				classified_data[entry[0]] = []
				class_counts[entry[0]] = 1

			classified_data[entry[0]].append(entry[1])
			class_counts[entry[0]] += 1

		return [classified_data, class_counts]

	# Create list of all words in review, store count of number of times
	# Each word appears as well as total counts
	def allWords(self, classDataset):
		words = {}
		total = 0
		# Iterate over entries for a given class
		for entry in classDataset:
			for word in entry:
				if word not in words:
					words[word] = 1
					total += 1
				else:
					words[word] += 1
					total += 1

		# Store total count as _count in dict
		words["_count"] = total
		return words

	# Create list of all words for all types of classification
	def classAllWords(self, class_data):
		frequencyWords = {}
		vocab_size = 0
		for k in class_data:
			frequencyWords[k] = self.allWords(class_data[k])
			vocab_size += len(frequencyWords[k].keys()) - 1

		return frequencyWords

	# For all classes of data, calculate probability of each term given its class
	def calculateProbs(self, frequency_data, vocabulary):
		prob_data = {}
		vocab_size = len(vocabulary)
		for key in frequency_data:
			n = frequency_data[key]["_count"]
			probability = 0
			prob_data[key] = {}
			for word in frequency_data[key]:
				if word != "_count":
					probability = float(frequency_data[key][word] + 1) / float(n  + vocab_size)
					prob_data[key][word] = probability
			prob_data[key]["_count"] = n
		
		return prob_data

	# Given a list of summaries, make a guess as to which item is most likely
	def predict(self, inputVector):
		predictions = {}
		class_prob = 0
		class_total = 0
		for classification in self.class_counts:
			class_total += self.class_counts[classification]
		for classification in self.prob_data:
			class_prob = float(self.class_counts[classification])/ float(class_total)
			for term in inputVector:
				# if term in in vocab
				if term in self.prob_data[classification].keys():
					class_prob *= self.prob_data[classification][term]
				# Else assign minimum value
				elif term in self.vocabulary:
					class_prob *= 1 / float(len(self.vocabulary) + self.prob_data[classification]["_count"])
				# Pass for now if not in vocab
				else:
					pass
			
			predictions[classification] = class_prob

		return predictions
		
	# Determine accuracy of classification system
	def getAccuracy(testSet, predictions):
		correct = 0
		for x in range(len(testSet)):
			if testSet[x][-1] == predictions[x]:
				correct += 1
		return (correct/float(len(testSet))) * 100.0

def main():
	filename = 'pima-indians-diabetes.data.csv'
	splitRatio = 0.67
	dataset = loadCsv(filename)
	trainingSet, testSet = splitDataset(dataset, splitRatio)
	print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainingSet), len(testSet))
	# prepare model
	summaries = summarizeByClass(trainingSet)
	# test model
	predictions = getPredictions(summaries, testSet)
	print predictions
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: {0}%').format(accuracy)

def tests():
	myClassifier = Classifier()
	myClassifier.process_data("./data/training_01.txt")
	queries = ["Donald J. Trump is the worst president we've ever had", 
			"I love Python", 
			"Have you seen the new cat?",
			"Monsanto is a horrible beast",
			"Cookies are delicious",
			"That movie sucked",
			"I love a tasty, warm, good, cookie"]
	print queries
	print myClassifier.get_sentiments(queries)

# Execution script
if __name__ == "__main__":
	tests()
#	main()




