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

## Installation & Run

### Clone repository
```bash
git clone <repo_link>
cd Data2Dialogue
