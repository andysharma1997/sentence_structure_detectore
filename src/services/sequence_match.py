from src.utilities import sken_logger, sken_singleton
from src.services import encoder

logger = sken_logger.get_logger("Sequence_match")


def interogation_detectore(sentence):
    ver_tags = ["VBZ", "VB", "VBD", "VBG", "VBN", "VBP"]
    doc = sken_singleton.Singletons.get_instance().get_nlp(sentence)
    matches = sken_singleton.Singletons.get_instance().get_phrase_matcher(doc)
    if len(matches) != 0:
        first_filter = doc[matches[0][1]:]
        tag_list = [item.tag_ for item in first_filter]
        dep_list = [item.dep_ for item in first_filter]

        if "subj" in first_filter[0].dep_ or "obj" in first_filter[0].dep_:
            return {"question": str(first_filter), "subject": "will be in answer",
                    "tag": "direct-question without subject"}

        try:
            flag = False
            for i in range(1, len(tag_list)):
                for j in range(i + 1, len(tag_list)):
                    if tag_list[i] in ver_tags and "nsubj" in dep_list[j]:
                        print(j, dep_list[j])
                        flag = True
                        subject_index = j
                        break
            if flag:
                return {"question": str(first_filter), "subject": str(first_filter[subject_index]),
                        "tag": "direct-question"}
        except IndexError:
            pass
    elif doc[0].pos_ == "VERB" or doc[0].tag_ in ver_tags:
        if "neg" in doc[1].dep_:
            if doc[2].tag_ in ver_tags and "nsubj" not in [item.dep_ for item in doc]:
                subject = []
                objects = []
                for tok in doc:
                    if "subj" in tok.dep_:
                        subject.append(str(tok))
                    if "obj" in tok.dep_:
                        objects.append(str(tok))
                return {"question": str(sentence), "subject": subject, "object": objects,
                        "tag": "negation yes/no question"}
            if doc[2].tag_ in ver_tags and "nsubj" in [item.dep_ for item in doc]:
                subject = []
                objects = []
                for tok in doc:
                    if "subj" in tok.dep_:
                        subject.append(str(tok))
                    if "obj" in tok.dep_:
                        objects.append(str(tok))
                return {"question": str(sentence), "subject": str(doc[[item.dep_ for item in doc].index("nsubj")]),
                        "objects": objects, "tag": "negation yes/no question"}
        else:
            if ("nsubj" in doc[1].dep_) or ("DET" in doc[1].pos_ and "nsubj" in doc[2].dep_):
                if "or" in [str(item) for item in doc]:
                    return {"question": str(sentence), "tag": "aleternative interrogative"}
                subject = []
                objects = []
                for tok in doc:
                    if "subj" in tok.dep_:
                        subject.append(str(tok))
                    if "obj" in tok.dep_:
                        objects.append(str(tok))
                return {"question": str(sentence), "subject": subject, "objects": objects, "tag": "yes/no question"}

    else:
        return "not a question"


def return_idx(sentence):
    sequence, context_nouns, context_verbs = encoder.get_tagged_sequence(sentence)
    sequence_indexes = sken_singleton.Singletons.get_instance().get_sequence_idx()
    result = {"matching_pattern_sentences": [], "matched_idx": []}
    for i, val in enumerate(sequence_indexes.isin([sequence["sequence"]], level='sequence')):
        if val:
            result['matching_pattern_sentences'].append(sequence_indexes[i][0])
            result['matched_idx'].append(i)
            result['pattern_matched'] = sequence
            result['input_sentence'] = sentence
            result['context_nouns'] = context_nouns
            result['context_verbs'] = context_verbs
        else:
            result["input_sentence"] = sentence
    return result


def check_lq_match(snippet):
    sentences = encoder.sentence_breaker(snippet)
    matched = list(map(return_idx, sentences))
    resp = []
    for match in matched:
        if len(match['matching_pattern_sentences']) != 0:
            resp.append(
                {"Sentence": match["input_sentence"], "Is_lq": True,
                 "Question_type": interogation_detectore(match["input_sentence"]),
                 "Context_noun": match['context_nouns'], "Context_Verb": match["context_verbs"]})
        else:
            resp.append({"Sentence": match['input_sentence'], "Is_lq": False})
    return resp
