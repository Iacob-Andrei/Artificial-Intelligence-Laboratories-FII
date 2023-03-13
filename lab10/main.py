import nltk
from rdflib import Graph
import random

relations = []


def ex1():
    # nltk.download("punkt")
    sentence = "Buffy wants a lot of food."
    tokens = nltk.word_tokenize(sentence)
    print(tokens)


def ex2():
    global relations
    g = Graph()
    g.parse("food.rdf")
    for concept1, relation, concept2 in g:
        if '#' in concept1 and '#' in relation and '#' in concept2:
            relations.append((concept1.split('#')[1], relation.split('#')[1], concept2.split('#')[1]))
    # print(*relations, sep='\n')


def generate_question():
    triplet = random.choice(relations)
    rand_el = random.randint(0, 2)

    if rand_el == 1:
        question = f"What is the relation between {triplet[0]} and {triplet[2]}?"
        answer = [triplet[1]]
    elif rand_el == 0:
        question = f"? - {triplet[1]} - {triplet[2]}"
        answer = find_answer(triplet[1], triplet[2], 0)
    else:
        question = f"{triplet[0]} - {triplet[1]} - ?"
        answer = find_answer(triplet[1], triplet[0], 1)

    return question, answer


def find_answer(relation, concept, flag):
    answers = []
    for con1, rel, con2 in relations:
        if flag == 0:
            if rel == relation and con2 == concept:
                answers.append(con1)
        else:
            if rel == relation and con1 == concept:
                answers.append(con2)
    return answers


def ex3():
    while input("Want question? ") != "no":
        question, response = generate_question()
        print(question)
        answer = input(f"{'Your answer is: '}")
        if answer not in response:
            print("Wrong answer!")
            print(f"Correct answers:{response}")
        else:
            print("Congrats!")


def ex4():
    word = input("Insert a word to search in WordNet: ")
    synsets = nltk.corpus.wordnet.synsets(word)

    for synset in synsets:
        print(f"Definition: {synset.definition()}")
        print(f"Examples: {synset.examples()}\n")


def find_synonyms(word: str):
    synonyms = set()
    for syn in nltk.corpus.wordnet.synsets(word)[:1]:
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms


def find_hypernyms(word: str):
    hypernyms = set()
    for syn in nltk.corpus.wordnet.synsets(word)[:1]:
        for hyper in syn.hypernyms():
            hypernyms.add(hyper.name().split(".")[0])
    return hypernyms


def find_meronyms(word: str):
    meronyms = set()
    for syn in nltk.corpus.wordnet.synsets(word)[:1]:
        for meron in syn.part_meronyms():
            meronyms.add(meron.name().split(".")[0])
    return meronyms


def ex5():
    while input("Want question? ") != "no":
        question, responses = generate_question()
        print(question)

        synonyms = set(responses)
        hypernyms = set()
        meronyms = set()

        for response in responses:
            synonyms |= find_synonyms(response)
            hypernyms |= find_hypernyms(response)
            meronyms |= find_meronyms(response)

        print(f"\nsynonyms + answers are: {synonyms}")
        print(f"hypernyms: {hypernyms}")
        print(f"meronyms: {meronyms}\n")

        answer = input(f"{'Your answer is: '}")

        if answer in synonyms:
            print("Congrats!")
        elif answer in hypernyms:
            print("Congrats! You found a hypernym")
        elif answer in meronyms:
            print("Congrats! You found a meronym")
        else:
            print("Wrong answer!")


ex2()
# ex3()
# ex4("dog")
ex5()
