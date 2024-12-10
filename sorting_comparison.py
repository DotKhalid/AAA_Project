import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import random
import time
import csv
import matplotlib.pyplot as plt


# Sorting Algorithms
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def heuristic_merge_sort(arr, left, right):
    if left < right:
        if right - left + 1 <= 10:  # Switch to insertion sort for small arrays
            insertion_sort(arr, left, right)
            return
        mid = (left + right) // 2
        heuristic_merge_sort(arr, left, mid)
        heuristic_merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)


def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    L = arr[left:left + n1]
    R = arr[mid + 1:mid + 1 + n2]
    i = j = 0
    k = left
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# File loading function
def load_csv_data(file_path, column_index):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            try:
                value = float(row[column_index])  # Convert to float
                data.append(value)
            except ValueError:
                continue
    return data


# Run a sorting algorithm
def run_sorting_algorithm(algorithm, data):
    original = data[:]
    start_time = time.time()
    if algorithm == "Bubble Sort":
        bubble_sort(data)
    elif algorithm == "Normal Merge Sort":
        merge_sort(data)
    elif algorithm == "Heuristic Merge Sort":
        heuristic_merge_sort(data, 0, len(data) - 1)
    end_time = time.time()
    result = f"Algorithm: {algorithm}\nOriginal Array: {original[:10]}...\nSorted Array: {data[:10]}...\nTime Taken: {end_time - start_time:.6f} seconds"
    messagebox.showinfo(f"{algorithm} Result", result)


# Run sorting algorithm with UI interaction
def run_sorting_algorithm_ui(algorithm):
    choice = messagebox.askquestion("Data Source", "Use Random Data?")
    if choice == 'yes':
        size = simpledialog.askinteger("Array Size", "Enter size of random array:")
        if not size:
            return
        data = [random.randint(1, 1000) for _ in range(size)]
    else:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        column_index = simpledialog.askinteger("Column Index", "Enter column index to sort (0 for first column):")
        if column_index is None:
            return
        data = load_csv_data(file_path, column_index)
    run_sorting_algorithm(algorithm, data)


# Compare all algorithms
def compare_sorts_ui():
    choice = messagebox.askquestion("Data Source", "Use Random Data?")
    if choice == 'yes':
        sizes = [100, 500, 1000, 5000]
        data_generator = lambda size: [random.randint(1, 1000) for _ in range(size)]
    else:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        column_index = simpledialog.askinteger("Column Index", "Enter column index to sort (0 for first column):")
        if column_index is None:
            return
        data = load_csv_data(file_path, column_index)
        sizes = [len(data)]
        data_generator = lambda _: data

    results = {"Bubble Sort": [], "Normal Merge Sort": [], "Heuristic Merge Sort": []}
    merge_time = heuristic_time = 0

    for size in sizes:
        arr = data_generator(size)

        # Bubble Sort
        start_time = time.time()
        bubble_sort(arr[:])
        results["Bubble Sort"].append(time.time() - start_time)

        # Normal Merge Sort
        start_time = time.time()
        merge_sort(arr[:])
        merge_time = time.time() - start_time
        results["Normal Merge Sort"].append(merge_time)

        # Heuristic Merge Sort
        start_time = time.time()
        heuristic_merge_sort(arr[:], 0, len(arr) - 1)
        heuristic_time = time.time() - start_time
        results["Heuristic Merge Sort"].append(heuristic_time)

    # Plot results
    for sort_type, times in results.items():
        plt.plot(sizes, times, label=sort_type, marker='o')

    plt.xlabel("Array Size")
    plt.ylabel("Time (seconds)")
    plt.title("Sorting Algorithm Performance Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Show comparison message
    comparison_msg = (
        f"We implemented Normal Merge Sort, and it was awful (time: {merge_time:.6f}s), "
        f"then we added the Heuristic, and it was great! (time: {heuristic_time:.6f}s)"
    )
    messagebox.showinfo("Comparison Result", comparison_msg)


# Main UI
def create_main_ui():
    root = tk.Tk()
    root.title("Sorting Algorithm Comparison")

    label = tk.Label(root, text="Choose a Sorting Algorithm:", font=("Arial", 14))
    label.pack(pady=10)

    bubble_button = tk.Button(root, text="Run Bubble Sort", font=("Arial", 12),
                              command=lambda: run_sorting_algorithm_ui("Bubble Sort"))
    bubble_button.pack(pady=5)

    merge_button = tk.Button(root, text="Run Normal Merge Sort", font=("Arial", 12),
                             command=lambda: run_sorting_algorithm_ui("Normal Merge Sort"))
    merge_button.pack(pady=5)

    heuristic_button = tk.Button(root, text="Run Heuristic Merge Sort", font=("Arial", 12),
                                 command=lambda: run_sorting_algorithm_ui("Heuristic Merge Sort"))
    heuristic_button.pack(pady=5)

    compare_button = tk.Button(root, text="Compare All Algorithms", font=("Arial", 12), command=compare_sorts_ui)
    compare_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_main_ui()
