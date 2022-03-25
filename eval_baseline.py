from gensim.models import Word2Vec
from matplotlib import pyplot as plt
import os
import random

# loads Word2Vec model
WV = Word2Vec.load("w2v_models/m3.model")
WV = WV.wv

def load_conversion():
    # returns a conversion table organized as {f_name: uf_name}
    f_temp = []
    uf_temp = []
    with open("f_singles.txt", "r") as r:
        for line in r:
            line = line.rstrip("\n")
            f_temp.append(line)
        
    with open("uf_singles.txt", "r") as r:
        for line in r:
            line = line.rstrip("\n")
            uf_temp.append(line)

    conversion = dict(zip(f_temp, uf_temp))
    return(conversion)

def card_from_cards(known, correction):
    """
    given a list of formated cardnames "known"
    return a prediction of the next card
    apply correction if "correction" is True
    """
    # correction parameter prevents >4 of the same card to appear in a list
    if correction == True:
        pred_card = random.choice(known)
        i=0
        while known.count(pred_card) == 4 and i<len(known):
            pred_card = known[i]
            i+=1
        # if every card is there in quadruple, pick a random card
        if known.count(pred_card) == 4:
            conversion = load_conversion()
            f_singles = list(conversion.keys())
            pred_card = random.choice(f_singles)
    else:
        pred_card = random.choice(known)
    
    return(pred_card)

def list_from_cards(inputs):
    """
    takes a list of known cards "inputs"
    returns a predicted list
    """
    prediction = inputs
    len_inputs = len(inputs)

    while len(prediction) < 60:
        # predict the next card given "prediction" as known cards
        next_card = card_from_cards(prediction, True)
        prediction.append(next_card)

    return(prediction[len_inputs:])

def cardvec_from_vectors(known_names, known_vecs, wv, correction): 
    """
    takes as input a list of card vectors ("known")
    outputs a next card name and next card vector
    applies correction if "correction" is True
    """
    if correction == True:
        cardname = random.choice(known_names)
        cardvec = wv[cardname]
        i = 0 # index of most_similar
        j = 0 # index of known
        while known_names.count(cardname) == 4:
            similar_to = known_vecs[j]
            cardname = wv.most_similar(similar_to)[i][0]
            cardvec = wv[cardname]

            j += 1
            if j == len(known_names):
                j = 0
                i += 1
                if i == 10: # all new vector predictions are predicted; extremely unlikely, but if so it gets 1 wrong
                    return(cardname, cardvec)

    else:
        similar_to = random.choice(known_vecs)
        # we don't want the first most similar:
        # it'll always be the same card
        cardname = wv.most_similar(similar_to)[1][0] 
        cardvec = wv[cardname]
        
    return(cardname, cardvec)

def list_from_vectors(input_names):
    """
    takes as input a list of cardnames
    returns a predicted lists
    predicts from most similar vectors
    """
    # yes I know this is useless, pred_name just points to the same list as input_names
    # I should at least be writing input_names.copy(), but that wouldn't change anything either
    pred_names = input_names
    len_input_names = len(input_names)

    # we also want a list of card vectors
    pred_vecs = [WV[cardname] for cardname in input_names]

    while len(pred_names) < 60:
        next_cardname, next_cardvec = cardvec_from_vectors(pred_names, pred_vecs, WV, True)
        pred_vecs.append(next_cardvec)
        pred_names.append(next_cardname)

    return(pred_names[len_input_names:])

def get_accuracy(prediction, target):
    """
    computes the accuracy of prediction based on target
    returns the ratio of unique pairs of cards between the two
    """
    score = 0
    len_target = len(target)
    for card in prediction:
        if card in target:
            score += 1
            target.remove(card) 
    return(score/len_target)

def update_scores(scores, cards):
    """
    for a given decklist "cards", makes predictions with 1, 5, 15..., 55, 59 cards
    updates the prediction accuracy dictionary "scores" after each prediction
    """
    random.shuffle(cards)
    # must find a list given "len_inputs" input cards
    for len_inputs in scores:        
        inputs, target = cards[:len_inputs], cards[len_inputs:]
        prediction = list_from_vectors(inputs)
        accuracy = get_accuracy(prediction, target)
        scores[len_inputs] += accuracy

    return(scores)



def plot_scores(scores):
    """
    takes in a dictionary of prediction accuracy per number of input cards
    plots a bar graphs of the accuracy per number of input cards
    """
    num_known, score = list(scores.keys()), list(scores.values())
    fig, ax = plt.subplots(1, 1)

    ax.bar(num_known, score)

    ax.set_ylim(0, 1)

    ax.set_title("VY")
    ax.set_xlabel("Number of Known Cards")
    ax.set_ylabel("Accuracy Ratio")

    plt.show()


def main():
    lists_path = os.path.join(os.getcwd(), "f_lists")
    lists_dir = os.scandir(lists_path)

    # how well does the algorithm perform when we give it i=1->59 cards
    scores = {i:0 for i in range(1, 60)}
    numlists = 0

    # update scores for each list
    for archetype in lists_dir:
        archetype_dir = os.scandir(archetype.path)
        # loops over decklists of that archetype
        for decklist in archetype_dir:
            cards = []
            # loads every card of the decklist
            with open(decklist.path, "r") as r:
                for line in r:
                    cardname = line.rstrip("\n")
                    if len(line) == 0:
                        continue
                    cards.append(cardname)
                # only keep length 60 lists
                if(len(cards) != 60):
                    cards = cards[:60]
            # calculate efficiency with this list, update scores
            scores = update_scores(scores, cards)
            numlists += 1
            print(numlists)

    # normalize scores (average them: up to now accuracies were just added up. Now we divide by the number of attempts)
    print(scores)
    for num_cards, score in scores.items():
        scores[num_cards] = score/numlists
    print(scores)

    # plots scores
    plot_scores(scores)
    

if __name__ == "__main__":
    main()