import tkinter as tk
from tkinter import messagebox
from datetime import datetime

root = tk.Tk()
root.title("Ultimate To-Do List")
root.geometry("400x500")
root.config(bg="#f0f0f0")

# --- Functions ---
def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            tasks = f.readlines()
            for task in tasks:
                listbox.insert(tk.END, task.strip())
    except FileNotFoundError:
        pass

def save_tasks():
    tasks = listbox.get(0, tk.END)
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")

def add_task():
    task = entry.get().strip()
    if task != "":
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        task_with_time = f"{task} - {now}"
        listbox.insert(tk.END, task_with_time)
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def delete_task():
    selected = listbox.curselection()
    if selected:
        listbox.delete(selected[0])
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Select a task to delete!")

def clear_tasks():
    if messagebox.askyesno("Confirm", "Clear all tasks?"):
        listbox.delete(0, tk.END)
        save_tasks()

def mark_complete(event):
    selected = listbox.curselection()
    if selected:
        idx = selected[0]
        task = listbox.get(idx)
        # Toggle completed
        if "[Done]" not in task:
            task = f"[Done] {task}"
            listbox.itemconfig(idx, fg="green")
        else:
            task = task.replace("[Done] ", "")
            listbox.itemconfig(idx, fg="black")
        listbox.delete(idx)
        listbox.insert(idx, task)
        save_tasks()

# --- GUI Elements ---
entry = tk.Entry(root, width=30, font=("Arial", 14))
entry.pack(pady=15)

add_button = tk.Button(root, text="Add Task", width=15, command=add_task, bg="#4CAF50", fg="white")
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", width=15, command=delete_task, bg="#f44336", fg="white")
delete_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear All", width=15, command=clear_tasks, bg="#FF9800", fg="white")
clear_button.pack(pady=5)

listbox = tk.Listbox(root, width=50, height=15, font=("Arial", 12))
listbox.pack(pady=15)
listbox.bind("<Double-Button-1>", mark_complete)  # Double click to mark complete

# Load previous tasks
load_tasks()

root.mainloop()