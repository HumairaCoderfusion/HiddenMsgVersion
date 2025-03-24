# ==========================================================================================
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
#
# ==========================================================================================


from PIL import Image
from cryptography.fernet import Fernet
import random
import base64
import hashlib

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
def hide_text_in_image(image_path, text, output_image_path, password):

    """
    Hide encrypted text inside an image.

    This function takes a path to an image, a plaintext string to hide, an output
    image path to save the image to, and a password to encrypt the text with.
    The function hides the encrypted text inside the image by modifying the
    least significant bit of the color channels of the image's pixels. The
    resulting image is saved to the output image path.

    Args:
        image_path (str): The path to the image to hide the text in.
        text (str): The plaintext string to hide in the image.
        output_image_path (str): The path to save the image with hidden text to.
        password (str): The password used to encrypt the text.

    Returns:
        None
    """
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = img.load()
    width, height = img.size
    
    # Encrypt text and convert to binary
    encrypted_text = encrypt_text(text, password)
    binary_text = text_to_bin(encrypted_text) + '1111111111111110'  # End marker
    
    # Generate a random sequence based on password
    random.seed(password)
    positions = [(x, y) for y in range(height) for x in range(width)]
    random.shuffle(positions)
    
    data_index = 0
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
    
    img.save(output_image_path)
    print(f"Text successfully hidden in {output_image_path}")

# Extract encrypted text from an image
def extract_text_from_image(image_path, password):

    """
    Extract encrypted text from an image.

    This function takes a path to an image and a password, and attempts to extract
    the encrypted text that was previously hidden in the image using the same password.
    The extracted text is decrypted with the password and returned as a plaintext string.

    Args:
        image_path (str): The path to the image to extract text from.
        password (str): The password used to generate the encryption key.

    Returns:
        str: The decrypted plaintext string, or an error message if the password is incorrect.
    """

    img = Image.open(image_path)
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
    return "No hidden text found."

# Example usage
image_path = "photo.jpg"
text = " just some initial text to hide in the image."
output_image_path = "hidden_image.png"
password = "konopasswordlagena"

# Hide the text
hide_text_in_image(image_path, text, output_image_path, password)

# Extract the text
extracted_text = extract_text_from_image(output_image_path, password)
print("Extracted Text:", extracted_text)
