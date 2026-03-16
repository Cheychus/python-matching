from owlready2 import *
from config import ONTOLOGIES_LIST, RAW_DIR, PARSED_DIR
import json


def normalize(value, append=""):
    if not value:
        return ""

    if isinstance(value, list):
        return append + " ".join(normalize(v) for v in value if v)

    if hasattr(value, "value"):
        return append + str(value.value)

    return append + str(value)


def parseOntology(ontologyName: str):
    print("Parse:", ontologyName)
    path = RAW_DIR / ontologyName
    onto: Ontology = get_ontology(str(path) + ".owl").load()
    synonymAttr = []
    for prop in onto.annotation_properties():
        if "synonym" in prop.name.lower():
            synonymAttr.append(prop.name)

    terms = []

    for cls in onto.classes():
        name = cls.name
        type = "class"
        label = cls.label.first()
        comment = cls.comment
        seeAlso = cls.seeAlso
        exampleOfUsage = getattr(cls, "IAO_0000112", [])
        definition = getattr(cls, "IAO_0000115", [])
        editorNote = getattr(cls, "IAO_0000116", [])
        alternativeTerm = getattr(cls, "IAO_0000118", [])
        synonyms = []

        for attr in synonymAttr:
            values = getattr(cls, attr, [])

            for v in values:
                synonyms.append(str(v))
                # synonyms.append({
                #     "type": attr,
                #     "value": str(v)
                # })

        fields = [
            normalize(label),
            normalize(definition, "Definition: "),
            # normalize(comment, "Comment: "),
            # normalize(editorNote, "Editor note: "),
            normalize(alternativeTerm, "Alternative Term: "),
            normalize(synonyms, "Synonyms: "),
        ]

        embeddingInput = " ".join(filter(None, fields))

        term = {
            "id": cls.name,
            "type": type,
            "label": label,
            "definition": definition,
            "editorNote": editorNote,
            "comment": comment,
            "alternativeTerm": alternativeTerm,
            "synonyms": synonyms,
            "embeddingInput": embeddingInput,
        }

        terms.append(term)

    with open(str(PARSED_DIR / ontologyName) + ".json", "w") as f:
        json.dump(terms, f, indent=2)


def parseOntologies():
    print("Parse", len(ONTOLOGIES_LIST), "ontologies")
    for name in ONTOLOGIES_LIST:
        parseOntology(name)
    print("Finished parsing")
