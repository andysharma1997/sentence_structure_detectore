from src.utilities import sken_logger, sken_singleton
from src.services import encoder


logger = sken_logger.get_logger("Sequence_match")


def return_idx(sentence):
    sequence = encoder.get_tagged_sequence(sentence)
    sequence_indexes = sken_singleton.Singletons.get_instance().get_sequence_idx()
    result = {"matching_pattern_sentences": [], "matched_idx": []}
    for i, val in enumerate(sequence_indexes.isin([sequence["sequence"]], level='sequence')):
        if val:
            result['matching_pattern_sentences'].append(sequence_indexes[i][0])
            result['matched_idx'].append(i)
            result['pattern_matched']=sequence
    return result



