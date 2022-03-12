from gensim.models import Word2Vec
from matplotlib import pyplot as plt
import os
import random

def load_conversion():
    # returns a conversion table of shape {f_name: uf_name}
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
    if correction == True:
        pred_card = random.choice(known)
        i=0
        while known.count(pred_card) == 4 and i<len(known):
            pred_card = known[i]
            i+=1
        # if no card in the list is not there in quadruple, pick a random card
        if known.count(pred_card) == 4:
            conversion = load_conversion()
            f_singles = list(conversion.keys())
            pred_card = random.choice(f_singles)
    return(pred_card)

def list_from_cards(inputs):
    prediction = inputs
    len_inputs = len(inputs)

    while len(prediction) < 60:
        # predict the next card given "prediction" as known cards
        next_card = card_from_cards(prediction, True)
        prediction.append(next_card)

    return(prediction[len_inputs:])

def card_from_vectors(known, correction):
    pass



def get_accuracy(prediction, target):
    score = 0
    len_target = len(target)
    for card in prediction:
        if card in target:
            score += 1
            target.remove(card) 
    return(score/len_target)

def update_scores(scores, cards):
    random.shuffle(cards)
    # must find a list given "len_inputs" input cards
    for len_inputs in scores:        
        inputs, target = cards[:len_inputs], cards[len_inputs:]
        prediction = list_from_cards(inputs)
        accuracy = get_accuracy(prediction, target)
        scores[len_inputs] += accuracy

    return(scores)



def plot_scores(scores):
    num_known, score = list(scores.keys()), list(scores.values())
    fig, ax = plt.subplots(1, 1)

    ax.bar(num_known, score)

    ax.set_ylim(0, 1)

    ax.set_title("SY")
    ax.set_xlabel("Number of Known Cards")
    ax.set_ylabel("Accuracy Ratio")

    plt.show()


def main():
    lists_path = os.path.join(os.getcwd(), "f_lists")
    lists_dir = os.scandir(lists_path)

    # how well does the algorithm perform when we give it i=1->59 cards
    scores = {i:0 for i in range(1, 59)}
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