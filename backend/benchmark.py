
import random
import json

from backend.algorithms import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def generate_records(size):
    records = []

    for i in range(size):
        records.append({
            "id": i + 1,
            "title": f"Task {i + 1:05d}",
            "priority": ["low", "medium", "high"][i % 3],
            "due_date": f"2026-09-{(i % 28) + 1:02d}",
            "project_id": (i % 10) + 1,
            "status": "pending"
        })

    random.shuffle(records)
    return records


def run_benchmark(size):
    records = generate_records(size)

    # Insertion sort
    insertion_records = [record.copy() for record in records]
    insertion_count = insertion_sort_count(
        insertion_records,
        "title"
    )

    # Binary search must receive an already sorted list
    binary_records = [record.copy() for record in records]
    insertion_sort_count(binary_records, "title")

    target = binary_records[-1]["title"]

    binary_result = binary_search_count(
        binary_records,
        target,
        "title"
    )

    # Linear search works on the unsorted list
    linear_target = records[-1]["title"]

    linear_result = linear_search_count(
        records,
        linear_target,
        "title"
    )

    return {
        "size": size,
        "insertion_sort_comparisons": insertion_count,
        "binary_search_comparisons": binary_result["comparison_count"],
        "linear_search_comparisons": linear_result["comparison_count"],
        "binary_search_index": binary_result["index"],
        "linear_search_index": linear_result["index"],
    }


def main():
    sizes = [10, 500, 3000]

    results = []

    for size in sizes:
        result = run_benchmark(size)
        results.append(result)

        print(f"\nDataset size: {size}")
        print(
            "Insertion sort comparisons:",
            result["insertion_sort_comparisons"]
        )
        print(
            "Binary search comparisons:",
            result["binary_search_comparisons"]
        )
        print(
            "Linear search comparisons:",
            result["linear_search_comparisons"]
        )

    with open("benchmark_results.json", "w") as file:
        json.dump(results, file, indent=4)

    print("\nRaw benchmark results saved to benchmark_results.json")


if __name__ == "__main__":
    main()