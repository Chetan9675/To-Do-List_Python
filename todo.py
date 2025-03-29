import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # Initialize tasks list
        self.tasks = []
        
        # Create GUI elements
        self.create_widgets()
        
        # Load tasks if save file exists
        self.load_tasks()
    
    def create_widgets(self):
        # Styling
        self.bg_color = "#f0f0f0"
        self.button_color = "#4a7a8c"
        self.text_color = "#333333"
        self.completed_color = "#888888"
        
        self.root.config(bg=self.bg_color)
        
        # Header
        self.header_frame = tk.Frame(self.root, bg=self.bg_color)
        self.header_frame.pack(pady=10)
        
        self.title_label = tk.Label(
            self.header_frame,
            text="To-Do List",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.pack()
        
        # Input area
        self.input_frame = tk.Frame(self.root, bg=self.bg_color)
        self.input_frame.pack(pady=10)
        
        self.task_entry = tk.Entry(
            self.input_frame,
            width=40,
            font=("Helvetica", 12),
            bd=2,
            relief=tk.GROOVE
        )
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        self.add_button = tk.Button(
            self.input_frame,
            text="Add",
            command=self.add_task,
            bg=self.button_color,
            fg="white",
            bd=0,
            padx=10,
            font=("Helvetica", 10, "bold")
        )
        self.add_button.pack(side=tk.LEFT)
        
        # Task list
        self.list_frame = tk.Frame(self.root, bg=self.bg_color)
        self.list_frame.pack(pady=10)
        
        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox = tk.Listbox(
            self.list_frame,
            width=50,
            height=15,
            font=("Helvetica", 12),
            yscrollcommand=self.scrollbar.set,
            selectbackground="#a6a6a6",
            bd=2,
            relief=tk.GROOVE,
            selectmode=tk.SINGLE
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.task_listbox.yview)
        
        # Bind double click to edit
        self.task_listbox.bind("<Double-Button-1>", self.edit_task)
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        self.buttons_frame.pack(pady=10)
        
        self.complete_button = tk.Button(
            self.buttons_frame,
            text="Mark Complete",
            command=self.mark_complete,
            bg=self.button_color,
            fg="white",
            bd=0,
            padx=10,
            font=("Helvetica", 10, "bold")
        )
        self.complete_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(
            self.buttons_frame,
            text="Delete",
            command=self.delete_task,
            bg="#8c4a4a",
            fg="white",
            bd=0,
            padx=10,
            font=("Helvetica", 10, "bold")
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = tk.Button(
            self.buttons_frame,
            text="Save",
            command=self.save_tasks,
            bg="#4a8c5e",
            fg="white",
            bd=0,
            padx=10,
            font=("Helvetica", 10, "bold")
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(
            self.buttons_frame,
            text="Clear All",
            command=self.clear_tasks,
            bg="#8c7a4a",
            fg="white",
            bd=0,
            padx=10,
            font=("Helvetica", 10, "bold")
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")
    
    def edit_task(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            old_text = self.tasks[selected_index]["text"]
            
            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("300x100")
            edit_window.resizable(False, False)
            edit_window.config(bg=self.bg_color)
            
            # Edit entry
            edit_entry = tk.Entry(
                edit_window,
                width=30,
                font=("Helvetica", 12),
                bd=2,
                relief=tk.GROOVE
            )
            edit_entry.pack(pady=10)
            edit_entry.insert(0, old_text)
            edit_entry.focus_set()
            
            # Save button
            save_button = tk.Button(
                edit_window,
                text="Save",
                command=lambda: self.save_edited_task(selected_index, edit_entry.get(), edit_window),
                bg=self.button_color,
                fg="white",
                bd=0,
                padx=10,
                font=("Helvetica", 10, "bold")
            )
            save_button.pack()
    
    def save_edited_task(self, index, new_text, window):
        if new_text.strip():
            self.tasks[index]["text"] = new_text.strip()
            self.update_listbox()
            window.destroy()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty.")
    
    def mark_complete(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            self.tasks[selected_index]["completed"] = not self.tasks[selected_index]["completed"]
            self.update_listbox()
    
    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            del self.tasks[selected_index]
            self.update_listbox()
    
    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.tasks = []
            self.update_listbox()
    
    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_text = task["text"]
            if task["completed"]:
                task_text = f"✓ {task_text}"
                self.task_listbox.insert(tk.END, task_text)
                self.task_listbox.itemconfig(tk.END, {'fg': self.completed_color})
            else:
                self.task_listbox.insert(tk.END, task_text)
    
    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save tasks to file"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.tasks, f)
                messagebox.showinfo("Success", "Tasks saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def load_tasks(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load tasks from file"
        )
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    self.tasks = json.load(f)
                self.update_listbox()
                messagebox.showinfo("Success", "Tasks loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
