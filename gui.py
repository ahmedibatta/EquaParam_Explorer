import tkinter as tk
from tkinter import filedialog, messagebox
import core  # Importing your core functions

# Global variables to store data
equations = None
variables = None
variable_index = None
parameter_meanings = None
parameter_index = None

def upload_equations():
    global equations, variables, variable_index
    file_path = filedialog.askopenfilename()
    if file_path:
        equations = core.read_equations(file_path)
        variables = core.extract_variables(equations)
        variable_index = core.create_variable_index(equations, variables)
        messagebox.showinfo("Success", "Equations uploaded successfully.")

def upload_parameters():
    global parameter_meanings, parameter_index
    file_path = filedialog.askopenfilename()
    if file_path:
        parameter_meanings = core.read_parameters(file_path)
        parameter_index = core.create_parameter_index(equations, parameter_meanings)
        messagebox.showinfo("Success", "Parameters uploaded successfully.")

def submit(event=None):
    global name_entry, output_text
    input_name = name_entry.get()
    if input_name:
        if equations and parameter_meanings and parameter_index and variable_index:
            info = core.get_info(input_name, equations, parameter_meanings, parameter_index, variable_index)
            output_text.delete('1.0', tk.END)
            for text, tag in info:
                output_text.insert(tk.END, text + "\n", tag)
        else:
            messagebox.showerror("Error", "Please upload equations and parameters first.")
    else:
        messagebox.showwarning("Warning", "Please enter the name of parameter or variable.")



def create_gui():
    global name_entry, output_text
    
    window = tk.Tk()
    window.title("Parameters and Variables Analysis Tool")
    window.configure(bg='#f0f0f0')
    
    top_frame = tk.Frame(window, bg='#f0f0f0')
    top_frame.pack(side=tk.TOP, fill=tk.X)

    title_label = tk.Label(top_frame, text="Parameters and Variables Analysis Tool", bg='#f0f0f0', fg='#333', font=('Helvetica', 16, 'bold'))
    title_label.pack(pady=10)

    button_frame = tk.Frame(window, bg='#f0f0f0')
    button_frame.pack(fill=tk.X, padx=10)

    upload_eq_button = tk.Button(button_frame, text="Upload Equations", command=upload_equations)
    upload_eq_button.pack(side=tk.LEFT, padx=5, pady=10)

    upload_param_button = tk.Button(button_frame, text="Upload Parameters", command=upload_parameters)
    upload_param_button.pack(side=tk.LEFT, padx=5, pady=10)

    # Add a label with instructions
    instruction_label = tk.Label(window, text="Please enter the full or partial name of the parameter/variable:", bg='#f0f0f0')
    instruction_label.pack(fill=tk.X, padx=10, pady=5)

    name_entry_frame = tk.Frame(window, bg='#f0f0f0')
    name_entry_frame.pack(fill=tk.X, padx=10, pady=5)

    name_entry = tk.Entry(name_entry_frame, bd=2)
    name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    name_entry.bind("<Return>", submit)

    submit_button = tk.Button(name_entry_frame, text="Submit", command=submit)
    submit_button.pack(side=tk.RIGHT, padx=5)

    output_text = tk.Text(window, wrap=tk.WORD, height=10)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    output_scroll = tk.Scrollbar(window, command=output_text.yview)
    output_text.configure(yscrollcommand=output_scroll.set)
    output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    output_text.tag_configure('meaning', foreground='gray', font=('Helvetica', 12), spacing1=4, spacing3=4)
    output_text.tag_configure('category', foreground='red', font=('Helvetica', 12, 'bold'), spacing1=4, spacing3=4)
    output_text.tag_configure('equation', foreground='blue', font=('Helvetica', 12), spacing1=4, spacing3=4)

    return window
