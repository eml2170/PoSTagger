import sys
import string
from pipes import *

#Implementation of weight vector v
v_bigram = {}
v_tag = {}
enum_server = Procserver(["python", "tagger_history_generator.py",  "ENUM"])
gold_server = Procserver(["python", "tagger_history_generator.py",  "GOLD"])
decode_server = Procserver(["python", "tagger_decoder.py", "HISTORY"])

def decode(sentence):
	#Generate all possible histories
	histories = enum_server.communicate(sentence).split("\n")

	scores = ""
	#Score each history
	for i in range(0,len(histories)-1):
		history = histories[i]
		s = score(history,sentence)
		scores += histories[i] + " " + str(s) + "\n"
	#print scores
	return decode_server.communicate(scores)
	

#g(<t_i-1,x,i>,t_i)={BIGRAM,TAG}
#history given as i,t_{i-1},t_i
#x is the sentence
def computeG(history,x):
	#print "history=" + history
	#print "x=" + x

	h = history.split()
	i = int(h[0])-1

	sentence = x.split("\n")
	bigram = (h[1],h[2])
	#print "bigram=" + str(bigram)

	tag = (sentence[i],h[2])
	#print "tag=" + str(tag)
	return (bigram,tag)

def score(history,x):
	
	g_vector = computeG(history,x)
	bigram = g_vector[0]
	tag = g_vector[1]

	bigram_key = "BIGRAM:" + bigram[0] + ":" + bigram[1]
	tag_key = "TAG:" + tag[0] + ":" + tag[1]
	
	#v dot g
	
	score = 0.0
	if bigram_key in v_bigram:
		score += v_bigram[bigram_key]
	if tag_key in v_tag:
		score += v_tag[tag_key]
	return score

def populateWeights(model):
	f = open('tag.model','r')
	for line in f:
		datum = line.strip().split(" ")
		x = datum[0]
		y = float(datum[1])

		tokens = x.split(":")
		if tokens[0] == "TAG":
			v_tag[x] = y
		elif tokens[0] == "BIGRAM":
			v_bigram[x] = y
	f.close()

def formatOutput(sentence,tag):
	tags = tag.split("\n")
	sentence_split = sentence.split("\n")
	#print sentence_split
	#print tags

	if sentence_split[0] == '':
		return ''
	for i in range(0,len(sentence_split)-1):
		sentence_split[i] = sentence_split[i] + " " + tags[i].split()[2]
	sentence_split[len(sentence_split)-1] = sentence_split[len(sentence_split)-1] + " " + tags[len(tags)-1].split()[2]
	#print sentence_split
	return "\n".join(sentence_split) + "\n\n"
	"""
	output = ""
	i = 1
	for word in sentence_split:
		if word not in ['\n', '\r\n']:
			print tags[i]
			#word += " " + tags[i].split()[1]
			output += word + " " + tags[i].split()[1] + "\n"
			i += 1
	output += "\n"
	#output = "\n".join(sentence_split)
	print output
	return output
	"""

if __name__ == '__main__':

	#output = enum_server2.communicate("There\nis\nno\nasbestos\nin\nour\nproducts\nnow\n.\n")
	#print output
	
	populateWeights('tag.model')
	
   	f = open('tag_dev.dat','r')
   	g = open('tag_dev.out','w')
	
	sentences = f.read().split("\n\n")
	for sentence in sentences:
		y_star = decode(sentence)
		#output = y_star
		output = formatOutput(sentence,y_star)
		g.write(output)


	f.close()
	g.close()
	