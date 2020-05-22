from src.utilities import sken_logger
import pandas as pd
import spacy
import os

logger = sken_logger.get_logger("Singleton")


class Singletons:
    __instance = None
    tagger = None
    nlp = None
    sequence_idx = None

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
            df = pd.read_pickle(os.path.join(os.getcwd(), "src/resources/encoder.pkl"))
            context_noun = df.contextnoun.to_list() + df.domain_noun.to_list() + df.noun.to_list()
            question = df.wquestion.to_list()
            contex_verb = df.verb.to_list() + df.verv.to_list()
            self.tagger = {"context_noun": context_noun, "wquestions": question, "context_verb": contex_verb}
            logger.info("Creating spacy tagger")
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Making sequence indexes")
            self.sequence_idx = pd.MultiIndex.from_frame(
                pd.read_pickle(os.path.join(os.getcwd(), 'src/resources/sequence.pkl')))
            Singletons.__instance = self

    def get_tagger(self):
        return self.tagger

    def get_nlp(self, sentence):
        return self.nlp(sentence)

    def get_sequence_idx(self):
        return self.sequence_idx
