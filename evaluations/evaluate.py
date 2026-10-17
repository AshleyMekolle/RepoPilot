
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "issues.json"
PREDICTIONS_PATH = BASE_DIR / "predictions.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate(dataset, predictions):
    predictions_by_id = {item["id"]: item for item in predictions}

    total = len(dataset)
    category_correct = 0
    priority_correct = 0
    both_correct = 0
    missing = []
    errors = []

    for issue in dataset:
        prediction = predictions_by_id.get(issue["id"])

        if prediction is None:
            missing.append(issue["id"])
            continue

        category_ok = (
            prediction.get("predicted_category")
            == issue["expected_category"]
        )
        priority_ok = (
            prediction.get("predicted_priority")
            == issue["expected_priority"]
        )

        category_correct += category_ok
        priority_correct += priority_ok
        both_correct += category_ok and priority_ok

        if not category_ok or not priority_ok:
            errors.append({
                "id": issue["id"],
                "title": issue["title"],
                "expected_category": issue["expected_category"],
                "predicted_category": prediction.get("predicted_category"),
                "expected_priority": issue["expected_priority"],
                "predicted_priority": prediction.get("predicted_priority"),
            })

    evaluated = total - len(missing)

    return {
        "total": total,
        "evaluated": evaluated,
        "missing_predictions": missing,
        "category_accuracy": round(category_correct / evaluated * 100, 2) if evaluated else 0,
        "priority_accuracy": round(priority_correct / evaluated * 100, 2) if evaluated else 0,
        "both_correct": round(both_correct / evaluated * 100, 2) if evaluated else 0,
        "errors": errors,
    }


if __name__ == "__main__":
    dataset = load_json(DATASET_PATH)
    predictions = load_json(PREDICTIONS_PATH)
    results = evaluate(dataset, predictions)

    print(f"Dataset size: {results['total']}")
    print(f"Issues evaluated: {results['evaluated']}/{results['total']}")
    print(f"Missing predictions: {results['missing_predictions']}")
    print(f"Category accuracy: {results['category_accuracy']}%")
    print(f"Priority accuracy: {results['priority_accuracy']}%")
    print(f"Both correct: {results['both_correct']}%")

    if results["evaluated"] < results["total"]:
        print("\nWARNING: Results are preliminary; some issues have no predictions.")

    print("\nIncorrect predictions:")
    for error in results["errors"]:
        print(json.dumps(error, indent=2))
