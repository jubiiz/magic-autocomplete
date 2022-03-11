from gensim.models import Word2Vec

card = "counterspell"

m = Word2Vec.load('w2v_models/m3.model')

print('FINDING SIMILAR TO: ', card)
for similar in m.wv.most_similar(card):
    print(similar[0])