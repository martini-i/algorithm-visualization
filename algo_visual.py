import tkinter as tk
from tkinter import messagebox
import random
import time
import matplotlib.pyplot as plt


# Bubble Sort
# Best for sorting small arrays
# Time complexity: O(n^2)
def bubble_sort(arr):
    start = time.perf_counter()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    # time.perf_counter() returns time in seconds * 1e6 to convert to microseconds
    # time.time() can also be used but it has lower resolution
    return (time.perf_counter() - start) * 1e6

# Merge Sort
# Best for sorting large arrays
# Time complexity: O(n log n)
def merge_sort(arr):
    start = time.perf_counter()
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return (time.perf_counter() - start) * 1e6

# Counting Sort (For Radix Sort)
# Helper function for LSD/MSD Radix Sort
def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]

# LSD Radix Sort
# Best for sorting integers with a fixed number of digits
# Time complexity: O(n * k) where k = number of digits in the largest number
def lsd_radix_sort(arr):
    start = time.perf_counter()
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return (time.perf_counter() - start) * 1e6

# MSD Radix Sort
# Best for sorting integers with varying number of digits
# Time complexity: O(n * k) where k = number of digits in the largest number
def msd_radix_sort(arr):
    start = time.perf_counter()
    # Helper function for MSD Radix Sort
    def msd_radix_helper(arr, digit_place):
        if len(arr) <= 1 or digit_place < 0:
            return arr

        # Create 10 buckets for 0-9
        buckets = [[] for _ in range(10)]

        for num in arr:
            digit = (num // 10 ** digit_place) % 10
            buckets[digit].append(num)

        sorted_arr = []
        for bucket in buckets:
            sorted_arr.extend(msd_radix_helper(bucket, digit_place - 1))

        return sorted_arr

    max_num = max(arr)
    max_digits = len(str(max_num))
    msd_radix_helper(arr, max_digits - 1)
    return (time.perf_counter() - start) * 1e6

# Quick Sort
# Best for sorting large arrays
# Time complexity: O(n log n)
def quick_sort(arr):
    start = time.perf_counter()
    # Helper function for Quick Sort
    def quick_sort_helper(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot] # Elements less than the pivot
        middle = [x for x in arr if x == pivot] # Elements equal to the pivot
        right = [x for x in arr if x > pivot] # Elements greater than the pivot
        return quick_sort_helper(left) + middle + quick_sort_helper(right) # Recursively sort left and right halves

    sorted_arr = quick_sort_helper(arr)
    arr[:] = sorted_arr

    return (time.perf_counter() - start) * 1e6

# Linear Search
# Finds single element in an array
# Time complexity: O(n)
def linear_search(arr, target):
    start = time.perf_counter()
    for i in range(len(arr)):
        if arr[i] == target:
            return (time.perf_counter() - start) * 1e6

# Function to generate array
def generate_array():
    try:
        size = int(array_size_entry.get())
        if size <= 0:
            raise ValueError
        global arr
        arr = [random.randint(1, 9999) for _ in range(size)]
        array_display.config(text=str(arr))
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive integer for array size.")

# Run selected algorithms
def run_algorithms():
    global arr
    times = {}
    selected_algorithms = [alg for alg, var in algorithm_vars.items() if var.get() == 1]
    # Check if at least one algorithm is selected
    if not selected_algorithms:
        messagebox.showerror("Error", "Please select at least one algorithm.")
        return
    # Copy the array to avoid modifying the original array
    for algorithm in selected_algorithms:
        arr_copy = arr[:]
        if algorithm == "Bubble Sort":
            times[algorithm] = bubble_sort(arr_copy)
        elif algorithm == "Merge Sort":
            times[algorithm] = merge_sort(arr_copy)
        elif algorithm == "Quick Sort":
            times[algorithm] = quick_sort(arr_copy)
        elif algorithm == "Radix Sort (LSD)":
            times[algorithm] = lsd_radix_sort(arr_copy)
        elif algorithm == "Radix Sort (MSD)":
            times[algorithm] = msd_radix_sort(arr_copy)
        elif algorithm == "Linear Search":
            target = target_value.get()
            # Check if target value is a valid integer, else display an error message
            if not target.isdigit():
                messagebox.showerror("Error", "Please enter a valid target value.")
                return
            times[algorithm] = linear_search(arr_copy, int(target))
    print(times)
    # Check if all algorithms returned valid execution times, else display an error message
    if any(not isinstance(time, (int, float)) for time in times.values()):
        messagebox.showerror("Error", "One of the algorithms did not return a valid execution time.")
        return

    display_chart(times)


# Display graph of execution times
def display_chart(times):
    algorithms = list(times.keys())
    execution_times = list(times.values())

    # Create a bar chart with animation
    fig, ax = plt.subplots(figsize=(10, 5))

    # Generates random colors for each bar for better contrast
    colors = [(random.random(), random.random(), random.random()) for _ in algorithms]

    ax.bar(algorithms, execution_times, color=colors)
    # Axes labels and title
    ax.set_xlabel("Algorithms")
    ax.set_ylabel("Execution Time (microseconds)")
    ax.set_title("Execution Time of Sorting Algorithms")
    ax.set_ylim(0, max(execution_times) * 1.1)

    plt.show()


# Toggle target input for linear search
def toggle_target_input():
    if algorithm_vars["Linear Search"].get():
        target_entry.config(state=tk.NORMAL)
    else:
        target_entry.config(state=tk.DISABLED)
        target_value.set("")


# Tkinter GUI setup
root = tk.Tk()
# Title
root.title("Sorting Algorithm Visualization")
root.geometry("500x500")

# Label asking for array size
array_size_label = tk.Label(root, text="Array Size:")
array_size_label.pack()

# Entry field for array size
array_size_entry = tk.Entry(root)
array_size_entry.pack()

# Button to generate array
generate_button = tk.Button(root, text="Generate Array", command=generate_array)
generate_button.pack()

target_value = tk.StringVar()

# Label asking for target value
target_label = tk.Label(root, text="Target Value for Linear Search:")
target_label.pack()

# Entry field for target value, disabled until linear search is selected
target_entry = tk.Entry(root, textvariable=target_value, state=tk.DISABLED)
target_entry.pack()

array_display = tk.Label(root, text="Generated array will appear here", wraplength=400) # Display generated array
array_display.pack()

# Dictionary to store the algorithm names and their respective Tkinter IntVar objects
algorithm_vars = {
    "Bubble Sort": tk.IntVar(),
    "Merge Sort": tk.IntVar(),
    "Quick Sort": tk.IntVar(),
    "Radix Sort (LSD)": tk.IntVar(),
    "Radix Sort (MSD)": tk.IntVar(),
    "Linear Search": tk.IntVar()
}
# Create a Checkbutton for each algorithm
for algorithm, var in algorithm_vars.items():
    chk = tk.Checkbutton(root, text=algorithm, variable=var,
                         command=toggle_target_input if algorithm == "Linear Search" else None)
    chk.pack()

# Button to run the selected algorithms
run_button = tk.Button(root, text="Run Algorithms", command=run_algorithms)
run_button.pack()

root.mainloop()