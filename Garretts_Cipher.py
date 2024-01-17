#!/usr/bin/env python3
# region Import Modules

import json
import os
import math
import sys

# endregion Import Modules

# region Variables

directory_path = os.path.dirname(os.path.realpath(__file__))
path_to_characters = directory_path + "/Data/Characters.json"

# endregion Variables

# region Loading Data


# Load Json file with the characters
def Load_Json():
    temp_data = {}
    with open(path_to_characters) as temp_file:
        temp_data = json.load(temp_file)
    return temp_data


# Get a list with only the valid characters
def Get_Valid_Characters():
    temp_data = []
    for x in loaded_data:
        temp_data.append(x)
    return temp_data


# Get the type of conversion
def Get_Type():
    while True:
        raw_type = 0
        try:
            raw_type = int(input("1 for Cipher | 2 for Decipher | 3 to Quit:\n"))
            if raw_type == 1 or raw_type == 2 or raw_type == 3:
                return raw_type
        except:
            pass


# Get user input
def User_Input(input_type, operation_type):
    raw_string = ""
    # Get the raw string
    if input_type == "Key":
        raw_string = input("Insert Your Key:\n")
    elif input_type == "Code":
        if operation_type == 1:
            raw_string = input("Insert Your Plaintext:\n")
        elif operation_type == 2:
            raw_string = input("Insert Your Ciphertext:\n")
    # Split the string into characters
    string_list = list(raw_string)
    # Get rid of characters that aren't valid, actually I'll replace them with a ?
    valid_string = []
    for x in string_list:
        if x in valid_characters:
            valid_string.append(x)
        else:
            valid_string.append("?")
    return valid_string


# Convert plain text to the corresponding numbers
def Plain_Text_To_Numbers(plain):
    # Convert the plaintext to the corresponding numbers
    converted_text = []
    for x in plain:
        converted_text.append(loaded_data[x]["Order"])
    return converted_text


# Load the json
loaded_data = Load_Json()
valid_characters = Get_Valid_Characters()

# endregion Loading Data

# region Cipher Code


def garrett_cipher(type_of_conversion):
    # Step 1: Starting Values
    key_sum = sum(num_key)
    code_integer = (len(num_code) * (len(num_code) + 1)) / 2
    # Step 2: Integer Code Index
    int_code_index = []
    for x in range(1, len(num_code) + 1):
        temp_x = divmod(code_integer, x)
        int_code_index.append(temp_x[0] + temp_x[1])
    # Step 3: Code Key Index
    code_key_index = []
    for x in range(1, len(num_code) + 1):
        temp_remainder = x % len(num_key)
        if temp_remainder == 0:
            temp_remainder = len(num_key)
        code_key_index.append(temp_remainder)
    # Step 4: Code Key Value
    code_key_value = []
    for x, y in enumerate(code_key_index):
        temp_value = num_key[y - 1]
        code_key_value.append(temp_value + int_code_index[x])
    # Step 5: Code Key Transformation
    code_key_trans = []
    for x, y in enumerate(code_key_value):
        temp_x = (y * (x + 1)) + math.isqrt(key_sum)
        code_key_trans.append(temp_x)
    # Step 6: Key and Code Length Transformation
    key_code_trans = []
    for x in range(len(code_key_trans)):
        temp_key = divmod(code_key_trans[x], len(num_key))
        temp_code = divmod(code_key_trans[x], len(num_code))
        temp_key = temp_key[0] + temp_key[1]
        temp_code = temp_code[0] + temp_code[1]
        temp_result = divmod(temp_key, temp_code)
        temp_result = temp_result[0] + temp_result[1]
        temp_result = temp_result * code_key_value[x]
        key_code_trans.append(temp_result)
    # Step 7: Amount to shift
    shift_amount = []
    for x in key_code_trans:
        temp_x = divmod(x, len(valid_characters))
        if type_of_conversion == 1:
            temp_x = temp_x[0] - temp_x[1]
        elif type_of_conversion == 2:
            temp_x = temp_x[1] - temp_x[0]
        shift_amount.append(temp_x)
    # Step 8: Shift the numbers
    shifted_number = []
    for x, y in enumerate(num_code):
        temp_value = y + shift_amount[x]
        if temp_value > len(valid_characters):
            temp_value = temp_value - len(valid_characters)
        elif temp_value < 1:
            temp_value = len(valid_characters) + temp_value
        shifted_number.append(temp_value)
    # Step 9: Convert numbers into characters
    converted_numbers = []
    for x in shifted_number:
        result = None
        for y in loaded_data:
            number_value = loaded_data[y]["Order"]
            if x == number_value:
                result = y
                break
        if result != None:
            converted_numbers.append(result)
    # Step 10: Convert it back into a string
    converted_string = "".join(converted_numbers)
    return converted_string


# endregion Cipher Code

# region Run Code

while True:
    # Get the plain text from the user
    operation_type = Get_Type()
    if operation_type == 3:
        sys.exit("Goodbye")
    plain_key = User_Input("Key", operation_type)
    plain_code = User_Input("Code", operation_type)

    # Convert the plain text to the corresponding numbers
    num_key = Plain_Text_To_Numbers(plain_key)
    num_code = Plain_Text_To_Numbers(plain_code)

    # Run the main cipher
    cipher = garrett_cipher(operation_type)
    print(f"Your cipher is:\n{cipher}")

# endregion Run Code
