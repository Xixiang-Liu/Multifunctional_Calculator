import matplotlib.pyplot as plt
import os.path as osp
from typing import List
import numpy as np

# visualization.py is never used directly
# so this path is relative to user_interface.py
temp_dir_path = "resources/temp"


# interpret the input (a string) into a list of numbers
# return None if the input has an error
def interpret(s: str) -> List:
    current = ""
    allow_minus = True
    allow_dot = True
    result = []
    for char in s:
        if char == "-" and allow_minus:
            allow_minus = False
            current += char
        elif char == "." and allow_dot:
            allow_dot = False
            current += char
        elif char == " ":
            allow_minus = allow_dot = True
            if len(current) > 0:
                current_num = float(current)
                current = ""
                result.append(current_num)
        elif "0" <= char <= "9":
            current += char
            allow_minus = False
        else:
            result = None
            break
    return result


# find the first available serial number for this type of graph
def find_serial(prefix: str) -> int:
    serial = 0
    img_name = f"{prefix}_{serial}.png"
    img_path = osp.join(temp_dir_path, img_name)
    while osp.exists(img_path):
        serial += 1
        img_name = f"{prefix}_{serial}.png"
        img_path = osp.join(temp_dir_path, img_name)
    return serial


# draw a boxplot based on the input, and store it
def draw_boxplot(nums: List, serial: int):
    global temp_dir_path
    graph_name = f"boxplot_{serial}.png"
    graph_path = osp.join(temp_dir_path, graph_name)

    fig, ax = plt.subplots()
    ax.set_title('Boxplot')
    ax.boxplot(nums, vert=False, whis=0.75)

    plt.savefig(graph_path)


# draw a histogram based on the input, and store it
def draw_histogram(nums: List, serial: int):
    global temp_dir_path
    graph_name = f"histogram_{serial}.png"
    graph_path = osp.join(temp_dir_path, graph_name)

    fig, ax = plt.subplots()
    ax.set_title('Histogram')
    if len(nums) < 21:
        n_bins = 10
    else:
        n_bins = 20
    ax.hist(nums, bins=n_bins)

    plt.savefig(graph_path)


# draw a stem and leaf plot based on the input, and store it
def draw_stem_and_leaf_plot(nums: List, serial: int):
    global temp_dir_path
    graph_name = f"stem_and_leaf_plot_{serial}.png"
    graph_path = osp.join(temp_dir_path, graph_name)

    fig, ax = plt.subplots()
    ax.set_title('Stem and Leaf Plot')
    ys = nums
    xs = []
    for y in ys:
        s = str(y)
        if s[0] != "-":
            xs.append(int(s[0]))
        else:
            xs.append(-int(s[1]))
    ax.stem(xs, ys)

    plt.savefig(graph_path)


# draw a scatter plot based on the input, and store it
def draw_scatter_plot(x_data: List, y_data: List, serial: int) -> None:
    global temp_dir_path
    graph_name = f"scatter_plot_{serial}.png"
    graph_path = osp.join(temp_dir_path, graph_name)

    fig, ax = plt.subplots()
    ax.scatter(x_data, y_data)

    plt.savefig(graph_path)


# draw a line graph based on the input, and store it
def draw_line_chart(x_data: List, y_data: List, serial: int) -> None:
    global temp_dir_path
    graph_name = f"line_chart_{serial}.png"
    graph_path = osp.join(temp_dir_path, graph_name)

    fig, ax = plt.subplots()
    ax.plot(x_data, y_data)

    plt.savefig(graph_path)


# draw a line graph based on the input, and store it
def draw_linear_regression(x_data: List, y_data: List, serial: int) -> None:
    global temp_dir_path
    graph_name = f"linear_regression_{serial}.png"
    graph_path = osp.join(temp_dir_path, graph_name)

    fig, ax = plt.subplots()
    coef = np.polyfit(x_data, y_data, 1)
    # create a function that takes in x and return the predicted value of y
    pred_func = np.poly1d(coef)
    ax.plot(x_data, y_data, "yo", x_data, pred_func(x_data), "--k")

    plt.savefig(graph_path)
