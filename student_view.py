
#student_view.py
import tkinter as tk
from tkinter import messagebox

def run(students_data, parent_window=None):
    view_window = tk.Tk() if parent_window is None else tk.Toplevel(parent_window)
    view_window.geometry("600x500+400+100")
    view_window.config(bg='lightgreen')
    view_window.title("Student Information")
    
    # Variable to keep track of the selected row
    selected_row_index = tk.IntVar(value=-1)
    
    def go_back():
        view_window.destroy()
        if parent_window:
            parent_window.deiconify()  # Show the parent window

    def delete_row():
        selected_idx = selected_row_index.get()
        
        if selected_idx >= 0 and selected_idx < len(students_data):
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
                # Get student name for confirmation message
                student_name = students_data[selected_idx][0]
                
                # Delete the selected student
                students_data.pop(selected_idx)
                
                # Save the updated data
                import student
                student.save_data(students_data)
                
                # Show confirmation
                messagebox.showinfo("Success", f"Student '{student_name}' has been deleted.")
                
                # Refresh the view
                view_window.destroy()
                run(students_data, parent_window)
        else:
            messagebox.showwarning("Warning", "Please select a student to delete")

    def update_info():
        selected_idx = selected_row_index.get()
        
        if selected_idx >= 0 and selected_idx < len(students_data):
            # Close current window
            view_window.destroy()
            # Hide parent window if it exists
            if parent_window:
                parent_window.withdraw()
            # Open student form with selected data pre-filled
            import student
            student.run(students_data, selected_idx)
        else:
            messagebox.showwarning("Warning", "Please select a student to update")

    def on_row_click(row_idx):
        # Set the selected row index
        selected_row_index.set(row_idx)
        
        # Reset all row colors
        for i in range(1, len(students_data) + 1):
            row_bg = '#f0f0f0' if i % 2 == 0 else 'white'
            for col in range(3):  # 3 columns (S.N., Name, ID)
                for widget in table_frame.grid_slaves(row=i, column=col):
                    widget.config(bg=row_bg)
                    
        # Highlight selected row
        row_ui_idx = row_idx + 1  # +1 because row 0 is the header
        for col in range(3):  # 3 columns
            for widget in table_frame.grid_slaves(row=row_ui_idx, column=col):
                widget.config(bg="yellow")
        
        # Show selection message
        if row_idx >= 0 and row_idx < len(students_data):
            name, _ = students_data[row_idx]
            selection_label.config(text=f"Selected: {name}")

    # Create title label
    title_label = tk.Label(view_window, text="STUDENT INFORMATION", font=('arial', 22, 'bold'), bg='lightgreen')
    title_label.place(relx=0.5, rely=0.05, anchor='center')
    
    # Create a frame for the table
    table_frame = tk.Frame(view_window, bg='white')
    table_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.6)
    
    # Create selection status label
    selection_label = tk.Label(view_window, text="Click on a row to select", font=('arial', 12), bg='lightgreen')
    selection_label.place(relx=0.5, rely=0.8, anchor='center')
    
    # Create headers
    tk.Label(table_frame, text="S.N.", font=('arial', 16, 'bold'), bg='lightblue', width=5, anchor='w', padx=10).grid(row=0, column=0, sticky="ew")
    tk.Label(table_frame, text="Student Name", font=('arial', 16, 'bold'), bg='lightblue', width=20, anchor='w', padx=10).grid(row=0, column=1, sticky="ew")
    tk.Label(table_frame, text="Stu ID", font=('arial', 16, 'bold'), bg='lightblue', width=15, anchor='w', padx=10).grid(row=0, column=2, sticky="ew")
    
    # Add scrollbar if there are many students
    if len(students_data) > 10:
        canvas = tk.Canvas(table_frame)
        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
        scrollbar.grid(row=1, column=3, sticky="ns")
        
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        content_frame = scrollable_frame
    else:
        content_frame = table_frame
    
    # Display student data or a message if no data
    if not students_data:
        tk.Label(content_frame, text="No student information available", font=('arial', 14), bg='white').grid(row=1, column=0, columnspan=3, pady=20)
    else:
        # Add student data rows
        for i, (name, student_id) in enumerate(students_data):
            row_idx = i + 1  # UI row index (header is row 0)
            row_bg = '#f0f0f0' if row_idx % 2 == 0 else 'white'  # Alternating row colors
            
            # Create and bind labels for each cell in the row
            sn_label = tk.Label(content_frame, text=f"{row_idx}.", font=('arial', 14), bg=row_bg, anchor='w', padx=10)
            sn_label.grid(row=row_idx, column=0, sticky="ew", pady=5)
            sn_label.bind("<Button-1>", lambda event, idx=i: on_row_click(idx))
            
            name_label = tk.Label(content_frame, text=name, font=('arial', 14), bg=row_bg, anchor='w', padx=10)
            name_label.grid(row=row_idx, column=1, sticky="ew", pady=5)
            name_label.bind("<Button-1>", lambda event, idx=i: on_row_click(idx))
            
            id_label = tk.Label(content_frame, text=student_id, font=('arial', 14), bg=row_bg, anchor='w', padx=10)
            id_label.grid(row=row_idx, column=2, sticky="ew", pady=5)
            id_label.bind("<Button-1>", lambda event, idx=i: on_row_click(idx))
    
    # Back button
    back_button = tk.Button(view_window, text="Back", font=('arial', 16, 'bold'), 
                          bg='#ff9999', command=go_back)
    back_button.place(relx=0.2, rely=0.9, relwidth=0.2, anchor='center')

    delete_button = tk.Button(view_window, text="Delete", font=('arial', 16, 'bold'), 
                          bg='#ff9999', command=delete_row)
    delete_button.place(relx=0.5, rely=0.9, relwidth=0.2, anchor='center')

    update_button = tk.Button(view_window, text="Update", font=('arial', 16, 'bold'), 
                          bg='#ff9999', command=update_info)
    update_button.place(relx=0.8, rely=0.9, relwidth=0.2, anchor='center')
    
    view_window.mainloop()

if __name__ == "__main__":
    # If run directly, show with sample data
    sample_data = [
        ("John Doe", "ID001"),
        ("Jane Smith", "ID002"),
        ("Robert Johnson", "ID003")
    ]
    run(sample_data)




