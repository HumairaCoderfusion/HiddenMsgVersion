# Image Steganography (LSB Technique with AES Encryption)

## 📄 Description

This project allows you to hide text within an image using the Least Significant Bit (LSB) method. It also integrates AES encryption to secure the text before embedding it inside the image. Here's the process:

1. **Encryption**: The text is encrypted using AES with a password.
2. **Conversion**: The encrypted text is then converted into binary form.
3. **Embedding**: The binary data is embedded in the least significant bits of the RGB channels of the image.
4. **Extraction**: The encrypted text is extracted from the image using the LSB method and decrypted with the password.

## 🛠️ Dependencies

- `cryptography`: AES encryption library. Install it using:
  ```bash
  pip install cryptography
  ```
- `Pillow`: Python Imaging Library (PIL) for working with images. Install it using:
  ```bash
  pip install pillow
  ```

## 🔑 Key Functions

1. **generate_key(password)**: Generates a key from the provided password.
2. **encrypt_text(text, password)**: Encrypts the given text using AES encryption.
3. **decrypt_text(encrypted_text, password)**: Decrypts the encrypted text using the AES key generated from the password.
4. **text_to_bin(text)**: Converts the input text into its binary representation.
5. **bin_to_text(binary_data)**: Converts a binary string back to readable text.
6. **hide_text_in_image(image_path, text, output_image_path, password)**: Hides the encrypted text within the image.
7. **extract_text_from_image(image_path, password)**: Extracts and decrypts the hidden text from the image.

## 🔒 Encryption and Steganography Workflow

1. **Encrypt the text**: The input text is encrypted using the AES algorithm with a password.
2. **Convert to binary**: The encrypted text is then converted into a binary form for LSB embedding.
3. **Embed the binary data in an image**: The binary data is embedded into the image's least significant bits of the RGB color channels.
4. **Extract the binary data**: The encrypted binary data is extracted using the same password.
5. **Decrypt the binary data**: Finally, the encrypted text is decrypted back to its original form.

## 🖼️ Example Usage

```python
image_path = "photo.jpg"
text = "just some initial text to hide in the image."
output_image_path = "hidden_image.png"
password = "konopasswordlagena"

# Hide the text
hide_text_in_image(image_path, text, output_image_path, password)

# Extract the text
extracted_text = extract_text_from_image(output_image_path, password)
print("Extracted Text:", extracted_text)
```

## 📝 Output

- The `hide_text_in_image()` function embeds the encrypted text into the image and saves it as `output_image_path`.
- The `extract_text_from_image()` function retrieves and decrypts the hidden text from the image, provided the correct password.

---

## 📜 License

This project is open-source under the MIT License. Feel free to modify and distribute it as needed.

---

### 👤 Author: Nibir  
GitHub: [NibirMahmud](https://www.github.com/mahmudnibir)  
Date: 2025-03-24
