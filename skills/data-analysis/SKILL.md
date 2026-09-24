---
name: data-analysis
description: Explore, clean, and summarize tabular data. Use when asked to analyze a CSV, spreadsheet, or dataset.
---

# Data Analysis

## Purpose

Turn a raw tabular dataset into a short, trustworthy answer: what the data contains, what's wrong with it, and what it says about the user's question. Every number reported must come from code that was actually run.

## When to use

- "Analyze this CSV", "what trends do you see?", "summarize this dataset"
- Answering a specific question from a table ("which region grew fastest?")
- Cleaning a dataset before handing it off

## When not to use

- The user wants a formatted spreadsheet as the deliverable (use a spreadsheet skill)
- Building a production data pipeline or ETL job
- Statistical modeling that needs domain review (clinical, financial risk). Flag it instead.

## Steps

1. **Clarify the question.** If the user didn't give one, profile first, then propose 2–3 questions the data can answer.
2. **Load and profile.**

   ```python
   import pandas as pd
   df = pd.read_csv("data.csv")          # or pd.read_excel(...)
   print(df.shape)
   print(df.dtypes)
   print(df.head())
   print(df.isna().sum())
   print(df.describe(include="all").T)
   ```

3. **Check quality.** Report, don't silently fix:
   - Missing values per column (count and %)
   - Duplicate rows: `df.duplicated().sum()`
   - Wrong types (numbers stored as text, dates as strings)
   - Outliers and impossible values (negative ages, future dates)
   - Inconsistent categories (`"NY"`, `"ny"`, `"New York"`)
4. **Clean with explicit, logged decisions.** Keep a list of every transformation and how many rows it affected:

   ```python
   before = len(df)
   df = df.drop_duplicates()
   log.append(f"Dropped {before - len(df)} duplicate rows")
   df["date"] = pd.to_datetime(df["date"], errors="coerce")
   ```

5. **Analyze.** Use the simplest method that answers the question: group-bys, pivots, and rates before models. Always show the denominator (e.g. "12% (48 of 400)").
6. **Visualize only when it helps.** Line charts for trends over time, bar charts for comparing categories. Label axes and units.
7. **Report** using the format below.

## Output format

```markdown
## Summary
2–3 sentences answering the question directly.

## Key findings
- Finding with number and denominator
- ...

## Data quality notes
- Issues found and how each was handled

## Method
Brief description + the code (or path to the script) so results are reproducible.
```

## Pitfalls

| Pitfall | Guard |
|---|---|
| Reporting numbers from memory | Every figure must come from executed code |
| Averaging averages | Recompute from raw rows, weighted by count |
| Dropping NaNs silently | Log how many rows were dropped and why |
| Correlation stated as cause | Say "associated with" unless there is an experiment |
| Huge file loaded whole | Use `usecols=`, `dtype=`, or `chunksize=` |

## Examples

### Example 1

**Input:** `sales.csv` with columns `date, region, units, price`. "Which region grew the most last quarter?"

**Output:**

```markdown
## Summary
The South grew most: revenue rose 18% quarter over quarter ($412K → $486K).

## Key findings
- South +18%, North +6%, West −3% (Q2 → Q3 revenue)
- South's growth came from volume (+21% units), not price (−2% avg price)

## Data quality notes
- 14 duplicate rows removed (0.3%)
- 9 rows with missing `region` excluded ($3.1K revenue)

## Method
revenue = units × price, grouped by region and quarter. Script: `analysis.py`.
```
