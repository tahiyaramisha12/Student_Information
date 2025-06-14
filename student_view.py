import tkinter as tk
from tkinter import messagebox
import student  # Move import to top

def run(students_data, parent_window=None):
    view_window = tk.Tk() if parent_window is None else tk.Toplevel(parent_window)
    view_window.geometry("600x500+400+100")
    view_window.config(bg='lightgreen')
    view_window.title("Student Information")

    selected_row_index = tk.IntVar(value=-1)

    def go_back():
        view_window.destroy()
        import student
        student.run(students_data)

    def delete_row():
        idx = selected_row_index.get()
        if 0 <= idx < len(students_data):
            if messagebox.askyesno("Confirm", "Delete selected student?"):
                name = students_data[idx][0]
                students_data.pop(idx)
                student.save_data(students_data)
                messagebox.showinfo("Deleted", f"Removed {name}")
                view_window.destroy()
                run(students_data, parent_window)
        else:
            messagebox.showwarning("Warning", "Select a student first")

    def update_info():
        idx = selected_row_index.get()
        if 0 <= idx < len(students_data):
            view_window.withdraw()
            student.run(students_data, idx)
            view_window.destroy()
        else:
            messagebox.showwarning("Warning", "Select a student first")

    def on_row_click(idx):
        selected_row_index.set(idx)
        selection_label.config(text=f"Selected: {students_data[idx][0]}")
        # Highlight selected row
        for widget in table_frame.grid_slaves():
            widget.config(bg='white')
        # Highlight this row
        for widget in table_frame.grid_slaves(row=idx+1):
            widget.config(bg='yellow')

    title = tk.Label(view_window, text="STUDENT INFORMATION", font=('arial', 22, 'bold'), bg='lightgreen')
    title.place(relx=0.5, rely=0.05, anchor='center')

    table_frame = tk.Frame(view_window, bg='white')
    table_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.6)

    tk.Label(table_frame, text="S.N.", font=('arial', 16, 'bold'), bg='lightblue', width=5).grid(row=0, column=0)
    tk.Label(table_frame, text="Name", font=('arial', 16, 'bold'), bg='lightblue', width=20).grid(row=0, column=1)
    tk.Label(table_frame, text="ID", font=('arial', 16, 'bold'), bg='lightblue', width=15).grid(row=0, column=2)

    if not students_data:
        tk.Label(table_frame, text="No student information available", bg='white', font=('arial', 14)).grid(row=1, column=0, columnspan=3, pady=20)
    else:
        for i, (name, sid) in enumerate(students_data):
            bg = '#f0f0f0' if i % 2 == 0 else 'white'
            sn = tk.Label(table_frame, text=f"{i+1}.", font=('arial', 14), bg=bg)
            sn.grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            sn.bind("<Button-1>", lambda e, idx=i: on_row_click(idx))

            nm = tk.Label(table_frame, text=name, font=('arial', 14), bg=bg)
            nm.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)
            nm.bind("<Button-1>", lambda e, idx=i: on_row_click(idx))

            idl = tk.Label(table_frame, text=sid, font=('arial', 14), bg=bg)
            idl.grid(row=i+1, column=2, sticky="w", padx=10, pady=5)
            idl.bind("<Button-1>", lambda e, idx=i: on_row_click(idx))

    selection_label = tk.Label(view_window, text="Click a row to select", font=('arial', 14), bg='lightgreen')
    selection_label.place(relx=0.5, rely=0.8, anchor='center')

    back_btn = tk.Button(view_window, text="🔙 Back", font=('arial', 16, 'bold'), bg='#ff9999', command=go_back)
    back_btn.place(relx=0.2, rely=0.9, relwidth=0.2, anchor='center')

    del_btn = tk.Button(view_window, text="🗑️Delete", font=('arial', 16, 'bold'), bg='#ff9999', command=delete_row)
    del_btn.place(relx=0.5, rely=0.9, relwidth=0.2, anchor='center')

    upd_btn = tk.Button(view_window, text="✏️ Update", font=('arial', 16, 'bold'), bg='#ff9999', command=update_info)
    upd_btn.place(relx=0.8, rely=0.9, relwidth=0.2, anchor='center')

    view_window.mainloop()

if __name__ == "__main__":
    sample = [("John Doe","ID001"), ("Jane Smith","ID002")]
    run(sample)