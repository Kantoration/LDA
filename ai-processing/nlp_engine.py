import spacy

nlp = spacy.load("en_core_web_sm")

def process_nlp_command(command):
    """Extracts intent, object, and parameters from the NLP command."""
    doc = nlp(command)
    parsed_data = {
        "action": None,
        "object": None,
        "location": None,
        "quantity": None
    }

    for token in doc:
        # Identify actions (verbs)
        if token.pos_ == "VERB":
            parsed_data["action"] = token.lemma_

        # Identify objects (nouns)
        if token.pos_ == "NOUN":
            if "light" in token.text.lower():
                parsed_data["object"] = "lighting fixture"

        # Identify quantities
        if token.like_num:
            parsed_data["quantity"] = int(token.text)

    return parsed_data
