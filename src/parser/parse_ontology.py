from owlready2 import *
from config import ONTOLOGIES_LIST, RAW_DIR, PARSED_DIR
import json
from tqdm import tqdm

SYNONYM_PROPERTIES = [
    "skos_prefLabel",
    "skos_altLabel",
    "skos_hiddenLabel",
    "oboInOwl_hasExactSynonym",
    "oboInOwl_hasRelatedSynonym",
    "oboInOwl_hasBroadSynonym",
    "oboInOwl_hasNarrowSynonym",
    "oboInOwl_hasSynonym",
    "IAO_0000118",
]

DEFINITION_PROPERTIES = ["IAO_0000115", "IAO_0000600"]


def parse(ontology: str):
    onto: Ontology = get_ontology(str(RAW_DIR / ontology) + ".owl").load()
    syn_props = SYNONYM_PROPERTIES.copy()

    # extract additional individual synonyms like BrAPI synonym, MIAPPE synonym...
    for prop in onto.annotation_properties():
        if "synonym" in prop.name.lower():
            syn_props.append(prop.name)

    # relevant ontology values
    classes = list(onto.classes())
    data_properties = list(onto.data_properties())
    object_properties = list(onto.object_properties())
    individuals = list(onto.individuals())

    ontologies = classes + data_properties + object_properties + individuals

    terms = []

    for cls in ontologies:
        label = cls.label.first()
        if not label:  # skip ontologies without label
            continue
        # print("CLASS: ", str(cls), cls.IAO_0000115)
        definition = set()
        for prop in DEFINITION_PROPERTIES:
            if hasattr(cls, prop):
                for d in getattr(cls, prop):
                    definition.add(str(d))

        synonyms = set()
        for prop in syn_props:
            try:
                values = getattr(cls, prop, [])
            except:
                print("[WARNING]: ", prop, label, cls)
                continue
            for v in values:
                synonyms.add(str(v))

        embedding_input = label
        # if len(definition) > 0:
        #     embedding_input += " ".join(definition)
        if len(synonyms) > 0:
            embedding_input += " " + " ".join(synonyms)

        term = {
            "id": cls.iri,
            "short_id": cls.name,
            "type": "class",
            "label": label,
            "definition": list(definition),
            "synonyms": list(synonyms),
            "embedding_input": embedding_input,
        }
        terms.append(term)
    with open(str(PARSED_DIR / ontology) + ".json", "w") as f:
        json.dump(terms, f, indent=2)


def parse_ontologies():
    print("Parse", len(ONTOLOGIES_LIST), "ontologies")

    start_total = time.perf_counter()
    for name in tqdm(ONTOLOGIES_LIST, desc="Parsing ontologies"):
        tqdm.write(f"Parse {name}...")
        start = time.perf_counter()
        parse(name)
        elapsed = time.perf_counter() - start
        tqdm.write(f"{name} parsed in {elapsed:.2f}s")

    total = time.perf_counter() - start_total
    print(f"[PARSER]: Finished parsing ({total:.2f}s total)")
