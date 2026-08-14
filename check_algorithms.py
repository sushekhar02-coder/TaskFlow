
from algorithms import (
    insertion_sort,
    binary_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count
)

def check(case_name, result, expected):
    if result == expected:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected {expected}, got {result}")


records = []
insertion_sort(records, "title")
check("insertion sort empty list", records, [])


records = [{"title": "Task A"}]
insertion_sort(records, "title")
check("insertion sort single element", records, [{"title": "Task A"}])


records = [
    {"title": "Alpha"},
    {"title": "Beta"},
    {"title": "Gamma"},
    {"title": "Delta"},
    {"title": "Epsilon"}
]

check("binary search first index", binary_search(records, "Alpha", "title"), 0)
check("binary search middle index", binary_search(records, "Gamma", "title"), 2)
check("binary search last index", binary_search(records, "Epsilon", "title"), 4)
check("binary search absent value", binary_search(records, "Omega", "title"), -1)


records = [
    {"title": "Charlie"},
    {"title": "Alpha"},
    {"title": "Bravo"}
]

result = insertion_sort_count(records, "title")

if records == [
    {"title": "Alpha"},
    {"title": "Bravo"},
    {"title": "Charlie"}
] and type(result) == int and result > 0:
    print("PASS: insertion sort count")
else:
    print(f"FAIL: insertion sort count — list {records}, count {result}")


records = [
    {"title": "Alpha"},
    {"title": "Bravo"},
    {"title": "Charlie"},
    {"title": "Delta"},
    {"title": "Echo"}
]

result = binary_search_count(records, "Charlie", "title")

if (
    type(result) == dict
    and result["index"] == 2
    and type(result["comparison_count"]) == int
    and result["comparison_count"] > 0
):
    print("PASS: binary search count")
else:
    print(f"FAIL: binary search count — got {result}")


records = [
    {"title": "Alpha"},
    {"title": "Bravo"},
    {"title": "Charlie"},
    {"title": "Delta"}
]

result = linear_search_count(records, "Omega", "title")

if (
    type(result) == dict
    and result["index"] == -1
    and result["comparison_count"] == len(records)
):
    print("PASS: linear search count")
else:
    print(f"FAIL: linear search count — got {result}")