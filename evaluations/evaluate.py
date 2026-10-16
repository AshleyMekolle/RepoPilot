
import json
from pathlib import Path


DATASET_PATH = Path(__file__).parent / "issues.json"


def load_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate(dataset):
    total = len(dataset)

    category_correct = 0
    priority_correct = 0
    both_correct = 0
    errors = []

    for issue in dataset:
        # Predictions will be filled in by the next integration step.
        predicted_category = issue.get("predicted_category")
        predicted_priority = issue.get("predicted_priority")

        category_ok = predicted_category == issue["expected_category"]
        priority_ok = predicted_priority == issue["expected_priority"]

        category_correct += category_ok
        priority_correct += priority_ok
        both_correct += category_ok and priority_ok

        if not category_ok or not priority_ok:
            errors.append({
                "id": issue["id"],
                "title": issue["title"],
                "expected_category": issue["expected_category"],
                "predicted_category": predicted_category,
                "expected_priority": issue["expected_priority"],
                "predicted_priority": predicted_priority,
            })

    return {
        "total": total,
        "category_accuracy": round(category_correct / total * 100, 2) if total else 0,
        "priority_accuracy": round(priority_correct / total * 100, 2) if total else 0,
        "both_correct": round(both_correct / total * 100, 2) if total else 0,
        "errors": errors,
    }


if __name__ == "__main__":
    dataset = load_dataset()
    results = evaluate(dataset)

    print(f"Total issues: {results['total']}")
    print(f"Category accuracy: {results['category_accuracy']}%")
    print(f"Priority accuracy: {results['priority_accuracy']}%")
    print(f"Both correct: {results['both_correct']}%")
    print("\nIncorrect predictions:")

    for error in results["errors"]:
        print(json.dumps(error, indent=2))
