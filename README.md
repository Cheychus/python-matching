
# Python Matching Service

> A research prototype developed as part of my computer science bachelor's thesis. It evaluates retrieval methods for finding suitable ontology terms for real research-data field labels.

### IMPORTANT NOTE: 

This repository is only for documentation. It will not be updated and its only purpose is to archive the evaluation process from my computer science bachelor's thesis. 
If you want to use the API-Service in the Ontology-Harmonizer, use the stripped down minimal version here: [Python Matching Service API](https://github.com/Cheychus/python-matching_v2.0)

## Background and research question

Ontology mapping is often slowed down by field labels that are abbreviated, inconsistent or ambiguous. The practical question behind this project was: which search method gives a person useful ontology-term candidates for those labels?

To investigate this, I compared three approaches in the context of a planned ontology-mapping workflow:

- external terminology APIs,
- local lexical (fuzzy) search over ontology labels and synonyms
- embedding-based semantic search.

The project complements the web application [Ontology Harmonizer](https://github.com/Cheychus/ontology-harmonizer). It documents the research and evaluation work behind the retrieval component rather than presenting a finished production service.

## Approaches compared

### Terminology APIs

External terminology services provide a practical baseline: they are quick to integrate, search across a broad set of ontologies and work well for known domain terms.

Specifically I used the [TIB Terminology Service](https://terminology.tib.eu/ts) and [TS4NFDI - API Gateway](https://ts4nfdi.github.io/api-gateway/) to retrieve ontology terms via API. 

### Local lexical search

Ontology files are downloaded and searched locally using fuzzy matching over labels and synonyms. This tests how far a purely lexical approach can get with abbreviated or inconsistently named database fields.

### Embedding-based semantic search

The service creates vector representations for ontology terms and compares them with a query using cosine similarity. I evaluated 15 embedding models to test whether semantic retrieval improves results for ambiguous labels, abbreviations and specialised terminology.

## Evaluation design

The evaluation used two ground-truth sets:

- around 75 already annotated field labels extracted from a research-data ARC (Research data container)
- 34 real field labels from a plant-research database for which a domain expert could define a concrete target ontology term.

Each query had one defined target concept. The methods were compared using:

- **Hit@1, Hit@5 and Hit@10** — whether the target appears among the first result
- **Mean Reciprocal Rank (MRR)** — how early the target appears
- **runtime** — because the result should remain useful in an interactive web workflow

This is a focused experiment, not a general-purpose model benchmark. The data set is intentionally small and domain-specific.

## Key findings

- Local lexical and embedding-based search outperformed the tested terminology-API baseline on the evaluated data.
- Lexical matching achieved strong rankings but was unexpectedly slow at roughly three seconds per request in the median case, mainly because labels and synonyms must be compared extensively.
- Embedding search performed well for domain terms and showed a practical advantage for database field labels. Model choice made a noticeable difference; Qwen3 Embedding achieved the strongest overall top-k retrieval results on the evaluated plant-research labels and was selected for the optional API implementation.
- For database field labels, about half of the defined target concepts appeared in the top ten results. Many of those cases also worked lexically, but semantic search sometimes improved ranking and resolved abbreviations for which lexical matching failed.

## Results

> Note: The figures retain their original German labels because they were created for the bachelor's thesis. The short interpretations below are provided in English.

<img width="3381" height="1692" alt="vergleich_hitK_gtB" src="https://github.com/user-attachments/assets/414a889c-9176-4bcf-b9d7-d7b30e7ebd79" />

This chart compares Hit@1, Hit@5 and Hit@10 on Ground Truth B, containing the plant-research-database labels. `qwen3-embed-0.6B` achieved the strongest overall top-k results, reaching 0.50 for both Hit@5 and Hit@10. This means that the intended ontology term appeared within the first five or ten suggestions for around half of the evaluated field labels. Local lexical search remained competitive, while both terminology-API baselines returned the intended term less reliably in this experiment.   
   


<img width="3381" height="1692" alt="vergleich_mrr" src="https://github.com/user-attachments/assets/e47ca89d-1538-4e1f-ac5a-f97c451fa248" />

The MRR comparison shows that ranking quality depends on both the retrieval method and the data set. On Ground Truth B, `llama-nemotron-embed-1b-v2` placed the target term highest on average, while local lexical search performed best on Ground Truth A. The result does not identify one universally best method, but shows why the selected embedding model and the intended input data both matter.
 


<img width="3381" height="1692" alt="vergleich_median" src="https://github.com/user-attachments/assets/2927975e-5917-47e5-8ee8-9c6753c9deb9" />

This chart shows the median runtime per request. Local lexical search was the slowest approach at about 3.2 seconds because it compares a large number of ontology labels and synonyms. The embedding models ranged from 59 to 889 ms, depending on the model, while the terminology APIs responded in roughly 400–500 ms. Retrieval quality therefore needs to be balanced against response time and operational effort.



## Current API implementation

The research prototype includes a FastAPI endpoint that accepts a query and returns ranked ontology-term candidates. It can run either lexical or embedding-based search.

For embedding search, the selected model and precomputed ontology vectors are loaded when the service starts. The API returns a normalised result shape, so the Ontology Harmonizer can display candidates from this service and from a terminology API through the same mapping interface.

The integration is optional. The web prototype requests the top ten matching candidates for a field label, while the user remains responsible for choosing the semantically correct ontology term.

## Practical scope and limitations

For the current use case, running a local semantic-search service is not automatically the best production choice. It requires downloading and parsing ontologies, generating and refreshing vectors, selecting a model and operating the service. For domain users who already understand a field label, a broad terminology API is often the more pragmatic default.

Semantic search may be most useful for cryptic labels, abbreviations or multilingual data. A future version could also include context from neighbouring metadata fields or cell values to better distinguish between several plausible meanings of the same label.

## Implementation

I implemented the technical investigation independently: model research and selection, local search variants, FastAPI integration, the evaluation pipeline and analysis of the resulting trade-offs. Domain experts supported the ontology context, the ontology selection and the validation of target terms.

The main outcome was not simply a model choice. It was a reasoned product decision: keep the terminology API as the primary search option and treat local semantic retrieval as an optional enhancement for the cases where it has a practical advantage.

## Technology

- Python
- FastAPI
- Sentence Transformers
- RapidFuzz
- NumPy and cosine similarity
- Pandas for evaluation and result aggregation
