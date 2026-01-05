import pandas as pd

INPUT_CSV = "sports_nutrition_supplements_with_ingredients.csv"
OUTPUT_CSV = "products.csv"

df = pd.read_csv(INPUT_CSV, low_memory=False)
df.columns = [c.strip().lower() for c in df.columns]

keep_cols = ["name", "ingredients", "flavor_rating", "price"]

for col in keep_cols:
    if col not in df.columns:
        df[col] = 0 if col in ["price", "flavor_rating"] else ""


df["product_id"] = ["P%05d" % i for i in range(1, len(df)+1)]

df = df[["product_id"] + keep_cols]

df["rating"] = pd.to_numeric(df["flavor_rating"], errors="coerce").fillna(0)

df["price"] = df["price"].astype(str)
df["price_num"] = pd.to_numeric(df["price"].str.replace("$", "").str.strip(), errors="coerce").fillna(0)

def extract_goals(ing):
    ing = str(ing).lower()
    if "whey" in ing or "protein" in ing or "casein" in ing:
        return "Protein"
    if "creatine" in ing or "pre" in ing or "energy" in ing:
        return "Energy & Performance"
    if "omega" in ing or "dha" in ing or "epa" in ing or "fish oil" in ing:
        return "Heart"
    if "probiotic" in ing or "enzyme" in ing or "gut" in ing:
        return "Digestion"
    if "melatonin" in ing or "sleep" in ing or "l-theanine" in ing:
        return "Sleep"
    if "vitamin" in ing or "mineral" in ing or "zinc" in ing or "magnesium" in ing:
        return "Immunity"
    if "ashwagandha" in ing or "adaptogen" in ing or "rhodiola" in ing or "stress" in ing:
        return "Stress & Mood"
    return "General"

df["goals"] = df["ingredients"].apply(extract_goals)

goal_keywords = {
    "muscle_gain_energy": ["whey","protein","casein","gainer","mass"],
    "performance_energy": ["creatine","pre","energy"],
    "heart_immunity": ["omega","dha","epa","fish oil"],
    "digestion_focus": ["probiotic","enzyme","gut"],
    "general_immunity": ["vitamin","mineral","zinc","selenium","magnesium"],
    "sleep_support": ["melatonin","sleep","chamomile","l-theanine"],
    "stress_relief": ["ashwagandha","stress","adaptogen","rhodiola"]
}

def infer_goal(row):
    text = f"{row['name']} {row['ingredients']}".lower()
    for goal, kws in goal_keywords.items():
        if any(kw in text for kw in kws):
            return goal
    return "other"

df["wellness_goal"] = df.apply(infer_goal, axis=1)

def calc_score(row):
    ing = str(row["ingredients"]).lower()
    bonus = 0.4 if row["wellness_goal"] != "other" else 0
    if "omega" in ing: bonus += 0.3
    if "probiotic" in ing: bonus += 0.3
    if "vitamin" in ing: bonus += 0.2
    if "protein" in ing: bonus += 0.3
    if "casein" in ing: bonus += 0.25
    return max(round(row["rating"] - (row["price_num"] / 50) + bonus, 3), 0)

df["score"] = df.apply(calc_score, axis=1)

df.to_csv(OUTPUT_CSV, index=False)

print("Final columns:", df.columns.tolist())
print("Total rows:", len(df))
print(df.head(3))
