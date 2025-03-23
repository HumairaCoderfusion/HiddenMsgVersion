# ==========================================================================================
#
# 📌 Project: Image Steganography (LSB Technique)
# 🔍 Description:
#    This script embeds a secret text file inside an image using the Least Significant Bit (LSB)
#    steganography technique. The image pixels' least significant bits are modified to store 
#    the binary representation of the text.
#
# 👤 Author: NibirMahmud
# 🌐 Website: https://www.github.com/mahmudnibir
# 📜 License: MIT License 
#
# 🛠️ Dependencies:
#    - Pillow (PIL) → Install using: pip install pillow
#
# 🚀 Features:
#    ✅ Hide a text message inside an image without noticeable changes.
#    ✅ Extract hidden text from the modified image.
#    ✅ Uses a delimiter (1111111111111110) to detect the end of the message.
#
# 💡 Future Improvements:
#    - Encrypt text before embedding for added security.
#    - Support for multiple file formats and larger payloads.
# ==========================================================================================


from PIL import Image

def text_to_bin(text):
    """Convert text to binary"""
    return ''.join(format(ord(char), '08b') for char in text)

def hide_text_in_image(image_path, text_file_path, output_image_path):
    """Hide text file inside an image"""
    # Open image
    img = Image.open(image_path)
    img = img.convert("RGB")
    
    # Read the text file content
    with open(text_file_path, 'r') as file:
        text = file.read()
    
    # Convert text to binary
    binary_text = text_to_bin(text) + '1111111111111110'  # Add end-of-text marker
    
    # Ensure the image has enough pixels to hide the data
    pixels = img.load()
    width, height = img.size
    data_index = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Modify the LSB of each color channel
            if data_index < len(binary_text):
                r = r & 0xFE | int(binary_text[data_index])  # Modify LSB of red
                data_index += 1
            if data_index < len(binary_text):
                g = g & 0xFE | int(binary_text[data_index])  # Modify LSB of green
                data_index += 1
            if data_index < len(binary_text):
                b = b & 0xFE | int(binary_text[data_index])  # Modify LSB of blue
                data_index += 1
                
            pixels[x, y] = (r, g, b)

            # Break early if all data has been hidden
            if data_index >= len(binary_text):
                break
        else:
            continue
        break
    
    # Save the new image with hidden data
    img.save(output_image_path)
    print(f"Text successfully hidden in image: {output_image_path}")


def bin_to_text(binary_data):
    """Convert binary to text"""
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])


def extract_text_from_image(image_path):
    """Extract hidden text from an image"""
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = img.load()
    
    binary_data = ''
    
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Extract the LSB of each color channel
            binary_data += str(r & 1)  # LSB of red
            binary_data += str(g & 1)  # LSB of green
            binary_data += str(b & 1)  # LSB of blue

    # Find the end-of-text marker
    end_marker = '1111111111111110'
    end_index = binary_data.find(end_marker)
    
    if end_index != -1:
        binary_data = binary_data[:end_index]
        text = bin_to_text(binary_data)
        return text
    else:
        return "No hidden text found."


# Example usage for hiding text and extracting text:

# 1. Hide Text in Image
image_path = "photo.jpg"
text_file_path = "secret.txt"
output_image_path = "image_with_hidden_text.png"
hide_text_in_image(image_path, text_file_path, output_image_path)

# 2. Extract Text from Image
output_text_file_path = "extracted_secret.txt"
hidden_text = extract_text_from_image(output_image_path)
if hidden_text:
    with open(output_text_file_path, 'w') as f:
        f.write(hidden_text)
    print(f"Extracted text saved to: {output_text_file_path}")
else:
    print("No hidden text found.")
