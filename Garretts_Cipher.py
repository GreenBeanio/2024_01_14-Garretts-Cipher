#!/usr/bin/env python3
# region Import Modules

import json
import os
import math
import sys
import random

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
    while True:
        try:
            raw_string = ""
            # Get the raw string
            if input_type == "Key":
                raw_string = input("Insert Your Key:\n")
            elif input_type == "Code":
                if operation_type == 1:
                    raw_string = input("Insert Your Plaintext:\n")
                elif operation_type == 2:
                    raw_string = input("Insert Your Ciphertext:\n")
            # If we're deciphering do some processing first
            if operation_type == 2 and input_type == "Code":
                raw_string = handle_spacing(raw_string, operation_type)
            # Split the string into characters
            string_list = list(raw_string)
            # Get rid of characters that aren't valid, actually I'll replace them with a ?
            valid_string = []
            for x in string_list:
                if x in valid_characters:
                    valid_string.append(x)
                else:
                    valid_string.append("?")
            # Only return if it isn't empty
            if len(valid_string) != 0:
                return valid_string
            else:
                print("Invalid Input")
        except:
            pass


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


# Continue to divide and reduce large results until they're within range
# This could be something I look to redo, as if you change the amount of valid characters the entire encryption will change
def reduce_over(temp_result):
    while abs(temp_result) > len(valid_characters):
        temp_result = divmod(temp_result, math.isqrt(len(valid_characters)))
        temp_result = temp_result[0] + temp_result[1]
    else:
        return temp_result


# Add or remove red herrings from the code
def red_herring(key_sum, cipher, type_of_conversion):
    # Step 1: Getting the amount of red herrings
    key_isqrt = math.isqrt(key_sum)
    key_qr = divmod(key_sum, len(num_key))
    key_qrt = key_qr[0] + key_qr[1]
    key_qr2 = divmod(key_qrt, key_isqrt)
    red_herring_amount = key_qr2[0] + key_qr2[1]
    original_length = 0
    ## If we are adding red herrings use the length of the cipher
    if type_of_conversion == 1:
        original_length = len(cipher)
    ## If we are removing add herrings subtract the total herrings from the length of the cipher
    else:
        original_length = len(cipher) - red_herring_amount
    # Step 2: Getting the distribution of inner red herrings
    inner_rh_every = math.ceil(original_length / red_herring_amount)
    # Step 3: How many inner and outer red herrings
    inner_rh_amount = original_length // inner_rh_every
    outer_rh_amount = red_herring_amount - inner_rh_amount
    # Step 4: Determine how many start and end outer red herrings
    start_rh_amount = 0
    end_rh_amount = 0
    temp_out_rh = divmod(outer_rh_amount, 2)
    ## If the remainder is even add it to the front
    if temp_out_rh[1] % 2 == 0:
        start_rh_amount = temp_out_rh[0] + temp_out_rh[1]
        end_rh_amount = temp_out_rh[0]
    ## If the remainder is odd add it to the back
    else:
        start_rh_amount = temp_out_rh[0]
        end_rh_amount = temp_out_rh[0] + temp_out_rh[1]
    # Step 5: Check if the amount of red herrings is correct
    check_total = inner_rh_amount + start_rh_amount + end_rh_amount
    ## If the total is not correct stop and return nothing
    if red_herring_amount != check_total:
        return None
    ## Branching off based on if red herring are being added or removed
    ## If we are adding red herrings
    if type_of_conversion == 1:
        # Step 6: Add the inner herrings
        added_inner = 0
        for x in range(1, inner_rh_amount + 1):
            temp_index = (x * inner_rh_every) + added_inner
            temp_random = random.randint(1, len(valid_characters))
            cipher.insert(temp_index, temp_random)
            added_inner += 1
        # Step 7: Add the outer herrings
        start_herring_numbers = []
        for x in range(start_rh_amount):
            start_herring_numbers.append(random.randint(1, len(valid_characters)))
        end_herring_numbers = []
        for x in range(end_rh_amount):
            end_herring_numbers.append(random.randint(1, len(valid_characters)))
        cipher = start_herring_numbers + cipher + end_herring_numbers
        # Step 8: Check if the new cipher length if equal to the original cipher and the red herrings
        if len(cipher) == (original_length + red_herring_amount):
            return cipher
        else:
            return None
    ## If we are removing red herrings
    else:
        # Step 6: Remove the outer herrings
        temp_start = start_rh_amount
        temp_end = len(cipher) - end_rh_amount
        cipher = cipher[temp_start:temp_end]
        # Step 7: Remove the inner herrings
        for x in range(1, inner_rh_amount + 1):
            temp_index = x * inner_rh_every
            cipher.pop(temp_index)
        # Step 8: Check if the new cipher length if equal to the original cipher with the red herrings
        if len(cipher) == original_length:
            return cipher
        else:
            return None


# Add or remove the cipher start and end indicators
def handle_spacing(cipher, type_of_conversion):
    # If we're making a cipher add these markers as the final step
    if type_of_conversion == 1:
        cipher = f"|||{cipher}|||"
    # If we're deciphering remove the markers as the first step
    else:
        cipher = cipher[3 : len(cipher) - 3]
    return cipher


# Handle the main cipher
def garrett_cipher(type_of_conversion):
    # Step 1: Get starting values
    key_sum = sum(num_key)
    use_num_code = num_code
    # Step 2 (Decipher Only): Remove the red herrings
    if type_of_conversion == 2:
        temp_no_red_herring = red_herring(key_sum, use_num_code, type_of_conversion)
        ## If it didn't work
        if temp_no_red_herring == None:
            return None
        ## If it did work
        else:
            use_num_code = temp_no_red_herring
    # Step 3: Integer Code Index
    code_integer = (len(use_num_code) * (len(use_num_code) + 1)) / 2
    int_code_index = []
    for x in range(1, len(use_num_code) + 1):
        temp_x = divmod(code_integer, x)
        int_code_index.append(temp_x[0] + temp_x[1])
    # Step 4: Code Key Index
    code_key_index = []
    for x in range(1, len(use_num_code) + 1):
        temp_remainder = x % len(num_key)
        if temp_remainder == 0:
            temp_remainder = len(num_key)
        code_key_index.append(temp_remainder)
    # Step 5: Code Key Value
    code_key_value = []
    for x, y in enumerate(code_key_index):
        temp_value = num_key[y - 1]
        code_key_value.append(temp_value + int_code_index[x])
    # Step 6: Code Key Transformation
    code_key_trans = []
    for x, y in enumerate(code_key_value):
        temp_x = (y * (x + 1)) + math.isqrt(key_sum)
        code_key_trans.append(temp_x)
    # Step 7: Key and Code Length Transformation
    key_code_trans = []
    for x in range(len(code_key_trans)):
        temp_key = divmod(code_key_trans[x], len(num_key))
        temp_code = divmod(code_key_trans[x], len(use_num_code))
        temp_key = temp_key[0] + temp_key[1]
        temp_code = temp_code[0] + temp_code[1]
        temp_result = divmod(temp_key, temp_code)
        temp_result = temp_result[0] + temp_result[1]
        temp_result = temp_result * code_key_value[x]
        # If the amount is more than the entire character set
        if temp_result > len(valid_characters):
            temp_result = reduce_over(temp_result)
        # Determine if a character will shift left (decrease) or right (increase)
        if code_key_trans[x] % 2 != 0:
            temp_result = -temp_result
        key_code_trans.append(temp_result)
    # Step 8: Amount to shift
    shift_amount = []
    for x in key_code_trans:
        temp_x = divmod(x, len(valid_characters))
        if type_of_conversion == 1:
            temp_x = temp_x[0] - temp_x[1]
        elif type_of_conversion == 2:
            temp_x = temp_x[1] - temp_x[0]
        shift_amount.append(temp_x)
    # Step 9: Shift the numbers
    shifted_number = []
    for x, y in enumerate(use_num_code):
        temp_value = y + shift_amount[x]
        if temp_value > len(valid_characters):
            temp_value = temp_value - len(valid_characters)
        elif temp_value < 1:
            temp_value = len(valid_characters) + temp_value
        shifted_number.append(temp_value)
    # Step 10 (Cipher Only): Add the red herrings
    if type_of_conversion == 1:
        temp_red_herring = red_herring(key_sum, shifted_number, type_of_conversion)
        ## If it didn't work
        if temp_red_herring == None:
            return None
        ## If it did work
        else:
            shifted_number = temp_red_herring
    # Step 11: Convert numbers into characters
    converted_numbers = []
    for x in shifted_number:
        result = None
        for y in loaded_data:
            number_value = loaded_data[y]["Order"]
            if x == number_value:
                result = y
                break
        # If there was a valid result add it
        if result != None:
            converted_numbers.append(result)
        # If there wasn't a valid result break because it's broken and a waste of time to continue
        else:
            break
    # Step 12: Convert it back into a string
    converted_string = "".join(converted_numbers)
    # Step 13: Check if the conversion was successful
    if len(shifted_number) == len(converted_numbers):
        # If we're making a cipher
        if type_of_conversion == 1:
            return handle_spacing(converted_string, type_of_conversion)
        else:
            return converted_string
    else:
        return None


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
    if cipher != None:
        if operation_type == 1:
            print(f"Your ciphertext is:\n{cipher}")
        else:
            print(f"Your plaintext is:\n{cipher}")
    else:
        if operation_type == 1:
            print(f"Sorry, there was an error in converting your ciphertext.")
        else:
            print(f"Sorry, there was an error in converting your plaintext.")

# endregion Run Code
