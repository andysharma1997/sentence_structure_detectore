from src.utilities import sken_logger
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher

import os

logger = sken_logger.get_logger("Singleton")


class Singletons:
    __instance = None
    tagger = None
    nlp = None
    sequence_idx = None
    phrase_matcher = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Singletons.__instance is None:
            logger.info("Calling Singletone private constructor")
            Singletons()
        return Singletons.__instance

    def __init__(self):
        if Singletons.__instance is not None:
            raise Exception("This class is a singleton!")
        else:

            logger.info("Initializing token tagger")
            df = pd.read_pickle(os.path.join(os.getcwd(), "src/resources/encoder2.pkl"))
            context_noun = df["context_noun"].to_list()
            question = df["wquestions"].to_list()
            contex_verb = df["context_verb"].to_list()
            self.tagger = {"context_noun": context_noun, "wquestions": question, "context_verb": contex_verb}
            logger.info("Creating spacy tagger")
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Making phrase matcher")
            self.phrase_matcher = PhraseMatcher(self.nlp.vocab, attr='LOWER')
            question_terms = ["who", "whom", "whose", "what", "when", "where", "why", "which", "how"]
            patterns = [self.nlp(text) for text in question_terms]
            self.phrase_matcher.add("question", None, *patterns)
            logger.info("Making sequence indexes")
            self.sequence_idx = pd.MultiIndex.from_frame(
                pd.read_pickle(os.path.join(os.getcwd(), 'src/resources/sequence1.pkl')))
            Singletons.__instance = self

    def get_tagger(self):
        return self.tagger

    def get_nlp(self, sentence):
        return self.nlp(sentence)

    def get_sequence_idx(self):
        return self.sequence_idx

    def get_phrase_matcher(self, doc):
        return self.phrase_matcher(doc)
