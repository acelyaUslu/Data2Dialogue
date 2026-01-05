import streamlit as st
import pandas as pd
import json
import requests

API_KEY = "Api-key"  
st.set_page_config(page_title="Supplement Recommender", layout="centered")
st.title("LLM-Powered Supplement Recommendation Demo")

@st.cache_data
def load_data():
    df = pd.read_csv("products.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    return df

df = load_data()

df["price_num"] = pd.to_numeric(
    df["price"].astype(str).str.replace("$", "").str.strip(),
    errors="coerce"
).fillna(0)

st.subheader("Choose your goal")
goal = st.selectbox("Select wellness goal:", sorted(df["wellness_goal"].unique().tolist()))

st.subheader("Budget filter")
max_price = st.number_input("Max price ($)", min_value=0.0, value=50.0, step=1.0)


def call_llm(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)

    if r.status_code != 200:
        raise RuntimeError(r.text)

    return r.json()["choices"][0]["message"]["content"]

if st.button("Generate LLM Recommendations"):

    d = df[(df["wellness_goal"] == goal) & (df["price_num"] <= max_price)].copy()

    if d.empty:
        st.warning("No products match this goal and budget.")
        st.stop()

    candidates = d.sort_values("score", ascending=False).head(10)

    list_text = "\n".join(
        [f"{r['product_id']} | {r['name']} | ${r['price_num']:.2f} | {str(r['ingredients'])[:120]}"
         for _, r in candidates.iterrows()]
    )

    prompt = f"""
You are a recommendation engine.

User wellness goal: {goal}
Maximum budget: ${max_price}

CANDIDATES (choose ONLY from this list):
{list_text}

Rules:
- Choose exactly 3 products from the list above.
- Do not invent new names.
- Return as JSON array (3 objects).
- Each object must include: product_id, name, price, reason (max 2 sentences).
- Return ONLY JSON.
"""

    try:
        answer = call_llm(prompt)
        raw = answer.strip()

        
        start = raw.find("[")
        end = raw.rfind("]")
        if start != -1 and end != -1:
            raw = raw[start:end+1]

        # JSON parse
        recs = json.loads(raw)

        st.success("Top 3 Recommended Supplements:")
        st.table(pd.DataFrame(recs[:3]))

    except Exception as e:
        st.error("LLM call failed: " + str(e))

st.subheader("Chat-based Supplement Assistant")

if user_input := st.chat_input("Write your wellness goal and budget (example: muscle_gain_energy 40)"):
    st.chat_message("user").write(user_input)

    # --- Goal ve bütçe çıkar ---
    text = user_input.lower()
    import re
    nums = re.findall(r"\d+", text)
    budget = float(nums[0]) if nums else max_price  # UI budget fallback

    inferred = None
    for g in df["wellness_goal"].unique():
        if g in text:
            inferred = g
            break
    if not inferred:
        inferred = goal  # UI goal fallback

    # --- Adayları hazırla ---
    cands = df[(df["wellness_goal"] == inferred) & (df["price_num"] <= budget)]
    top10 = cands.sort_values("score", ascending=False).head(10)

    if top10.empty:
        st.chat_message("assistant").write("No supplements match your request.")
        st.stop()

    cand_text = "\n".join(
        [f"{r['product_id']} | {r['name']} | ${r['price_num']:.2f}" for _, r in top10.iterrows()]
    )

    llm_prompt = f"""
You are a supplement sales agent chatbot.
Goal: {inferred}
Budget: ${budget}

Candidates (choose ONLY from this list):
{cand_text}

Rules:
- Pick exactly 3 products from the list.
- Do not invent new names.
- Return ONLY JSON array with 3 objects: product_id, name, price, reason.
"""

    try:
        answer = call_llm(llm_prompt)
        recs = json.loads(answer)
        st.chat_message("assistant").write("Here are your top 3 supplements:")
        st.table(pd.DataFrame(recs))
    except:
        st.chat_message("assistant").write("LLM could not generate recommendations.")
