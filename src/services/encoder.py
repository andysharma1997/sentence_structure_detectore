import spacy

from src.utilities import sken_logger, sken_singleton
import re

logger = sken_logger.get_logger("Encodeer")


def return_clean_text(sentence):
    logger.info("Cleaning sentence:{}".format(sentence))
    return re.sub(r'[^a-zA-Z ]+', '', sentence).lower()


def get_tagged_sequence(sentence):
    clean_text = return_clean_text(sentence)
    tagger = sken_singleton.Singletons.get_instance().get_tagger()
    doc = sken_singleton.Singletons.get_instance().get_nlp(clean_text)
    logger.info("Made {} tokens for sentence={}".format(len(doc),sentence))
    resp = {"sentence": sentence, "sequence": ''}
    for token in doc:
        if 'W' in token.tag_:
            if str(token) in tagger['wquestions']:
                resp['sequence'] += "<wquestion>"
            else:
                resp['sequence'] += '<' + str(spacy.explain(token.pos_)) + '>'
        elif 'VERB' in token.pos_:
            if str(token) in tagger["context_verb"]:
                resp["sequence"] += '<context_verb>'
            else:
                resp['sequence'] += '<' + str(spacy.explain(token.pos_)) + '>'
        elif 'NOUN' in token.pos_:
            if str(token) in tagger['context_noun']:
                resp['sequence'] += "<context_noun>"
        else:
            resp['sequence'] += '<' + str(spacy.explain(token.pos_)) + '>'
    return resp


