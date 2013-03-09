import nltk
from nltk.corpus import stopwords
from nltk import tag,tokenize
#sentence = "this dc comics superhero swims at high speeds & communicates telepathically with sea creatures"
sentence = "types of these cards used in digital cameras include MicroSD SDHC & CompactFlash"

def wants(tex,full):
	want = ''
	if "this" in tex:
		for item in full:
			counter = 0
			if item[0] == "this":
				tmcounter = counter
				while full[tmcounter+1][1] not in ['NN','NNP','NNS','NNPS']:
					tmcounter += 1
					want += full[tmcounter+1][0]
				return want
			counter += 1
def gen_query(tex):
	word_list = tex.split(" ")
	filtered_words = [w for w in word_list if not w in stopwords.words('english')]
	#full = nltk.pos_tag(tex)
	query = ''
	for word in filtered_words:
        	query += word + ' '
	fulltags = make_tags(query)
	return(fulltags)

def make_tags(text_a):
	sents = tokenize.sent_tokenize(text_a)
	sents2 = tokenize.word_tokenize(sents[0])
	tagged = tag.pos_tag(sents2)
	new_query = ''
	for elem in tagged:
		string = elem[0]
		if(elem[1] in ['NNP','NNPS','SD']):
			new_query += str('"'+string+'" ')
		elif(elem[1] not in ['VBZ','VBG']):
			new_query += str(string + " ")
	datafilt = new_query + " site:wikipedia.org"
	return datafilt

def test():
	print(gen_query(sentence))
