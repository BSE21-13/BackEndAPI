import re
import os
# import PyPDF2
import enchant
import spacy
from flask import Flask, json
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin

from spacy.tokens import Span
from spacy.matcher import PhraseMatcher
from spacy.language import Language
from scipy import spatial

load_dotenv() 

# Defining spacy NLP Medium Model
nlp = spacy.load('en_core_web_md')
# create dictionary for the language
# in use(en_US here)
enchant_dict = enchant.Dict("en_US")

# method for reading a pdf file
def readTextFile(filename, folder_name):
    # storing path of PDF-Documents folder
    data_path = str(os.getcwd()) + "\\" + folder_name

    file = open(data_path + "\\" + filename, mode="rb")
    text = file.read()
    text = text.decode("ansi")
    #txt = text.replace("\n", " ")
        
    # creating a single string containing full text
    #full_text = "".join(text)

    return text

# customer sentence segmenter for creating spacy document object
@Language.component('en_sentence')
def setCustomBoundaries(doc):
    # traversing through tokens in document object
    for token in doc[:-1]:
        if token.text == ';':
            doc[token.i + 1].is_sent_start = True
        if token.text == ".":
            doc[token.i + 1].is_sent_start = False
    return doc


# create spacy document object from pdf text
def getSpacyDocument(pdf_text, nlp):
    main_doc = nlp(pdf_text)  # create spacy document object

    return main_doc

# convert keywords to vector
def createKeywordsVectors(keyword, nlp):
    doc = nlp(keyword)  # convert to document object

    return doc.vector


# method to find cosine similarity
def cosineSimilarity(vect1, vect2):
    # return cosine distance
    return 1 - spatial.distance.cosine(vect1, vect2)


# method to find similar words
def getSimilarWords(keyword, nlp):
    similarity_list = []

    keyword_vector = createKeywordsVectors(keyword, nlp)

    for tokens in nlp.vocab:
        if tokens.has_vector:
            if tokens.is_lower:
                if tokens.is_alpha:
                    similarity_list.append((tokens, cosineSimilarity(keyword_vector, tokens.vector)))

    similarity_list = sorted(similarity_list, key=lambda item: -item[1])
    similarity_list = similarity_list[:30]

    top_similar_words = [item[0].text for item in similarity_list]

    top_similar_words = top_similar_words[:3]
    top_similar_words.append(keyword)

    for token in nlp(keyword):
        top_similar_words.insert(0, token.lemma_)

    for words in top_similar_words:
        if words.endswith("s"):
            top_similar_words.append(words[0:len(words) - 1])

    top_similar_words = list(set(top_similar_words))

    top_similar_words = [words for words in top_similar_words if enchant_dict.check(words) == True]

    return ", ".join(top_similar_words)


# method for searching keyword from the text
def search_for_keyword(keyword, doc_obj, nlp):
    phrase_matcher = PhraseMatcher(nlp.vocab)
    phrase_list = [nlp(keyword)]
    phrase_matcher.add("Text Extractor", None, *phrase_list)

    matched_items = phrase_matcher(doc_obj)

    matched_text = []
    matched_start_position = []
    for match_id, start, end in matched_items:
        text = nlp.vocab.strings[match_id]
        span = doc_obj[start: end]
        matched_text.append(span.sent.text)
        matched_start_position.append(start)
        
    return {"matched_text" : matched_text, "start_positions": matched_start_position}


def getTitle(titles, sent_start):
    req_title = None
    near_titles = []
    for title in titles:
        if sent_start > title[0]:
            near_titles.append(title[0])
    
    near_titles.sort()
    
    title_index = near_titles[-1]
    
    
    for item in titles:
        if item[0] == title_index:
            req_title = item[2]
           
            
    
    return req_title
            
# Importing resource for indexing
pdffile = readTextFile('PlainConstitution.txt', './resources/')
pdffile = pdffile.lower()
# print(pdffile)

doc = getSpacyDocument(pdffile, nlp)

# adding setCustomBoundaries to the pipeline
nlp.add_pipe('en_sentence', before='parser')

# configuring regex matcher for the chapter titles
r_nlp = spacy.blank("en")
r_doc = r_nlp(pdffile)

# defining regex pattern for token enclosed in square braces
pattern = r"\[(.*?)\]" 
mwt_ents = []

# iterate over the document object while appending matched tokens
for match in re.finditer(pattern, r_doc.text):
    start, end = match.span()
    span = r_doc.char_span(start, end)
   
    if span is not None:
        mwt_ents.append((span.start, span.end, span.text))
print(mwt_ents)
# for ent in mwt_ents:
#     start , end , name = ent

keywords = 'president'
similar_keywords = getSimilarWords(keywords, nlp)
similar_keywords = similar_keywords.split(", ")
print( similar_keywords)

results = []
positions = []

# for word in similar_keywords:
#     print(word)
#     result = search_for_keyword(word, doc, nlp)
#     results += result["matched_text"]
#     positions += result["start_positions"]

result = search_for_keyword('president, vice, delegate', doc, nlp)

print(f'Total results are {len(result)}')

title_list = []
for item in positions:
    title_list.append(getTitle(mwt_ents,item))

for item in result:
    print('*****')
    print(item)
    print('***** \n')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = 'secret_key'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo  = PyMongo(app)
    
@app.route('/search', methods=['GET'])
@cross_origin()
def query_resource():
    queryString = request.args.get('q')
    results = {
        "keywords":[title_list, "law", "state", "prosecution", "police", "unfair", "appeal"], 
        
    "results" : [{
        
        "chapter":"Chapter 1",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    },
    {
        "chapter":"Chapter 13",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    },
    {
        "chapter":"Chapter 11",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    },
    {
        "chapter":"Chapter 8",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    },
    {
        "chapter":"Chapter 5",
        "text":" The  people  shall  express  their  will  and  consent  on  who  shall govern them and how\nthey should be governed, through regular, free and fair elections of their representatives or through referenda.",
    }
    ]}

    resp = jsonify(results)
    resp.status_code = 200
    return resp


@app.errorhandler(404)
@cross_origin()
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ :
    app.run(debug=True)


