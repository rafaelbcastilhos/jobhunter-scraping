import spacy
nlp = spacy.load("pt_core_news_lg")


def search_company_name(text):
    doc = nlp(text)
    items = []
    counts = dict()

    print(doc.ents)
    for entity in doc.ents:
        if entity.label_ == "ORG":
            items.append(entity.text)

    for i in items:
        counts[i] = counts.get(i, 0) + 1

    return max(counts, key=counts.get)
