# =========================================================================================================
#
# 👤 Author: Nibir
# 🌐 Github: https://www.github.com/mahmudnibir
# 📅 Date: 2025-03-24 
# 
# 📌 Project: Image Steganography (LSB Technique with AES Encryption)
# 🔍 Description:
#    This script hides text inside an image using the least significant bit (LSB) method.
#    It uses the AES encryption algorithm for encrypting and decrypting the text before embedding it.
#    The text is first encrypted with a password using AES, then converted to binary.
#    The binary data is hidden in the least significant bits of the image's RGB channels.
#    The encrypted text can be extracted from the image using the LSB method and decrypted
#    using the password to reveal the original text.
#
# 🛠️ Dependencies:
#    - cryptography (for AES encryption) → Install using: pip install cryptography
#    - Pillow (PIL) → Install using: pip install pillow
#    - termcolor (for colored text) → Install using: pip install termcolor 
#    - art (for ASCII art) → Install using: pip install art
# ========================================================================================================= 


from PIL import Image
from cryptography.fernet import Fernet
import random
import base64
import hashlib
from termcolor import colored
from art import text2art
import sys
import time


AUTHOR_NAME = "Nibir Mahmud"
AUTHOR_GITHUB = "github.com/mahmudnibir"
AUTHOR_PROJECT = "Hidden Message in Image"


def print_AUTHOR_info():
    """
    Display the author's information in a stylized manner.

    This function prints the author's name, GitHub link, and project name
    using colored text for enhanced visual appeal.
    """

    """Displays AUTHOR information in a cool way."""
    print(colored("\n📌 Author:", 'yellow'), colored(AUTHOR_NAME, 'cyan'))
    print(colored("🔗 GitHub:", 'yellow'), colored(AUTHOR_GITHUB, 'cyan'))
    print(colored("🛠️ Project:", 'yellow'), colored(AUTHOR_PROJECT, 'cyan'))
    
    # Print a separator line in magenta
    print(colored("=" * 100, 'magenta'))

def animated_logo(text="Unfollow"):
    """Prints the logo with a typing animation effect."""
    logo = text2art(text)  # Generate ASCII text
    for char in logo:
        sys.stdout.write(colored(char, 'cyan'))  # Print each character with color
        sys.stdout.flush()  # Force output without waiting for a new line
        time.sleep(0.002)  # Adjust speed (lower = faster)

# Generate encryption key from password
def generate_key(password):
    """
    Generate a key from a password.

    This function takes a string password, hashes it with SHA-256, and then
    encodes the hash with url-safe base64 encoding to produce a key that can be
    used with the Fernet symmetric encryption algorithm.

    Args:
        password (str): The password to generate the key from.

    Returns:
        bytes: The generated key, as a url-safe base64 encoded string.
    """

    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

# Encrypt text using AES
def encrypt_text(text, password):
    """
    Encrypt a given text using a password.

    This function takes a plaintext string and a password, generates an encryption
    key from the password, and uses it to encrypt the text with the Fernet symmetric
    encryption algorithm. The encrypted text is returned as a base64-encoded string.

    Args:
        text (str): The plaintext string to encrypt.
        password (str): The password used to generate the encryption key.

    Returns:
        str: The encrypted text as a base64-encoded string.
    """
    key = generate_key(password)
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()

# Decrypt text using AES
def decrypt_text(encrypted_text, password):
    """
    Decrypt an encrypted text using a password.

    This function takes an encrypted text string and a password, generates a decryption
    key from the password, and uses it to decrypt the text with the Fernet symmetric
    encryption algorithm. The decrypted text is returned as a plaintext string.

    Args:
        encrypted_text (str): The encrypted text to decrypt.
        password (str): The password used to generate the decryption key.

    Returns:
        str: The decrypted plaintext string.
    """

    key = generate_key(password)
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_text.encode()).decode()

# Convert text to binary
def text_to_bin(text):

    """
    Convert text to a binary string representation.

    This function takes a plaintext string and converts each character
    into its binary representation using 8 bits per character. The resulting
    binary strings are concatenated into a single binary string.

    Args:
        text (str): The plaintext string to convert to binary.

    Returns:
        str: A binary string representation of the input text.
    """

    return ''.join(format(ord(char), '08b') for char in text)

# Convert binary to text
def bin_to_text(binary_data):

    """
    Convert a binary string to a plaintext string.

    This function takes a binary string and separates it into 8-bit
    chunks. Each chunk is converted back to a character using the
    chr() function, and the characters are concatenated into a single
    string.

    Args:
        binary_data (str): The binary string to convert to text.

    Returns:
        str: The plaintext string representation of the input binary data.
    """

    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

# Hide encrypted text inside an image
def hide_text_in_image(IMAGE_PATH, text, OUTPUT_IMAGE_PATH, password):

    """
    Hide encrypted text inside an image.

    This function takes a path to an image, a plaintext string to hide, an output
    image path to save the image to, and a password to encrypt the text with.
    The function hides the encrypted text inside the image by modifying the
    least significant bit of the color channels of the image's pixels. The
    resulting image is saved to the output image path.

    Args:
        IMAGE_PATH (str): The path to the image to hide the text in.
        text (str): The plaintext string to hide in the image.
        OUTPUT_IMAGE_PATH (str): The path to save the image with hidden text to.
        password (str): The password used to encrypt the text.

    Returns:
        None
    """
    try:
        img = Image.open(IMAGE_PATH)
        img = img.convert("RGB")
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    pixels = img.load()
    width, height = img.size

    try:
        encrypted_text = encrypt_text(text, password)
        binary_text = text_to_bin(encrypted_text) + '1111111111111110'  # End marker
    except Exception as e:
        print(f"Error encrypting text: {e}")
        return

    # Generate a random sequence based on password
    random.seed(password)
    positions = [(x, y) for y in range(height) for x in range(width)]
    random.shuffle(positions)

    
    data_index = 0
    try:
        for x, y in positions:
            r, g, b = pixels[x, y]
            
            if data_index < len(binary_text):
                r = r & 0xFE | int(binary_text[data_index])
                data_index += 1
            if data_index < len(binary_text):
                g = g & 0xFE | int(binary_text[data_index])
                data_index += 1
            if data_index < len(binary_text):
                b = b & 0xFE | int(binary_text[data_index])
                data_index += 1
            
            pixels[x, y] = (r, g, b)
            if data_index >= len(binary_text):
                break
    except Exception as e:
        print(f"Error hiding text in image: {e}")
        return

    try:
        img.save(OUTPUT_IMAGE_PATH)
        print(f"Text successfully hidden in {OUTPUT_IMAGE_PATH}")
    except Exception as e:
        print(f"Error saving image: {e}")
    for x, y in positions:
        r, g, b = pixels[x, y]
        
        if data_index < len(binary_text):
            r = r & 0xFE | int(binary_text[data_index])
            data_index += 1
        if data_index < len(binary_text):
            g = g & 0xFE | int(binary_text[data_index])
            data_index += 1
        if data_index < len(binary_text):
            b = b & 0xFE | int(binary_text[data_index])
            data_index += 1
        
        pixels[x, y] = (r, g, b)
        if data_index >= len(binary_text):
            break
    
    img.save(OUTPUT_IMAGE_PATH)
    print(f"Text successfully hidden in {OUTPUT_IMAGE_PATH}")

# Extract encrypted text from an image
def extract_text_from_image(IMAGE_PATH, password):

    """
    Extract encrypted text from an image.

    This function takes a path to an image and a password, and attempts to extract
    the encrypted text that was previously hidden in the image using the same password.
    The extracted text is decrypted with the password and returned as a plaintext string.

    Args:
        IMAGE_PATH (str): The path to the image to extract text from.
        password (str): The password used to generate the encryption key.

    Returns:
        str: The decrypted plaintext string, or an error message if the password is incorrect.
    """

    img = Image.open(IMAGE_PATH)
    img = img.convert("RGB")
    pixels = img.load()
    width, height = img.size
    
    # Generate same random sequence based on password
    random.seed(password)
    positions = [(x, y) for y in range(height) for x in range(width)]
    random.shuffle(positions)
    
    binary_data = ''
    for x, y in positions:
        r, g, b = pixels[x, y]
        binary_data += str(r & 1) + str(g & 1) + str(b & 1)
    
    end_marker = '1111111111111110'
    end_index = binary_data.find(end_marker)
    if end_index != -1:
        binary_data = binary_data[:end_index]
        encrypted_text = bin_to_text(binary_data)
        try:
            return decrypt_text(encrypted_text, password)
        except:
            return "Incorrect password! Cannot decrypt."
    return "Incorrect password! Cannot decrypt."


if __name__ == "__main__":
    try:
        animated_logo("Hidden Message")
        print_AUTHOR_info()  # Display AUTHOR info
        print("Welcome to the Unfollow Script!")

        # Ask user what to do
        print(colored("\nWhat would you like to do?", 'yellow'))
        print(colored("1. Hide text in image", 'green'))
        print(colored("2. Extract text from image", 'red'))
        choice = input(colored("Enter your choice (1/2): ", 'cyan'))

        if choice == '1':
            # Hide text in image
            PASSWORD = input(colored("Enter the password for encryption: ", 'cyan'))
            text = input(colored("Enter the text to hide in the image: ", 'cyan'))
            IMAGE_PATH = input(colored("Enter the path to the image file: ", 'cyan'))
            OUTPUT_IMAGE_PATH = input(colored("Enter the path to save the output image: ", 'cyan'))
            hide_text_in_image(IMAGE_PATH, text, OUTPUT_IMAGE_PATH, PASSWORD)
            print(colored(f"Text successfully hidden in {OUTPUT_IMAGE_PATH}", 'green'))
        elif choice == '2':
            # Extract text from image
            PASSWORD = input(colored("Enter the password for decryption: ", 'cyan'))
            IMAGE_PATH = input(colored("Enter the path to the image file: ", 'cyan'))
            extracted_text = extract_text_from_image(IMAGE_PATH, PASSWORD)
            print(colored("Extracted Text:", 'green'))
            print(extracted_text)
        else:
            print(colored("Invalid choice. Please try again.", 'red'))

    except Exception as e:
        print(colored(f"An error occurred: {e}", 'red'))
