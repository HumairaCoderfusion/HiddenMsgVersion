# Image Steganography Web Tool

A web-based tool for hiding and extracting text messages within images using the Least Significant Bit (LSB) steganography technique.

## Features

- Hide text messages within images
- Extract hidden text from images
- Password protection for hidden messages
- Modern and responsive web interface
- Works entirely in the browser (no server required)

## How to Use

1. **Hide Text in Image**
   - Click on the "Hide Text" tab
   - Select an image file
   - Enter the text you want to hide
   - Set a password for encryption
   - Click "Hide Text"
   - Download the resulting image

2. **Extract Text from Image**
   - Click on the "Extract Text" tab
   - Select an image containing hidden text
   - Enter the password used to hide the text
   - Click "Extract Text"
   - View the extracted message

## Technical Details

- Uses LSB (Least Significant Bit) steganography
- Implements XOR-based encryption for message security
- Works with PNG and JPEG images
- All processing is done client-side in the browser

## Hosting on GitHub Pages

1. Create a new repository on GitHub
2. Push these files to your repository
3. Go to repository Settings > Pages
4. Select the main branch as the source
5. Your web tool will be available at `https://HumairaCoderfusion.github.io/HiddenMsgVersion`

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Security Notes

- The encryption used is a simple XOR-based method and should not be used for highly sensitive data
- Always use strong passwords
- The tool works entirely in your browser - no data is sent to any server

## License

This project is open source and available under the MIT License.

---

## 📜 License

This project is open-source under the MIT License. Feel free to modify and distribute it as needed.

---

### 👤 Author: Nibir  
GitHub: [Humaira](https://www.github.com/HumairaCoderfusion)  
Date: 2025-03-24
