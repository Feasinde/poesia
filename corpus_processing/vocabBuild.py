import os,json
from nltk import word_tokenize as tokenise

## os.getcwd() returns the current working directory
## os.path.dirname() takes a path and returns the directory above it
corpus_filename = os.path.dirname(os.getcwd())+'/corpus.json'

## load the corpus
corpus = json.load(open(corpus_filename))
index = {}

## number of training examples in corpus
m = len(corpus)

for i in range(m):
	tokens = tokenise(corpus[i]['title']) + tokenise(corpus[i]['text'])
	for token in tokens:
		token_lower = token.lower()
		if token_lower not in index:
			index[token_lower] = [i]
		else:
			index[token_lower].append(i)


with open('index.json','w') as op:
	op.write(json.dumps(index))