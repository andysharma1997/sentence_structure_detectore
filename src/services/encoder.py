import spacy

from src.utilities import sken_logger, sken_singleton
from textblob import TextBlob
import re

logger = sken_logger.get_logger("Encodeer")


def return_clean_text(sentence):
    logger.info("Cleaning sentence:{}".format(sentence))
    return re.sub(r'[^a-zA-Z ]+', '', sentence).lower()


def sentence_breaker(sentence):
    """
    This method extracts all the sentences present in a single long sentence using TextBlob
    @param sentence: str
    @return: list of sentences present
    """
    if len(sentence.split()) > 0:
        testimonial = TextBlob(sentence)
        sentences = []
        for sent in testimonial.sentences:
            sentences.append(str(sent))
        return sentences


def get_tagged_sequence(sentence):
    clean_text = return_clean_text(sentence)
    tagger = sken_singleton.Singletons.get_instance().get_tagger()
    doc = sken_singleton.Singletons.get_instance().get_nlp(clean_text)
    logger.info("Made {} tokens for sentence={}".format(len(doc), sentence))
    resp = {"sentence": sentence, "sequence": ''}
    context_verbs = []
    context_nouns = []
    for token in doc:
        if 'W' in token.tag_:
            if str(token) in tagger['wquestions']:
                resp['sequence'] += "<wquestion>"
            else:
                resp['sequence'] += '<' + str(spacy.explain(token.pos_)) + '>'
        elif 'VERB' in token.pos_:
            if str(token) in tagger["context_verb"]:
                resp["sequence"] += '<context_verb>'
                context_verbs.append(str(token))
            else:
                resp['sequence'] += '<' + str(spacy.explain(token.pos_)) + '>'
        elif 'NOUN' in token.pos_:
            if str(token) in tagger['context_noun']:
                resp['sequence'] += "<context_noun>"
                context_nouns.append(str(token))
            else:
                resp['sequence'] += '<' + str(spacy.explain(token.pos_)) + '>'
        else:
            resp['sequence'] += '<' + str(spacy.explain(token.pos_)) + '>'
    return resp, context_nouns, context_verbs
