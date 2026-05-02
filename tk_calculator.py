import tkinter as tk
import math


def calculate(op):
    err_label.config(text="")
    try:
        a = float(entry_a.get().strip())

        # Unary operations (square, square root) only need one input
        if op in ("x²", "√x"):
            if op == "x²":
                res = a * a
                expr_label.config(text=f"({fmt(a)})²", fg=MUTED)
                op_label.config(text="SQUARED", fg=OP_COLORS[op])
            else:  # √x
                if a < 0:
                    err_label.config(text="Cannot take square root of a negative number.")
                    return
                res = math.sqrt(a)
                expr_label.config(text=f"√({fmt(a)})", fg=MUTED)
                op_label.config(text="SQUARE ROOT", fg=OP_COLORS[op])

            result_val_label.config(text=fmt(res), fg=OP_COLORS[op])
            result_frame.pack(fill=tk.X, padx=40, pady=(0, 8))
            return

        # Binary operations need both inputs
        b = float(entry_b.get().strip())

        if op == "/" and b == 0:
            err_label.config(text="Cannot divide by zero.")
            return

        ops = {"+": a + b, "-": a - b, "*": a * b, "/": a / b}
        res = ops[op]

        symbols = {"+": "plus", "-": "minus", "*": "times", "/": "divided by"}
        expr_label.config(text=f"{fmt(a)}  {op}  {fmt(b)}", fg=MUTED)
        result_val_label.config(text=fmt(res), fg=OP_COLORS[op])
        op_label.config(text=symbols[op].upper(), fg=OP_COLORS[op])
        result_frame.pack(fill=tk.X, padx=40, pady=(0, 8))

    except ValueError:
        err_label.config(text="Enter valid numeric values.")


def fmt(n):
    return str(int(n)) if n == int(n) else f"{n:,.6g}"


def clear_all():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    err_label.config(text="")
    result_frame.pack_forget()


BG       = "#f9f9f7"
FG       = "#1a1a18"
MUTED    = "#888780"
BORDER   = "#d1d1cc"
ENTRY_BG = "#f0f0ec"
MONO     = "Courier New"
SERIF    = "Georgia"

OP_COLORS = {
    "+":  "#185FA5",   # blue
    "-":  "#993556",   # pink
    "*":  "#3B6D11",   # green
    "/":  "#854F0B",   # amber
    "x²": "#5A3A8A",   # purple
    "√x": "#1A7A6E",   # teal
}

root = tk.Tk()
root.title("tk_calculator.py")
root.geometry("480x680")
root.resizable(False, False)
root.configure(bg=BG)

tk.Label(root, text="Calculator", font=(SERIF, 32, "bold"),
         bg=BG, fg=FG, anchor="w").pack(fill=tk.X, padx=40, pady=(32, 0))
tk.Label(root, text="ARITHMETIC OPERATIONS", font=(MONO, 8),
         bg=BG, fg=MUTED, anchor="w").pack(fill=tk.X, padx=40, pady=(2, 28))

# --- Input fields ---
inputs_frame = tk.Frame(root, bg=BG)
inputs_frame.pack(fill=tk.X, padx=40)
inputs_frame.columnconfigure(0, weight=1)
inputs_frame.columnconfigure(1, weight=1)

tk.Label(inputs_frame, text="FIRST NUMBER", font=(MONO, 8),
         bg=BG, fg=MUTED, anchor="w").grid(row=0, column=0, sticky="w",
                                            pady=(0, 4), padx=(0, 8))
entry_a = tk.Entry(inputs_frame, font=(MONO, 20), bd=0,
                   bg=ENTRY_BG, fg=FG, insertbackground=FG,
                   relief=tk.FLAT, width=10)
entry_a.grid(row=1, column=0, sticky="ew", ipady=12, padx=(0, 8))

tk.Label(inputs_frame, text="SECOND NUMBER", font=(MONO, 8),
         bg=BG, fg=MUTED, anchor="w").grid(row=0, column=1, sticky="w",
                                             pady=(0, 4))
entry_b = tk.Entry(inputs_frame, font=(MONO, 20), bd=0,
                   bg=ENTRY_BG, fg=FG, insertbackground=FG,
                   relief=tk.FLAT, width=10)
entry_b.grid(row=1, column=1, sticky="ew", ipady=12)

tk.Label(root, text="(Second number not used for x² and √x)", font=(MONO, 7),
         bg=BG, fg=MUTED, anchor="w").pack(fill=tk.X, padx=40, pady=(4, 0))

err_label = tk.Label(root, text="", font=(MONO, 8), bg=BG, fg="#E24B4A")
err_label.pack(anchor="w", padx=40, pady=(4, 0))

# --- Binary operation buttons ---
tk.Label(root, text="OPERATION", font=(MONO, 8),
         bg=BG, fg=MUTED, anchor="w").pack(fill=tk.X, padx=40, pady=(18, 6))

ops_frame = tk.Frame(root, bg=BG)
ops_frame.pack(fill=tk.X, padx=40)

binary_ops = [
    ("+", "ADD"),
    ("-", "SUBTRACT"),
    ("*", "MULTIPLY"),
    ("/", "DIVIDE"),
]

for i, (sym, label) in enumerate(binary_ops):
    color = OP_COLORS[sym]
    ops_frame.columnconfigure(i, weight=1)
    btn_frame = tk.Frame(ops_frame, bg=color)
    btn_frame.grid(row=0, column=i, sticky="ew",
                   padx=(0, 6) if i < 3 else 0)
    tk.Button(
        btn_frame, text=f"{sym}\n{label}",
        font=(MONO, 9, "bold"),
        bg=color, fg=BG,
        activebackground=color, activeforeground=BG,
        relief=tk.FLAT, bd=0,
        pady=14, cursor="hand2",
        command=lambda s=sym: calculate(s)
    ).pack(fill=tk.X)

# --- Unary operation buttons (square & square root) ---
tk.Label(root, text="UNARY OPERATION  (uses first number only)", font=(MONO, 8),
         bg=BG, fg=MUTED, anchor="w").pack(fill=tk.X, padx=40, pady=(16, 6))

unary_frame = tk.Frame(root, bg=BG)
unary_frame.pack(fill=tk.X, padx=40)

unary_ops = [
    ("x²", "SQUARE"),
    ("√x", "SQRT"),
]

for i, (sym, label) in enumerate(unary_ops):
    color = OP_COLORS[sym]
    unary_frame.columnconfigure(i, weight=1)
    btn_frame = tk.Frame(unary_frame, bg=color)
    btn_frame.grid(row=0, column=i, sticky="ew",
                   padx=(0, 6) if i == 0 else 0)
    tk.Button(
        btn_frame, text=f"{sym}\n{label}",
        font=(MONO, 9, "bold"),
        bg=color, fg=BG,
        activebackground=color, activeforeground=BG,
        relief=tk.FLAT, bd=0,
        pady=14, cursor="hand2",
        command=lambda s=sym: calculate(s)
    ).pack(fill=tk.X)

# --- Clear button ---
tk.Button(root, text="CLEAR", font=(MONO, 8),
          bg=BG, fg=MUTED, activebackground=BG, activeforeground=FG,
          relief=tk.FLAT, bd=0, pady=6, cursor="hand2",
          command=clear_all).pack(pady=(10, 0))

tk.Frame(root, height=1, bg=BORDER).pack(fill=tk.X, padx=40, pady=(14, 0))

# --- Result display ---
result_frame = tk.Frame(root, bg=BG)

expr_label = tk.Label(result_frame, text="", font=(MONO, 10),
                      bg=BG, fg=MUTED, anchor="w")
expr_label.pack(fill=tk.X, padx=40, pady=(20, 2))

op_label = tk.Label(result_frame, text="", font=(MONO, 7),
                    bg=BG, fg=MUTED, anchor="w")
op_label.pack(fill=tk.X, padx=40)

result_val_label = tk.Label(result_frame, text="—",
                            font=(SERIF, 52, "bold"),
                            bg=BG, fg=FG, anchor="w")
result_val_label.pack(fill=tk.X, padx=40, pady=(0, 20))

root.bind("<Return>", lambda e: None)
root.mainloop()