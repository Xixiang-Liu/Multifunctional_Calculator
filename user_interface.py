from tkinter import *
from tkinter import scrolledtext
from backend import basic_arithmetic, other_bases, visualization
from decimal import Decimal
from PIL import ImageTk, Image
import os
import os.path as osp

temp_dir_path = "resources/temp"
statistics_dir_path = "resources/statistics"
help_dir_path = "resources/help"

# the user can choose different styles with different colors
# the default style is blue
blue_colors = {"background": "dimgrey",
               "light_1": "lightsteelblue",
               "light_2": "dodgerblue",
               "deep_1": "slateblue",
               "deep_2": "blue",
               "highlight": "red"}

red_colors = {"background": "dimgrey",
              "light_1": "mistyrose",
              "light_2": "tomato",
              "deep_1": "firebrick",
              "deep_2": "red",
              "highlight": "darkred"}

black_colors = {"background": "dimgrey",
                "light_1": "gainsboro",
                "light_2": "silver",
                "deep_1": "darkgrey",
                "deep_2": "black",
                "highlight": "darkred"}

green_colors = {"background": "dimgrey",
                "light_1": "palegreen",
                "light_2": "yellowgreen",
                "deep_1": "limegreen",
                "deep_2": "forestgreen",
                "highlight": "red"}

style = blue_colors


# initialize root window
root = Tk()
root.title("Multifunctional Calculator")
root.configure(bg="dimgrey")

# set up the input entry
e = Entry(root, width=62, borderwidth=5)
e.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


# set up buttons for numbers and operators which can be directly added to the expression
def click_to_add(char: str):
    current = e.get()
    e.delete(0, END)
    e.insert(0, current + char)


button_1 = Button(root, text="1", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("1"))
button_2 = Button(root, text="2", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("2"))
button_3 = Button(root, text="3", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("3"))
button_4 = Button(root, text="4", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("4"))
button_5 = Button(root, text="5", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("5"))
button_6 = Button(root, text="6", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("6"))
button_7 = Button(root, text="7", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("7"))
button_8 = Button(root, text="8", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("8"))
button_9 = Button(root, text="9", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("9"))
button_0 = Button(root, text="0", padx=40, pady=20, bg="lightsteelblue", command=lambda: click_to_add("0"))
button_add = Button(root, text="+", padx=39, pady=20, bg="slateblue", fg="white", command=lambda: click_to_add("+"))
button_subtract = Button(root, text="-", padx=40, pady=20,
                         bg="slateblue", fg="white", command=lambda: click_to_add("-"))
button_multiply = Button(root, text="*", padx=40, pady=20,
                         bg="slateblue", fg="white", command=lambda: click_to_add("*"))
button_divided_by = Button(root, text="/", padx=40, pady=20,
                           bg="slateblue", fg="white", command=lambda: click_to_add("/"))
button_left_bracket = Button(root, text="(", padx=41, pady=20,
                             bg="dodgerblue", fg="white", command=lambda: click_to_add("("))
button_right_bracket = Button(root, text=")", padx=41, pady=20,
                              bg="dodgerblue", fg="white", command=lambda: click_to_add(")"))
button_power = Button(root, text="^", padx=39, pady=20, bg="slateblue", fg="white", command=lambda: click_to_add("^"))
button_sqrt = Button(root, text="√", padx=39, pady=20, bg="slateblue", fg="white", command=lambda: click_to_add("√"))
button_dot = Button(root, text=".", padx=41, pady=20, bg="lightsteelblue", command=lambda: click_to_add("."))
button_pi = Button(root, text="π", padx=39, pady=20, bg="lightsteelblue", command=lambda: click_to_add("π"))
button_mod = Button(root, text="%", padx=38, pady=20, bg="slateblue", fg="white", command=lambda: click_to_add("%"))

button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)
button_0.grid(row=4, column=0)
button_left_bracket.grid(row=6, column=0)
button_right_bracket.grid(row=6, column=1)
button_add.grid(row=2, column=3)
button_subtract.grid(row=3, column=3)
button_multiply.grid(row=4, column=3)
button_divided_by.grid(row=5, column=3)
button_power.grid(row=5, column=0)
button_sqrt.grid(row=5, column=1)
button_dot.grid(row=4, column=1)
button_pi.grid(row=4, column=2)
button_mod.grid(row=5, column=2)


# set up buttons operators which change the expression once clicked
def button_clear():
    e.delete(0, END)


def button_equal() -> None:
    expression = e.get()
    global first_equal
    if first_equal:
        output_window.delete(1.0, END)
        first_equal = False
    output_window.insert(INSERT, expression)

    expression, changed, can_proceed = basic_arithmetic.standardize_and_check_error(expression)
    # if unchanged, no need to print again
    if not changed:
        output_window.insert(INSERT, f"\n(Input is standard)")
    else:
        # print the standardized version
        if can_proceed:
            output_window.insert(INSERT, f"\n(Standardized to {expression})")
        # meet an error, can not go on
        else:
            output_window.insert(INSERT, f"\n{expression}\nTo check what this means, please clik HELP")
            output_window.insert(INSERT, "\n" + "\n")
            return

    finished = False
    while not finished:
        expression, finished = basic_arithmetic.interpret(expression)
        output_window.insert(INSERT, f"\n= {expression}")

    output_window.insert(INSERT, "\n" + "\n")


first_equal = True
button_clear = Button(root, text="C", padx=39, pady=20, command=button_clear, bg="blue", fg="white")
button_equal = Button(root, text="=", padx=39, pady=20, command=button_equal, bg="blue", fg="white")

button_clear.grid(row=6, column=2)
button_equal.grid(row=6, column=3)


# set up the backspace button
def backspace() -> None:
    current = e.get()
    if current == "":
        return
    e.delete(0, END)
    new = current[: len(current) - 1]
    e.insert(INSERT, new)


button_backspace = Button(root, text="⌫", padx=32, pady=20, font="BOLD",
                          bg="blue", fg="white", command=backspace)
button_backspace.grid(row=1, column=3)


# set up the clear output button
def clear_output() -> None:
    output_window.delete(1.0, END)
    output_window.insert(INSERT, "Here will display the calculation step by step.")
    global first_equal
    first_equal = True


button_clear_output = Button(root, text="CLEAR", padx=27, pady=26, font="BOLD",
                             bg="Red", fg="white", command=clear_output)
button_clear_output.grid(row=0, column=9)


# set up the help button
def display_help() -> None:
    # set up the help window
    global pic
    global pic_label
    global current_page_num
    help_win = Toplevel()
    help_win.title("Help")
    help_win.configure(bg=style["background"])
    help_win.geometry("500x740")

    # grap all the help information in images in the help folder
    imgs = os.listdir(help_dir_path)
    pic_label = Label(help_win)
    pic_label.grid(row=0, column=0, columnspan=3)

    # elements in the 0th row
    pic_path = osp.join(help_dir_path, imgs[0])
    pic = Image.open(pic_path).resize((500, 705))
    pic = ImageTk.PhotoImage(pic)
    pic_label.config(image=pic)

    def backward() -> None:
        global pic
        global pic_label
        global current_page_num

        # if at the 1st page, can't move backward
        if current_page_num == 1:
            return

        # update the picture and the pos label
        current_page_num -= 1
        pos.config(text=f"{current_page_num}/{len(imgs)}")
        pic_path = osp.join(help_dir_path, imgs[current_page_num - 1])
        pic = Image.open(pic_path).resize((500, 705))
        pic = ImageTk.PhotoImage(pic)
        pic_label.config(image=pic)

    def forward() -> None:
        global pic
        global pic_label
        global current_page_num

        # if at the last page, can't move forward
        if current_page_num == len(imgs):
            return

        # update the picture and the pos label
        current_page_num += 1
        pos.config(text=f"{current_page_num}/{len(imgs)}")
        pic_path = osp.join(help_dir_path, imgs[current_page_num - 1])
        pic = Image.open(pic_path).resize((500, 705))
        pic = ImageTk.PhotoImage(pic)
        pic_label.config(image=pic)

    # elements in the 1st row
    current_page_num = 1
    backward_button = Button(help_win, text="◁", fg="white", bg=style["deep_1"],
                             font="BOLD", command=backward)
    pos = Label(help_win, text=f"1/{len(imgs)}", font="BOLD")
    forward_button = Button(help_win, text="▷", fg="white", bg=style["deep_1"],
                            font="BOLD", command=forward)
    backward_button.grid(row=1, column=0)
    pos.grid(row=1, column=1)
    forward_button.grid(row=1, column=2)


button_help = Button(root, text="HELP", padx=31, pady=53, font="BOLD",
                     bg=style["light_1"], command=display_help)
button_help.grid(row=1, column=9, rowspan=2)

# set up the output multi line window with a scrollbar
output_window = scrolledtext.ScrolledText(root, wrap=WORD, width=50, borderwidth=5, height=37)
output_window.grid(row=0, column=4, columnspan=5, rowspan=7)
output_window.insert(INSERT, "Here will display the calculation step by step.")


# set up the other functionalities button
def open_other_func() -> None:
    global button_other_func
    global drop_func
    global button_confirm_func
    global var

    button_other_func.destroy()

    # create a drop-down menu for other functions
    options = [
        "cancel",
        "Other\nbases",
        "Statistics"
    ]
    var.set("Select:")
    drop_func = OptionMenu(root, var, *options)
    drop_func.grid(row=3, column=9)

    # confirm the selection
    button_confirm_func = Button(root, text="Confirm", command=do_other_func)
    button_confirm_func.grid(row=4, column=9)


# selected another functionality, do it
def do_other_func():
    global button_other_func
    global drop_func
    global button_confirm_func

    drop_func.destroy()
    button_confirm_func.destroy()
    button_other_func = Button(root, text="Other\nFunctions", padx=11, pady=50, font="BOLD",
                               bg=style["deep_2"], fg="white", command=open_other_func)
    button_other_func.grid(row=3, column=9, rowspan=2)

    func = var.get()
    if func == "Other\nbases":
        other_bases_window()
    elif func == "Statistics":
        statistics_window()


def statistics_window():
    # initialize the statistics window
    stat_window = Toplevel()
    stat_window.title("Statistics")
    stat_window.configure(bg=style["background"])

    global statistics_dir_path
    global graph
    global graph_label
    graph_name = "Output_Sample.png"
    graph_path = osp.join(statistics_dir_path, graph_name)
    graph = Image.open(graph_path).resize((400, 300))
    graph = ImageTk.PhotoImage(graph)
    graph_label = Label(stat_window, image=graph)
    graph_label.grid(row=0, column=0, columnspan=4)

    # elements in row 1
    description = Label(stat_window, anchor=W, font="BOLD", fg="white", relief=SUNKEN, padx=10,
                        bg=style["light_2"], text="Please enter each term with your keyboard")
    description.grid(row=1, column=0, columnspan=4, sticky="ew")

    # elements in row 2
    operation_one_label = Label(stat_window, anchor=W, font="BOLD", fg="white", relief=SUNKEN, padx=10,
                                bg=style["deep_1"], text="Operation 1: plot with one-dimensional data")
    operation_one_label.grid(row=2, column=0, columnspan=4, sticky="ew")

    # elements in row 3
    operation_one_instruction = Label(stat_window, anchor=W, font="BOLD", fg="white", bg=style["background"],
                                      text="Enter data with space as the delimiter:")
    operation_one_instruction.grid(row=3, column=0, columnspan=4, sticky="w")

    # elements in row 4
    operation_one_entry = Entry(stat_window, width=50)
    operation_one_entry.grid(row=4, column=0, columnspan=4, sticky="e")

    def draw_with_one_dimensional_data() -> None:
        global statistics_dir_path
        global img
        global graph_label
        global temp_graphs
        global graph_menu
        global choose_button
        global g3

        typed = operation_one_entry.get()
        data = visualization.interpret(typed)

        # This means there is some problem in the input
        if data is None:
            img_name = "Invalid_Input.png"
            img_path = osp.join(statistics_dir_path, img_name)
            img = Image.open(img_path).resize((400, 300))
            img = ImageTk.PhotoImage(img)
            graph_label = Label(stat_window, image=img)
            graph_label.grid(row=0, column=0, columnspan=4)
            return

        # no problem, then identify graph type and draw, display
        operation_one_entry.delete(0, END)
        graph_type = graph_1.get()
        # create the graph in the temp directory
        if graph_type == "Boxplot":
            serial = visualization.find_serial("boxplot")
            visualization.draw_boxplot(data, serial)
            img_name = f"boxplot_{serial}.png"
        elif graph_type == "Histogram":
            serial = visualization.find_serial("histogram")
            visualization.draw_histogram(data, serial)
            img_name = f"histogram_{serial}.png"
        else:
            serial = visualization.find_serial("stem_and_leaf_plot")
            visualization.draw_stem_and_leaf_plot(data, serial)
            img_name = f"stem_and_leaf_plot_{serial}.png"

        # display it
        img_path = osp.join(temp_dir_path, img_name)
        img = Image.open(img_path).resize((400, 300))
        img = ImageTk.PhotoImage(img)
        graph_label = Label(stat_window, image=img)
        graph_label.grid(row=0, column=0, columnspan=4)

        # update the dropdown menu for graphs in Operation 3
        graph_menu.destroy()
        temp_graphs = os.listdir(temp_dir_path)
        g3 = StringVar()
        g3.set(temp_graphs[0])
        graph_menu = OptionMenu(stat_window, g3, *temp_graphs)
        choose_button = Button(stat_window, text="draw", bg=style["light_1"],
                               command=show_graph)
        graph_menu.grid(row=12, column=0, columnspan=3, sticky="w")
        choose_button.grid(row=12, column=3, sticky="e")

    # elements in row 5
    operation_one_options = [
        "Boxplot",
        "Histogram",
        "Stem and Leaf Plot (Whole Numbers)"
    ]
    graph_1 = StringVar()
    graph_1.set(operation_one_options[0])
    operation_one_menu = OptionMenu(stat_window, graph_1, *operation_one_options)
    operation_one_draw_button = Button(stat_window, bg=style["light_1"], text="draw",
                                       command=draw_with_one_dimensional_data)
    operation_one_menu.grid(row=5, column=0, columnspan=2, sticky="w")
    operation_one_draw_button.grid(row=5, column=3, sticky="e")

    # elements in row 6
    operation_two_label = Label(stat_window, anchor=W, font="BOLD", fg="white", relief=SUNKEN, padx=10,
                                bg=style["deep_1"], text="Operation 2: plot with two-dimensional data")
    operation_two_label.grid(row=6, column=0, columnspan=4, sticky="ew")

    # elements in row 7
    operation_two_instruction = Label(stat_window, anchor=W, font="BOLD", fg="white", bg=style["background"],
                                      text="Enter data with space as the delimiter:")
    operation_two_instruction.grid(row=7, column=0, columnspan=4, sticky="w")

    # elements in row 8
    operation_two_x_label = Label(stat_window, anchor=W, font="BOLD", fg="white", bg=style["background"],
                                  text="X Entry: ")
    operation_two_x_entry = Entry(stat_window, width=50)
    operation_two_x_label.grid(row=8, column=0, sticky="w")
    operation_two_x_entry.grid(row=8, column=1, columnspan=3, sticky="e")

    # elements in row 9
    operation_two_y_label = Label(stat_window, anchor=W, font="BOLD", fg="white", bg=style["background"],
                                  text="Y Entry: ")
    operation_two_y_entry = Entry(stat_window, width=50)
    operation_two_y_label.grid(row=9, column=0, sticky="w")
    operation_two_y_entry.grid(row=9, column=1, columnspan=3, sticky="e")

    def draw_with_two_dimensional_data() -> None:
        global statistics_dir_path
        global img
        global graph_label
        global temp_graphs
        global graph_menu
        global choose_button
        global g3

        x_input = operation_two_x_entry.get()
        y_input = operation_two_y_entry.get()
        x_data = visualization.interpret(x_input)
        y_data = visualization.interpret(y_input)

        # This means there is some problem in the input
        if x_data is None or y_data is None or len(x_data) != len(y_data):
            img_name = "Invalid_Input.png"
            img_path = osp.join(statistics_dir_path, img_name)
            img = Image.open(img_path).resize((400, 300))
            img = ImageTk.PhotoImage(img)
            graph_label = Label(stat_window, image=img)
            graph_label.grid(row=0, column=0, columnspan=4)
            return

        # no problem, then identify graph type and draw, display
        operation_two_x_entry.delete(0, END)
        operation_two_y_entry.delete(0, END)
        graph_type = graph_2.get()
        # create the graph in the temp directory
        if graph_type == "Scatter Plot":
            serial = visualization.find_serial("scatter_plot")
            visualization.draw_scatter_plot(x_data, y_data, serial)
            img_name = f"scatter_plot_{serial}.png"
        elif graph_type == "Line Chart":
            serial = visualization.find_serial("line_chart")
            visualization.draw_line_chart(x_data, y_data, serial)
            img_name = f"line_chart_{serial}.png"
        else:
            serial = visualization.find_serial("linear_regression")
            visualization.draw_linear_regression(x_data, y_data, serial)
            img_name = f"linear_regression_{serial}.png"

        # display it
        img_path = osp.join(temp_dir_path, img_name)
        img = Image.open(img_path).resize((400, 300))
        img = ImageTk.PhotoImage(img)
        graph_label = Label(stat_window, image=img)
        graph_label.grid(row=0, column=0, columnspan=4)

        # update the dropdown menu for graphs in Operation 3
        graph_menu.destroy()
        temp_graphs = os.listdir(temp_dir_path)
        g3 = StringVar()
        g3.set(temp_graphs[0])
        graph_menu = OptionMenu(stat_window, g3, *temp_graphs)
        choose_button = Button(stat_window, text="draw", bg=style["light_1"],
                               command=show_graph)
        graph_menu.grid(row=12, column=0, columnspan=3, sticky="w")
        choose_button.grid(row=12, column=3, sticky="e")

    # elements in row 10
    operation_two_options = [
        "Scatter Plot",
        "Line Chart",
        "Linear Regression"
    ]
    graph_2 = StringVar()
    graph_2.set(operation_two_options[0])
    operation_two_menu = OptionMenu(stat_window, graph_2, *operation_two_options)
    operation_two_draw_button = Button(stat_window, bg=style["light_1"], text="draw",
                                       command=draw_with_two_dimensional_data)
    operation_two_menu.grid(row=10, column=0, columnspan=2, sticky="w")
    operation_two_draw_button.grid(row=10, column=3, sticky="e")

    # elements in row 11
    operation_three_label = Label(stat_window, anchor=W, font="BOLD", fg="white", relief=SUNKEN, padx=10,
                                  bg=style["deep_1"], text="Operation 3: show drawn graphs")
    operation_three_label.grid(row=11, column=0, columnspan=4, sticky="ew")

    def show_graph() -> None:
        global img
        global graph_label
        global g3
        img_name = g3.get()
        # If we have no stored image, just do nothing
        if img_name == "There exists no stored graph!":
            return
        # else we display the chosen stored image
        img_path = osp.join(temp_dir_path, img_name)
        img = Image.open(img_path).resize((400, 300))
        img = ImageTk.PhotoImage(img)
        graph_label = Label(stat_window, image=img)
        graph_label.grid(row=0, column=0, columnspan=4)

    # elements in row 12
    global g3
    global temp_dir_path
    global temp_graphs
    global graph_menu
    global choose_button
    temp_graphs = os.listdir(temp_dir_path)
    if not temp_graphs:
        temp_graphs.append("There exists no stored graph!")
    g3 = StringVar()
    g3.set(temp_graphs[0])
    graph_menu = OptionMenu(stat_window, g3, *temp_graphs)
    choose_button = Button(stat_window, text="draw", bg=style["light_1"],
                           command=show_graph)
    graph_menu.grid(row=12, column=0, columnspan=3, sticky="w")
    choose_button.grid(row=12, column=3, sticky="e")

    # elements in row 13
    operation_four_label = Label(stat_window, anchor=W, font="BOLD", fg="white", relief=SUNKEN, padx=10,
                                 bg=style["deep_1"], text="Operation 4: clear all drawn graphs")
    operation_four_label.grid(row=13, column=0, columnspan=4, sticky="ew")

    def clear_graph() -> None:
        # clear all the files in the temp directory
        global temp_dir_path
        files = os.listdir(temp_dir_path)
        for file in files:
            file_path = osp.join(temp_dir_path, file)
            os.remove(file_path)

        # update the dropdown menu of Operation 3
        global g3
        global temp_graphs
        global graph_menu
        temp_graphs = ["There exists no stored graph!"]
        g3.set(temp_graphs[0])
        graph_menu.destroy()
        graph_menu = OptionMenu(stat_window, g3, *temp_graphs)
        graph_menu.grid(row=12, column=0, columnspan=3, sticky="w")

    # elements in row 14
    clear_button = Button(stat_window, text="CLEAR", bg=style["highlight"], fg="white", font="BOLD",
                          command=clear_graph)
    clear_button.grid(row=14, column=2, columnspan=2, sticky="e")


def other_bases_window():
    # initialize the other_bases window
    new_window = Toplevel()
    new_window.title("Calculations for other bases")
    new_window.configure(bg="dimgrey")

    # elements in row 0
    description = Label(new_window, anchor=W, font="BOLD", fg="white", pady=30, relief=SUNKEN, padx=10,
                        bg=style["light_2"], text="Please enter each term with your keyboard")
    output = scrolledtext.ScrolledText(new_window, wrap=WORD, width=30, borderwidth=3, height=20)
    description.grid(row=0, column=0, rowspan=2, columnspan=4, sticky="ew")
    output.grid(row=0, column=4, columnspan=5, rowspan=10)
    output.insert(INSERT, "Here will display the calculation.")
    global began_calculation_other_bases
    began_calculation_other_bases = False

    # elements in row 2
    operation_one_label = Label(new_window, anchor=W, font="BOLD", fg="white", relief=SUNKEN, padx=10,
                                bg=style["deep_1"], text="Operation 1: Base Conversion")
    operation_one_label.grid(row=2, column=0, columnspan=4, sticky="ew")

    # elements in row 3
    original_num_label = Label(new_window, anchor=W, font="BOLD", fg="white",
                               bg=style["background"], text="Num_1")
    original_base_label = Label(new_window, anchor=W, font="BOLD", fg="white",
                                bg=style["background"], text="From Base")
    new_base_label = Label(new_window, anchor=W, font="BOLD", fg="white",
                           bg=style["background"], text="To Base")
    original_num_label.grid(row=3, column=0, sticky="w")
    original_base_label.grid(row=3, column=1, sticky="w")
    new_base_label.grid(row=3, column=2, sticky="w")

    # elements in row 4
    original_num_entry = Entry(new_window, width=12)
    original_base_entry = Entry(new_window, width=5)
    new_base_entry = Entry(new_window, width=5)
    original_num_entry.grid(row=4, column=0, sticky="w")
    original_base_entry.grid(row=4, column=1, sticky="w")
    new_base_entry.grid(row=4, column=2, sticky="w")

    # execute when clicking the convert button
    def convert():
        # eliminate the placeholder if doing calculation at the first time
        global began_calculation_other_bases
        if not began_calculation_other_bases:
            output.delete(1.0, END)
            began_calculation_other_bases = True

        # grab the inputs from the entries, and output them
        num = original_num_entry.get()
        original_base = int(original_base_entry.get())
        new_base = int(new_base_entry.get())
        output.insert(INSERT, f"{num} in base {original_base}\n")

        # clear the entries
        original_num_entry.delete(0, END)
        original_base_entry.delete(0, END)
        new_base_entry.delete(0, END)

        # produce and output result
        input_correct = other_bases.check(num, original_base)
        if input_correct:
            result = other_bases.convert(num, original_base, new_base)
            output.insert(INSERT, f"= {result} in base {new_base}\n" + "\n")
        else:
            output.insert(INSERT, "Invalid Input\n" + "\n")

    # elements in row 5
    convert_button = Button(new_window, text="Convert", bg=style["light_1"], command=convert)
    convert_button.grid(row=5, column=3, sticky="ew")

    # elements in row 6
    operation_two_label = Label(new_window, anchor=W, font="BOLD", fg="white", relief=SUNKEN, padx=10,
                                bg=style["deep_1"], text="Operation 2: Arithmetic in An Arbitrary Base:")
    operation_two_label.grid(row=6, column=0, columnspan=4, sticky="ew")

    # elements in row 7
    num_1_label = Label(new_window, anchor=W, font="BOLD", fg="white",
                        bg=style["background"], text="Num_1")
    operators_label = Label(new_window, anchor=W, font="BOLD", fg="white",
                            bg=style["background"], text="Operator")
    num_2_label = Label(new_window, anchor=W, font="BOLD", fg="white",
                        bg=style["background"], text="Num_2")
    in_base_label = Label(new_window, anchor=W, font="BOLD", fg="white",
                          bg=style["background"], text="In Base")
    num_1_label.grid(row=7, column=0, sticky="w")
    operators_label.grid(row=7, column=1, sticky="w")
    num_2_label.grid(row=7, column=2, sticky="w")
    in_base_label.grid(row=7, column=3, sticky="w")

    # elements in row 8
    num_1_entry = Entry(new_window, width=12)
    operators = ["+", "-", "*", "/"]
    op = StringVar()
    op.set(operators[0])
    op_menu = OptionMenu(new_window, op, *operators)
    num_2_entry = Entry(new_window, width=12)
    in_base_entry = Entry(new_window, width=5)
    num_1_entry.grid(row=8, column=0, sticky="w")
    op_menu.grid(row=8, column=1, sticky="w")
    num_2_entry.grid(row=8, column=2, sticky="w")
    in_base_entry.grid(row=8, column=3, sticky="w")

    # execute when click the calculate button
    def arithmetic():
        # eliminate the placeholder if doing calculation at the first time
        global began_calculation_other_bases
        if not began_calculation_other_bases:
            output.delete(1.0, END)
            began_calculation_other_bases = True

        # grab the inputs and check, and output them
        num_1 = num_1_entry.get()
        base = int(in_base_entry.get())
        if not other_bases.check(num_1, base):
            output.insert(INSERT, "Invalid Num_1\n" + "\n")
            return
        operator = op.get()
        num_2 = num_2_entry.get()
        if not other_bases.check(num_2, base):
            output.insert(INSERT, "Invalid Num_2\n" + "\n")
            return
        output.insert(INSERT, f"{num_1}{operator}{num_2} in base {base}\n")

        # clear the entries
        num_1_entry.delete(0, END)
        in_base_entry.delete(0, END)
        op.set("+")
        num_2_entry.delete(0, END)

        # do the calculation and output result
        if operator == "+":
            result = other_bases.plus(num_1, num_2, base)
        elif operator == "-":
            result = other_bases.minus(num_1, num_2, base)
        elif operator == "*":
            result = other_bases.multiply(num_1, num_2, base)
        else:
            num_2_base_ten = other_bases.convert(num_2, base, 10)
            if Decimal(num_2_base_ten) == 0:
                output.insert(INSERT, "Num_2 cannot be 0\n" + "\n")
                return
            result = other_bases.divided_by(num_1, num_2, base)
        output.insert(INSERT, f"= {result} in base {base}\n" + "\n")

    # elements in row 9
    button_calculate = Button(new_window, text="Calculate", bg=style["light_1"], command=arithmetic)
    button_calculate.grid(row=9, column=3, sticky="ew")


button_other_func = Button(root, text="Other\nFunctions", padx=11, pady=50, font="BOLD",
                           bg=style["deep_2"], fg="white", command=open_other_func)
button_other_func.grid(row=3, column=9, rowspan=2)
# These variables will be built in def open_other_func()
s = StringVar()
drop_func, button_confirm_func, var = OptionMenu(root, s, ""), Button(), StringVar()
began_calculation_other_bases = False


# set up the settings button
def settings() -> None:
    global button_style
    global color_menu
    global button_confirm_color

    # destroy the setting button and show options
    button_style.destroy()
    colors = ["Blue",
              "Red",
              "Black",
              "Green"]
    c = StringVar()
    c.set(colors[0])
    color_menu = OptionMenu(root, c, *colors)
    button_confirm_color = Button(root, text="Confirm",
                                  command=lambda: change_style(c.get()))
    color_menu.grid(row=5, column=9)
    button_confirm_color.grid(row=6, column=9)


# changed the style options, change color here
def change_style(color: str) -> None:
    global style
    global button_style
    global color_menu
    global button_confirm_color

    # set the style
    if color == "Blue":
        style = blue_colors
    elif color == "Black":
        style = black_colors
    elif color == "Red":
        style = red_colors
    elif color == "Green":
        style = green_colors

    # restore the style button
    color_menu.destroy()
    button_confirm_color.destroy()
    button_style = Button(root, text="Style", padx=27, pady=53, font="BOLD",
                          bg=style["deep_2"], fg="white", command=settings)
    button_style.grid(row=5, column=9, rowspan=2)

    # change color for each element
    root.config(bg=style["background"])
    button_1.config(bg=style["light_1"])
    button_2.config(bg=style["light_1"])
    button_3.config(bg=style["light_1"])
    button_4.config(bg=style["light_1"])
    button_5.config(bg=style["light_1"])
    button_6.config(bg=style["light_1"])
    button_7.config(bg=style["light_1"])
    button_8.config(bg=style["light_1"])
    button_9.config(bg=style["light_1"])
    button_0.config(bg=style["light_1"])
    button_add.config(bg=style["deep_1"])
    button_subtract.config(bg=style["deep_1"])
    button_multiply.config(bg=style["deep_1"])
    button_divided_by.config(bg=style["deep_1"])
    button_left_bracket.config(bg=style["light_2"])
    button_right_bracket.config(bg=style["light_2"])
    button_power.config(bg=style["deep_1"])
    button_sqrt.config(bg=style["deep_1"])
    button_dot.config(bg=style["light_1"])
    button_pi.config(bg=style["light_1"])
    button_mod.config(bg=style["deep_1"])
    button_clear.config(bg=style["deep_2"])
    button_equal.config(bg=style["deep_2"])
    button_backspace.config(bg=style["deep_2"])
    button_clear_output.config(bg=style["highlight"])
    button_help.config(bg=style["light_1"])
    button_other_func.config(bg=style["deep_2"])
    button_style.config(bg=style["deep_2"])


button_style = Button(root, text="Style", padx=27, pady=53, font="BOLD",
                      bg="blue", fg="white", command=settings)
button_style.grid(row=5, column=9, rowspan=2)

# keep my app running
root.mainloop()
