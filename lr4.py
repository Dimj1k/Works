from ortools.linear_solver import pywraplp as lin
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Combobox


class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                width=200, height=300,
                                yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = ttk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)

    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())


def __table_to_eq():
    table = [f"{c.replace(',', '.', 1)}*Eq_table[{i}]" if c != "" else f"0*Eq_table[{i}]"
             for i, c in enumerate(map(lambda x: x.get(), Eq_coeffs))]
    return eval("+".join(table))


def func_change():
    Eq.Minimize(__table_to_eq()) if min_or_max.get() == "min" else Eq.Maximize(__table_to_eq())


def __replace(string):
    if "x" not in string:
        return string
    arr = [*string.replace(" ", "")]
    flag = False
    for i, el in enumerate(arr):
        if i + 1 == len(arr) or arr[i + 1] in ("-", "+"):
            flag = False
        if el == "x" or flag:
            arr[i] = "Eq_table["
            arr[i + 1] = f"{int(arr[i + 1]) - 1}]"
            flag = True
    return "".join(arr)


def __replace2(string):
    return string if string != "=" else "=="


def __limitation():
    for limit in Limits:
        bord = [f"{c.replace(',', '.', 1)}*Eq_table[{i}]" if c != "" else f"0*Eq_table[{i}]"
                for i, c in enumerate((map(lambda x: x.get(), limit[:-2])))]
        yield eval("+".join(bord) + __replace2(limit[-2].get()) + __replace(limit[-1].get()))


def add_limitation():
    [Eq.Add(limit) for limit in __limitation()]


def write_ans():
    status = Eq.Solve()
    if status != lin.Solver.OPTIMAL:
        ans_str = "Оптимальное решение задачи не было найдено."
        ans.set(ans_str)
        return
    ans_str = "Оптимальное решение задачи было найдено"
    ans_str += f"\nЗначение функции: {Eq.Objective().Value()}\n"
    ans_str += "\n".join([f"x{i}: {x.solution_value():.6f}" for i, x in enumerate(Eq_table, start=1)])
    ans.set(ans_str)


def select_x_in(event=None):
    global a, b
    [a, b] = x_ins[x_in.get()]


def to_copy(list1, list2):
    for el in list2:
        list1.append(el)


def find_ans():
    to_copy(Eq_table, [Eq.NumVar(a, b, f"x{i}") for i in range(1, len_variables.get() + 1)])
    func_change()
    add_limitation()
    write_ans()
    Eq_table.clear()
    Eq.Clear()


def generate_first_q():
    func = ["1.1", "0.9", "2.5", "3.5", "6"]
    limits = [
        ["1.2", "1.5", "1.3", "1", "1.1", "<=", "1250000"],
        ["2", "2.5", "1.5", "1.1", "1.4", "<=", "2000000"],
        ["1", "1", "1", "1", "1", "=", "1000000"],
        ["0", "1", "0", "0", "0", "<=", "0.3 * x1"],
        ["0", "0", "1", "0", "0", "<=", "0.1 * x1"],
        ["0", "0", "0", "1", "0", "<=", "0.25 * x3"],
        ["0", "0", "0", "0", "1", "<=", "0.05 * x1"]
    ]
    for i, el in enumerate(func):
        Eq_coeffs[i].set(el)
    for i, el in enumerate(limits):
        for j, el2 in enumerate(el):
            Limits[i][j].set(el2)
    find_ans()


def change_table(len_vars, len_limits, first=False):
    global Frame_Equation
    Frame_Equation.destroy()
    Eq_coeffs.clear()
    Limits.clear()
    Frame_Equation = tk.Frame(window)
    Frame_Equation.pack()
    Frame_Eq = tk.Frame(Frame_Equation)
    Frame_Eq.pack()
    tk.Label(Frame_Eq, text="Целевая функция").pack(side=tk.TOP)
    l = range(1, len_vars.get() + 1)
    tk.Label(Frame_Eq, text="F=").pack(side=tk.LEFT, anchor=tk.S)
    for i in l:
        c = tk.StringVar()
        frame = tk.Frame(Frame_Eq)
        frame.pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text=f"x{i}").pack()
        text = tk.Entry(frame, textvariable=c, width=5)
        text.pack()
        Eq_coeffs.append(c)
    tk.Label(Frame_Eq, text="->").pack(side=tk.LEFT, anchor=tk.S)
    Combobox(Frame_Eq, values=["min", "max"], textvariable=min_or_max,
             state="readonly", width=5).pack(side=tk.LEFT, anchor=tk.S)
    k = range(1, len_limits.get() + 1)
    vals = ["<=", "=", ">="]
    frame_limits = VerticalScrolledFrame(Frame_Equation)
    frame_limits.pack()
    for i in k:
        frame_row = tk.LabelFrame(frame_limits.interior, text="", pady=3)
        frame_row.pack(side=tk.TOP)
        tk.Label(frame_row, text=f"Огр{i}: ", width=5).pack(side=tk.LEFT, anchor=tk.S)
        limit_row = []
        for j in l:
            frame_column = tk.Frame(frame_row, padx=3)
            frame_column.pack(side=tk.LEFT)
            tk.Label(frame_column, text=f"x{j}").pack()
            c = tk.StringVar()
            tk.Entry(frame_column, textvariable=c, width=5).pack()
            limit_row.append(c)
        frame_column = tk.Frame(frame_row, padx=3)
        frame_column.pack(side=tk.LEFT, anchor=tk.S)
        c = tk.StringVar(value="=")
        Combobox(frame_column, values=vals, textvariable=c, state="readonly", width=3).pack(anchor=tk.S)
        limit_row.append(c)
        c = tk.StringVar()
        frame_column = tk.Frame(frame_row, padx=3)
        frame_column.pack(side=tk.LEFT, anchor=tk.S)
        tk.Entry(frame_column, textvariable=c, width=15).pack()
        limit_row.append(c)
        Limits.append(limit_row)
    if first:
        generate_first_q()


window = tk.Tk()
window.title("Решение задач линейного программирования")
screen_width = int(window.winfo_screenwidth() // 1.5)
screen_height = int(window.winfo_screenheight() // 1.5)
window.geometry(f"{screen_width}x{screen_height}+"
                f"{int(int(screen_width) * 1.5 // 5)}+{int(int(screen_height) * 1.5 // 6)}")
Eq = lin.Solver.CreateSolver("GLOP")
a, b = 0, Eq.infinity()
min_or_max = tk.StringVar(value="max")
Eq_table = []
Eq_coeffs = []
Limits = []
Left_Frame = tk.Frame(window)
Left_Frame.pack(side=tk.LEFT, anchor=tk.N)
Frame_choose = tk.LabelFrame(Left_Frame, text="Количество переменных и условий")
Frame_choose.pack(anchor=tk.N)
Frame_vars = tk.Frame(Frame_choose)
Frame_vars.pack(anchor=tk.CENTER)
Frame_x = tk.Frame(Left_Frame)
Frame_x.pack()
tk.Label(Frame_x, text="x принадлежит").pack()
x_in = tk.StringVar(value="[0, +бск]")
x_ins = {"[0, +бск)": [0, Eq.infinity()], "(-бск, 0]": [-Eq.infinity(), 0], "R": [-Eq.infinity(), Eq.infinity()]}
cmb = Combobox(Frame_x, values=["[0, +бск)", "(-бск, 0]", "R"], state="readonly", width=10, textvariable=x_in)
cmb.pack()
cmb.bind("<<ComboboxSelected>>", select_x_in)
tk.Button(Frame_x, text="Решить задачу", command=find_ans).pack()
Frame_answer = tk.LabelFrame(Left_Frame, text="Ответ на задачу")
Frame_answer.pack()
ans = tk.StringVar()
tk.Label(Frame_answer, textvariable=ans, width=50).pack()
tk.Label(Frame_vars, text="Количество переменных").pack()
len_variables = tk.IntVar(value=5)
tk.Spinbox(Frame_vars, textvariable=len_variables, from_=1, to=15, width=15).pack()
Frame_limits = tk.Frame(Frame_choose)
Frame_limits.pack()
tk.Label(Frame_limits, text="Количество условий").pack()
len_limits = tk.IntVar(value=7)
tk.Spinbox(Frame_limits, textvariable=len_limits, from_=1, to=50, width=15).pack()
tk.Button(Frame_choose, text="Изменить сетку", command=lambda: change_table(len_variables, len_limits)).pack()
Frame_Equation = tk.Frame(window)
Frame_Equation.pack()
change_table(len_variables, len_limits, True)
window.mainloop()
