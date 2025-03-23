# Text Hiding in Image (Steganography)

This project allows you to hide text inside an image using the Least Significant Bit (LSB) method of image steganography. The text is converted into binary and embedded into the image's pixel values, where the LSB of the image's color channels (RGB) is modified.

## Features:
- Hide text in an image.
- Extract hidden text from an image.
- Use the Least Significant Bit (LSB) method for text embedding.
- Easy-to-use functions for text-to-binary conversion and image manipulation.

## Requirements:
- Python 3.x
- Pillow (PIL) library for image processing

### Install the required libraries:
You can install the required dependencies using `pip`:

```bash
pip install pillow
```

## Usage
1. **Hide Text in Image:**
   To hide a text file inside an image:

   ```python
   image_path = "photo.jpg"            # Path to the image you want to hide text in
   text_file_path = "secret.txt"       # Path to the text file containing the message
   output_image_path = "image_with_hidden_text.png"  # Path where the image with hidden text will be saved

   hide_text_in_image(image_path, text_file_path, output_image_path)
   ```

2. **Extract Text from Image:**
   To extract the hidden text from an image:

   ```python
   image_path = "image_with_hidden_text.png"  # Path to the image with hidden text

   hidden_text = extract_text_from_image(image_path)
   print(hidden_text)
   ```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## About the project:
This project was created to demonstrate the basics of steganography by hiding text in images. It can be extended to include more advanced features, such as encryption, better error handling, and GUI support. Feel free to contribute or open an issue if you have any questions or need further assistance. pull requests are welcome.
