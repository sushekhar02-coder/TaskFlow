
from backend.algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def check(condition, message):
    if condition:
        print(f"PASS: {message}")
    else:
        print(f"FAIL: {message}")


def main():

    # =========================
    # INSERTION SORT
    # =========================

    records = []
    insertion_sort(records, "title")
    check(
        records == [],
        "insertion_sort empty list"
    )

    records = [{"title": "Task A"}]
    insertion_sort(records, "title")
    check(
        records == [{"title": "Task A"}],
        "insertion_sort single element"
    )

    records = [
        {"title": "Task B"},
        {"title": "Task A"},
    ]
    insertion_sort(records, "title")
    check(
        records == [
            {"title": "Task A"},
            {"title": "Task B"},
        ],
        "insertion_sort sorts correctly"
    )


    # =========================
    # BINARY SEARCH
    # =========================

    values = [
        {"title": "Task A"},
        {"title": "Task B"},
        {"title": "Task C"},
        {"title": "Task D"},
        {"title": "Task E"},
    ]

    check(
        binary_search(values, "Task C", "title") == 2,
        "binary_search finds existing value"
    )

    check(
        binary_search(values, "Task Z", "title") == -1,
        "binary_search missing value"
    )


    # =========================
    # LINEAR SEARCH
    # =========================

    check(
        linear_search(values, "Task C", "title") == 2,
        "linear_search finds existing value"
    )

    check(
        linear_search(values, "Task Z", "title") == -1,
        "linear_search missing value"
    )


    # =========================
    # INSERTION SORT COUNT
    # =========================

    records = [
        {"title": "Task B"},
        {"title": "Task A"},
    ]

    insertion_count = insertion_sort_count(records, "title")

    check(
        insertion_count > 0,
        "insertion_sort comparison count"
    )


    # =========================
    # BINARY SEARCH COUNT
    # =========================

    binary_result = binary_search_count(
        values,
        "Task C",
        "title"
    )

    check(
        binary_result["index"] == 2,
        "binary_search_count finds value"
    )

    check(
        binary_result["comparison_count"] > 0,
        "binary_search comparison count"
    )


    # =========================
    # LINEAR SEARCH COUNT
    # =========================

    linear_result = linear_search_count(
        values,
        "Task C",
        "title"
    )

    check(
        linear_result["index"] == 2,
        "linear_search_count finds value"
    )

    check(
        linear_result["comparison_count"] > 0,
        "linear_search comparison count"
    )


if __name__ == "__main__":
    main()