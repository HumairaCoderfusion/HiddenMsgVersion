document.addEventListener('DOMContentLoaded', () => {
    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show selected tab content
            tabContents.forEach(content => {
                content.classList.add('hidden');
                if (content.id === tabId) {
                    content.classList.remove('hidden');
                }
            });
        });
    });

    // Hide text functionality
    const hideBtn = document.getElementById('hide-btn');
    const imageInput = document.getElementById('image-input');
    const textInput = document.getElementById('text-input');
    const passwordInput = document.getElementById('password-input');
    const resultContainer = document.getElementById('result-container');
    const resultImage = document.getElementById('result-image');
    const downloadBtn = document.getElementById('download-btn');

    hideBtn.addEventListener('click', async () => {
        if (!imageInput.files[0] || !textInput.value || !passwordInput.value) {
            alert('Please fill in all fields');
            return;
        }

        const image = imageInput.files[0];
        const text = textInput.value;
        const password = passwordInput.value;

        try {
            // Create a canvas to manipulate the image
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Load the image
            const img = new Image();
            img.src = URL.createObjectURL(image);
            
            await new Promise((resolve) => {
                img.onload = resolve;
            });

            // Set canvas dimensions
            canvas.width = img.width;
            canvas.height = img.height;
            
            // Draw image on canvas
            ctx.drawImage(img, 0, 0);

            // Get image data
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;

            // Encrypt text
            const encryptedText = await encryptText(text, password);

            // Hide text in image using LSB
            hideTextInImage(data, encryptedText);

            // Update canvas with modified image data
            ctx.putImageData(imageData, 0, 0);

            // Convert canvas to blob
            canvas.toBlob((blob) => {
                const url = URL.createObjectURL(blob);
                resultImage.innerHTML = `<img src="${url}" alt="Result Image">`;
                downloadBtn.href = url;
                downloadBtn.download = 'hidden_image.png';
                resultContainer.classList.remove('hidden');
                downloadBtn.classList.remove('hidden');
            }, 'image/png');
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the image');
        }
    });

    // Extract text functionality
    const extractBtn = document.getElementById('extract-btn');
    const extractImageInput = document.getElementById('extract-image-input');
    const extractPasswordInput = document.getElementById('extract-password-input');
    const extractResult = document.getElementById('extract-result');
    const extractedText = document.getElementById('extracted-text');

    extractBtn.addEventListener('click', async () => {
        if (!extractImageInput.files[0] || !extractPasswordInput.value) {
            alert('Please fill in all fields');
            return;
        }

        const image = extractImageInput.files[0];
        const password = extractPasswordInput.value;

        try {
            // Create a canvas to read the image
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Load the image
            const img = new Image();
            img.src = URL.createObjectURL(image);
            
            await new Promise((resolve) => {
                img.onload = resolve;
            });

            // Set canvas dimensions
            canvas.width = img.width;
            canvas.height = img.height;
            
            // Draw image on canvas
            ctx.drawImage(img, 0, 0);

            // Get image data
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;

            // Extract text from image
            const encryptedText = extractTextFromImage(data);
            
            // Decrypt text
            const decryptedText = await decryptText(encryptedText, password);

            extractedText.textContent = decryptedText;
            extractResult.classList.remove('hidden');
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while extracting text from the image');
        }
    });

    // Helper functions
    async function encryptText(text, password) {
        // Simple encryption using XOR with password
        const encoder = new TextEncoder();
        const textBytes = encoder.encode(text);
        const passwordBytes = encoder.encode(password);
        
        const encryptedBytes = textBytes.map((byte, i) => 
            byte ^ passwordBytes[i % passwordBytes.length]
        );
        
        return btoa(String.fromCharCode(...encryptedBytes));
    }

    async function decryptText(encryptedText, password) {
        // Simple decryption using XOR with password
        const decoder = new TextDecoder();
        const encryptedBytes = new Uint8Array(
            atob(encryptedText)
                .split('')
                .map(c => c.charCodeAt(0))
        );
        const passwordBytes = new TextEncoder().encode(password);
        
        const decryptedBytes = encryptedBytes.map((byte, i) => 
            byte ^ passwordBytes[i % passwordBytes.length]
        );
        
        return decoder.decode(decryptedBytes);
    }

    function hideTextInImage(imageData, text) {
        const binaryText = textToBinary(text);
        let textIndex = 0;
        
        for (let i = 0; i < imageData.length; i += 4) {
            if (textIndex < binaryText.length) {
                // Modify the least significant bit of each color channel
                imageData[i] = (imageData[i] & 0xFE) | parseInt(binaryText[textIndex++]);
                if (textIndex < binaryText.length) {
                    imageData[i + 1] = (imageData[i + 1] & 0xFE) | parseInt(binaryText[textIndex++]);
                }
                if (textIndex < binaryText.length) {
                    imageData[i + 2] = (imageData[i + 2] & 0xFE) | parseInt(binaryText[textIndex++]);
                }
            } else {
                break;
            }
        }
    }

    function extractTextFromImage(imageData) {
        let binaryText = '';
        
        for (let i = 0; i < imageData.length; i += 4) {
            // Extract the least significant bit from each color channel
            binaryText += (imageData[i] & 1).toString();
            binaryText += (imageData[i + 1] & 1).toString();
            binaryText += (imageData[i + 2] & 1).toString();
        }
        
        return binaryToText(binaryText);
    }

    function textToBinary(text) {
        return text.split('').map(char => 
            char.charCodeAt(0).toString(2).padStart(8, '0')
        ).join('');
    }

    function binaryToText(binary) {
        const bytes = binary.match(/.{1,8}/g);
        return bytes ? bytes.map(byte => 
            String.fromCharCode(parseInt(byte, 2))
        ).join('') : '';
    }
}); 