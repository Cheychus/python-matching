import requests


def api_search(query: str):
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
