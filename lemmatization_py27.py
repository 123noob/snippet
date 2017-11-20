from pattern.en import lemma

words = []
with open('result.txt') as f:
	for w in f.readlines():
		words.append(lemma( w.strip() ) )

with open('result2.txt','w+') as w:		
	for word in list(set(words) ):
		if len(word) > 4:
			w.write(word+'\n')
