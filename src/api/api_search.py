import requests


def transform_result(iri: str, label: str, descriptions, short_form: str):
    return {
        "iri": iri,
        "label": label,
        "descriptions": descriptions,
        "short_form": short_form,
    }


def get_url(api, query, collection=True):
    if api == "terminology":
        return f"https://terminology.services.base4nfdi.de/api-gateway/search?query={query}{'&collectionId=ca19cfb6-c15e-48d9-bde8-c631031f0035' if collection else ''}"
    elif api == "tib":
        return f"https://api.terminology.tib.eu/api/v2/entities?search={query}&page=0&size=20&lang=en&exclusive=true&facetFields=type+ontologyId{'&schema=collection&classification=DataPLANT' if collection else ''}&option=COMPOSITE"


def api_search(query: str, api="terminology", collection=True):
    url = get_url(api, query, collection)
    response = requests.get(url)

    if not response.status_code == 200:
        print(f"Error: {response.status_code}")
        return

    data = response.json()
    if api == "terminology":
        return [
            transform_result(d["iri"], d["label"], d["descriptions"], d["short_form"])
            for d in data
        ]
    elif api == "tib":
        return [
            transform_result(
                d["iri"], d["label"][0], getattr(d, "definition", []), d["curie"]
            )
            for d in data["elements"]
        ]


def api_search_terminology(query: str):
    url = f"https://terminology.services.base4nfdi.de/api-gateway/search?query={query}&collectionId=ca19cfb6-c15e-48d9-bde8-c631031f0035"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        result = [
            {
                "iri": d["iri"],
                "label": d["label"],
                "descriptions": d["descriptions"],
                "short_form": d["short_form"],
            }
            for d in data
        ]
        return result
    else:
        print(f"Error: {response.status_code}")


def api_search_tib(query: str):
    url = f"https://api.terminology.tib.eu/api/v2/entities?search={query}&page=0&size=10&lang=en&exclusive=true&facetFields=type+ontologyId&schema=collection&classification=DataPLANT&option=COMPOSITE"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        results = data["elements"]
        result = [
            {
                "iri": d["iri"],
                "label": d["label"][0],
                "descriptions": getattr(d, "definition", []),
                "short_form": d["curie"],
            }
            for d in results
        ]
        return result
    else:
        print(f"Error: {response.status_code}")
