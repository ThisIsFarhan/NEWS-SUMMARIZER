import spacy
from nltk.stem import PorterStemmer
nlp = spacy.load("en_core_web_sm")

def preprocess(text):
  stemmer = PorterStemmer()
  doc = nlp(text)
  filtered = []
  for token in doc:
    if token.is_stop or token.is_punct:
      continue
    elif token.tag_ == "NNS":
      filtered.append(stemmer.stem(token.text))
    else:
      filtered.append(token.text)
  return " ".join(filtered)

def create_keyword_table(filtered_sentences, title):
  keyword_table = {}
  #collecting and adding title words in the table
  title_keylist = []
  for token in nlp(title):
    if token.is_stop:
      continue
    title_keylist.append(token.text)
  for word in title_keylist:
    keyword_table[word] = title_keylist.count(word)/len(title_keylist)


  #collecting ner, nouns, cardinal for each sentence
  for sentence in filtered_sentences:
    #ner
    NER_keylist = []
    for ent in nlp(sentence).ents:
      if ent.label_ == "PERSON" or ent.label == "ORG" or ent.label == "LOC":
        NER_keylist.append(ent.text)
    for word in NER_keylist:
      keyword_table[word] = NER_keylist.count(word)/len(NER_keylist)

    # #NP
    # NP_keylist = []
    # CARD_keylist = []
    # for chunk in nlp(sentence).noun_chunks:
    #   for ent in chunk.ents:
    #     if ent.label_ == 'CARDINAL':
    #       CARD_keylist.append(ent.text)
    #   NP_keylist.append(chunk.text)
    # for word in NP_keylist:
    #   keyword_table[word] = NP_keylist.count(word)/len(NP_keylist)
    # for word in CARD_keylist:
    #   keyword_table[word] = CARD_keylist.count(word)/len(CARD_keylist)

    #NOUNS
    NOUN_keylist = []
    for token in nlp(sentence):
      if token.pos_ == "NOUN":
        NOUN_keylist.append(token.text)
    for word in NOUN_keylist:
      keyword_table[word] = NOUN_keylist.count(word)/len(NOUN_keylist)

    #CARD
    CARD_keylist = []
    for token in nlp(sentence).ents:
      if token.label_ == "CARDINAL":
        CARD_keylist.append(token.text)
    for word in CARD_keylist:
      keyword_table[word] = CARD_keylist.count(word)/len(CARD_keylist)


  TT = []
  combined = " ".join(filtered_sentences)
  for token in nlp(combined):
    if token.is_stop or token.is_punct:
      continue
    TT.append(token.text)
  for term in TT:
    if term not in keyword_table:
      if TT.count(term)/len(TT) >= 0.1 and TT.count(term)/len(TT) <= 0.15:
        keyword_table[term] = TT.count(term)/len(TT)

  return keyword_table

def score_sentence(sentence, keyword_table):
  score = 0
  for token in nlp(sentence):
    if token.text in keyword_table:
      score += keyword_table[token.text]
  return score

def similarityscore(s1, s2, keyword_table):
  simScore = 0
  num = 0
  denom = 0
  s1_temp = 0
  s2_temp = 0
  s1_length = 0
  s2_length = 0

  sent1 = nlp(s1)
  sent2 = nlp(s2)

  common_terms = set(token.text for token in sent1) & set(token.text for token in sent2)
  for term in common_terms:
    if term in keyword_table:
      num += (keyword_table[term])**2

  for token in sent1:
    if token.text in keyword_table:
      s1_temp += (keyword_table[token.text])**2
  s1_length = (s1_temp)**(1/2)

  for token in sent2:
    if token.text in keyword_table:
      s2_temp += (keyword_table[token.text])**2
  s2_length = (s2_temp)**(1/2)

  denom = s1_length * s2_length
  if denom == 0:
    denom = 0.00000001
  return num/denom

def summarize(text, title, summarizer_percent):
    text = text.replace("\n", " " )
    doc = nlp(text)
  
    sentences = []
    for sent in doc.sents:
        sentences.append(sent.text.strip())

    filtered_sentences = [preprocess(sent) for sent in sentences]
    keyTable = create_keyword_table(filtered_sentences, title)

    score_list = []
    for sentence in filtered_sentences:
        score_list.append(score_sentence(sentence, keyTable))
    score_list[0] = max(score_list) + 1 #setting the score of the first sentence of the article as the highest as per the paper

    sentence_dustbin = []
    score_dustbin = []

    i = 0
    while i < len(sentences) - 1:
      innerCounter = i+1
      while innerCounter < len(sentences):
        if similarityscore(filtered_sentences[i],filtered_sentences[innerCounter], keyTable) > 0.3:
          if score_list[i] > score_list[innerCounter]:
            sentence_dustbin.append(sentences[innerCounter])
            score_dustbin.append(score_list[innerCounter])
          else:
            sentence_dustbin.append(sentences[i])
            score_dustbin.append(score_list[i])
        innerCounter = innerCounter + 1
      i = i + 1

    sentence_dustbin = list(set(sentence_dustbin))
    for senten in sentence_dustbin:
      index = sentences.index(senten)
      sentences.pop(index)
      score_list.pop(index)

    summary_output = []
    N = int((summarizer_percent/100)*len(sentences))
    res = sorted(range(len(score_list)), key = lambda sub: score_list[sub])[-N:]
    res = reversed(res)
    for n in res:
        summary_output.append(sentences[n])
    return " ".join(summary_output)

# text = """In a groundbreaking move for the tech industry, QuantumCom has announced the launch of its first commercially available quantum computer, the Q-1. This state-of-the-art machine leverages the principles of quantum mechanics to perform computations at speeds exponentially faster than traditional supercomputers. The Q-1 is expected to revolutionize fields such as cryptography, drug discovery, and financial modeling by solving complex problems that were previously intractable. With its ability to process massive datasets in parallel, QuantumCom's Q-1 opens up new possibilities for artificial intelligence, climate modeling, and optimization challenges. Industry experts are hailing this as a pivotal moment in computing history, marking the beginning of the quantum era."""
# title = " "



