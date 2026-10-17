# RepoPilot AI Evaluation

How accurately does RepoPilot's AI triage classify GitHub issues? This evaluation measures it against a labelled test set instead of relying on a few manual spot checks.

## Objective

Measure how often RepoPilot's issue triage (RP-02) assigns the correct **category** (`bug`, `feature`, `documentation`, `needs-review`) and **priority** (`high`, `medium`, `low`) when compared with labels set by a human.

## Dataset

[`issues.json`](issues.json) contains 20 realistic GitHub issues. Each one has a title, a body, and the expected category and priority. The set deliberately includes:

- Clear-cut bugs, feature requests and documentation fixes
- High-priority cases: security risks, data loss and outages
- Vague or ambiguous reports that should be classified `needs-review`

## Method

| Setting | Value |
|---|---|
| Model | `openai/gpt-oss-120b` on Groq |
| Prompt | Same system prompt as RP-02 Issue Triage |
| Temperature | 0, for repeatable results |
| Output | JSON mode: category, priority, labels and reason |
| Scoring | Exact match after normalizing case and whitespace |

**Pipeline**

1. The n8n workflow [`RepoPilot_AI_Evaluation.json`](RepoPilot_AI_Evaluation.json) loads `issues.json` from this repo.
2. Each issue is classified one at a time, with a 20-second pause between calls to stay within Groq's free-tier rate limits.
3. Predictions are paired with the expected labels and exported to [`predictions.json`](predictions.json).
4. Accuracy is calculated in the workflow and independently by [`evaluate.py`](evaluate.py), so the two can be cross-checked.

## Results

| Metric | Score |
|---|---|
| Issues evaluated | RESULT / 20 |
| Category accuracy | RESULT% |
| Priority accuracy | RESULT% |
| Category and priority both correct | RESULT% |

### Misclassified issues

ERRORS_TABLE

## Findings

FINDINGS

## Limitations

- **Small dataset:** 20 issues gives a useful signal, but each issue moves accuracy by 5 percentage points.
- **One labeller:** the expected labels reflect one person's judgment. Borderline priorities, such as medium versus high, are partly subjective.
- **Exact match only:** a prediction one priority level away counts as fully wrong.

## Next steps

- Grow the dataset to 50+ issues, with more borderline cases
- Compare other models and prompt versions against this baseline
- Re-run the evaluation after every prompt change to catch regressions
