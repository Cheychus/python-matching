# Python Matching Tool

## Requirements

* Python >= 3.13
* pip

---

## Installation

Clone repository:

```bash
git clone https://github.com/Cheychus/python-matching.git
cd python-matching
```

Create virtual enviroment:

```bash
python -m venv .venv
```

Activate:

**Windows (PowerShell):**

```bash
.venv\Scripts\Activate.ps1
```

**Linux / Mac:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Optional: GPU Support (PyTorch)

Default Torch Version is CPU.

To use the GPU for calculating embeddings, install PyTorch manually:

=> https://pytorch.org/get-started/locally/

Example (CUDA):

```bash
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu126
```

---

## Start project

```bash
python main.py -d -p # 1. Download and parse all ontologies 
python main.py embeddings [0,1,2,3,4] -d cpu | gpu # Calculate embedding vectors for all ontologies with a specified model
python main.py # run main program - create search querys in main()
```

## Start API
```bash
fastapi dev api.py
```

Query: http://127.0.0.1:8000/?q=somequery.


