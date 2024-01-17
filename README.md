# Garrett's_Cipher

# What Does It Do?

I wanted to try and make a cipher so I did. It's probably not any good for any real secrecy, but it does work!

# How To Use It?

- Run the program in the same folder/directory as the script.
- Choose if you're making a cipher or deciphering.
- Type in the key you're using.
- Enjoy your coded message.

# What Characters Can I Use?

If you're using a US keyboard you should be able to use every key. If you're using another language or other symbols you'll need to add them into the JSON file yourself.
The JSON file has information on the type of character and the corresponding ASCII code, but it isn't used. If you're adding more characters all you need to care about is
adding the character itself as the main item and incrementing the "Order" number.

### Windows

- Initial Run
  - cd /your/folder
  - python3 -m venv env
  - call env/Scripts/activate.bat
  - python3 Garretts_Cipher.py
- Running After
  - cd /your/folder
  - call env/Scripts/activate.bat && python3 Garretts_Cipher.py

### Linux

- Initial Run
  - cd /your/folder
  - python3 -m venv env
  - source env/bin/activate
  - python3 Garretts_Cipher.py
- Running After
  - cd /your/folder
  - source env/bin/activate && python3 Garretts_Cipher.py
  - You may have to set executable if it doesn't work
    - chmod +x Garretts_Cipher.py
