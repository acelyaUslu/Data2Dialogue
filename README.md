# Data2Dialogue – LLM-Grounded Supplement Recommendation Prototype

This project is an academic prototype that implements the **Data2Dialogue pipeline** by grounding structured supplement product knowledge into an OpenAI LLM agent for personalized, wellness-goal-aligned, and budget-aware supplement recommendations.

The prototype workflow includes:
- Building a local enterprise-like supplement knowledge base from a public Kaggle dataset (CSV)
- Semantic wellness-goal inference from ingredient descriptions
- Candidate filtering based on a user-defined maximum budget
- Lightweight ranking using a custom scoring function
- Top-3 supplement selection performed by **OpenAI `gpt-4o-mini`** (strictly constrained to pick from provided candidates)
- Result visualization through an interactive **Streamlit UI**

> ⚠️ This prototype is for **academic demonstration only** and does **not provide medical advice**.

---

## Pipeline Summary

The system follows this unified pipeline:

1. Load supplement data from `sports_nutrition_supplements_with_ingredients.csv`
2. Normalize column names for stability (`strip()` + `lower()`)
3. Convert price values to numeric (`price_num`) for budget filtering
4. Infer wellness goals semantically from ingredient text using keyword mapping
5. Rank candidates using a lightweight scoring function (flavor rating + semantic bonuses)
6. Send top-10 ranked candidates to the OpenAI LLM agent
7. LLM selects exactly **3 products from the candidate list** (no hallucination, no new names)
8. Parse JSON output and display results in Streamlit table

---

## Dataset

- **Source:** Public Kaggle supplement dataset (used as a substitute enterprise knowledge base with instructor approval)
- **Content:** Product names, ingredient descriptions, flavor ratings, and price details
- **Purpose:** Structured knowledge grounding and reproducible candidate filtering/ranking

---

## Tech Stack

| Component | Tool / Library |
|---|---|
| Language | Python |
| Data Processing | pandas |
| LLM Agent | OpenAI `gpt-4o-mini` (REST API, `requests.post`) |
| UI | Streamlit |
| Knowledge Base | Local CSV grounding (`products.csv`) |

---

## 🚀 Installation & Run

### 1. Clone repository
```bash
git clone <repo_link>
cd Data2Dialogue
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key
Edit `app.py` and update:
```python
API_KEY = "your_api_key_here"
```

### 4. Run the prototype UI
```bash
streamlit run app.py  # Launch the interface
```

---

##  File Structure
```
📁 Data2Dialogue
│
├── sports_nutrition_supplements_with_ingredients.csv  # Original knowledge source
├── products.csv                                      # Generated local knowledge base
├── app.py                                           # Streamlit UI + LLM logic
├── requirements.txt                                  # Project dependencies
└── README.md                                        # Documentation
```

---

## 🤖 LLM Output Constraints
The OpenAI agent is instructed to:
- Pick **exactly 3 products**
- Select **only from the candidate list provided**
- **Never generate new product names**
- Return results **only in JSON array format**

### Example valid model output:
```json
[
  {"product_id": "P00034", "name": "whey isolate", "price": 27.99, "reason": "Supports muscle gain and protein goals."},
  {"product_id": "P00112", "name": "omega 3 fish oil", "price": 19.50, "reason": "Promotes heart health and immunity."},
  {"product_id": "P00256", "name": "probiotic complex", "price": 32.00, "reason": "Provides digestion support."}
]
```

---

## ✍️ Author 
**Açelya Uslu**  
MSc Computer Engineering  
Manisa Celal Bayar University, Türkiye

