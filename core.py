import pandas as pd
import openpyxl
import re

def read_equations(file_path):
    equations = {}
    current_category = None
    with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
        for line in csvfile:
            line = line.strip()
            if line.startswith('%%'):
                current_category = line[2:].strip()
                equations[current_category] = []
            elif current_category is not None and line:
                if ';' in line:
                    equation = line.split(';')[0].strip()
                    equation = equation.strip('\'"')
                    equations[current_category].append(equation)
    return equations

def extract_variables(equations):
    variable_pattern = re.compile(r'^\s*(\w+)\s*=')
    variables = set()
    for eqs in equations.values():
        for eq in eqs:
            match = variable_pattern.match(eq)
            if match:
                variables.add(match.group(1))
    return variables

def create_variable_index(equations, variables):
    variable_index = {var: [] for var in variables}
    for category, eqs in equations.items():
        for eq_number, eq in enumerate(eqs):
            for variable in variables:
                if variable in eq:
                    variable_index[variable].append((category, eq_number))
    return variable_index

def read_parameters(file_path):
    parameters = {}
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        parameter_name = row['Parameter Name']
        description = row['Description']
        parameters[parameter_name] = description
    return parameters

def create_parameter_index(equations, parameter_meanings):
    parameter_index = {key: [] for key in parameter_meanings}
    for category, eqs in equations.items():
        for eq_number, eq in enumerate(eqs):
            for parameter in parameter_meanings:
                if parameter in eq:
                    parameter_index[parameter].append((category, eq_number))
    return parameter_index

def get_info(input_name, equations, parameter_meanings, parameter_index, variable_index):
    info = []
    found = False
    category_dict = {}

    def add_to_category_dict(eq_references):
        for category, eq_number in eq_references:
            eq = equations[category][eq_number]
            if category not in category_dict:
                category_dict[category] = []
            category_dict[category].append(eq)

    # Check for exact matches first
    if input_name in parameter_meanings:
        meaning = parameter_meanings[input_name]
        eq_references = parameter_index.get(input_name, [])
        info.append((f"Name: {input_name}", 'variable'))  # Add a tag for variable names
        info.append((f"Meaning: {meaning}", 'meaning'))  # Use the 'meaning' tag for meanings
        add_to_category_dict(eq_references)
        found = True
    elif input_name in variable_index:
        info.append((f"Variable: {input_name}", 'variable'))
        eq_references = variable_index.get(input_name, [])
        add_to_category_dict(eq_references)
        found = True

    # If no exact match, look for partial matches
    if not found:
        for name in parameter_meanings:
            if input_name in name:
                meaning = parameter_meanings[name]
                eq_references = parameter_index.get(name, [])
                info.append((f"Name: {name}", 'variable'))
                info.append((f"Meaning: {meaning}", 'meaning'))
                add_to_category_dict(eq_references)
        for name in variable_index:
            if input_name in name:
                info.append((f"Variable: {name}", 'variable'))
                eq_references = variable_index.get(name, [])
                add_to_category_dict(eq_references)

    # Add categories and equations to the info list with appropriate tags
    for category, eqs in category_dict.items():
        info.append((f"Category: {category}", 'category'))
        for eq in eqs:
            info.append((eq, 'equation'))

    if len(info) == 0:
        return [("Name not found", 'error')]  # Assuming you define an 'error' tag in your Text widget

    return info
