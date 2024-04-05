from PIL import Image

# Function to hide text message within an image using LSB method
def hide_message(image_path, output_path, message):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    message_length = len(binary_message)
    
    # Check if message can fit in the image
    if message_length > width * height * 3:
        raise ValueError("Message is too long to be hidden in the image.")
    
    # Add stopper to indicate end of message
    binary_message += '1111111111111110'  # Using 16 bits for end marker
    
    data_index = 0
    # Iterate over each pixel and modify LSB to hide message
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):  # For each color channel (RGB)
                if data_index < message_length:
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1
            img.putpixel((x, y), tuple(pixel))
            if data_index >= message_length:
                break
        if data_index >= message_length:
            break
    
    # Save the modified image
    img.save(output_path)
    print("Message hidden successfully.")

# Function to extract hidden message from an image using LSB method
def extract_message(image_path):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    
    binary_message = ''
    data_index = 0
    
    # Iterate over each pixel to extract LSBs
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):  # For each color channel (RGB)
                binary_message += str(pixel[i] & 1)
                data_index += 1
                # Check for end marker
                if data_index % 16 == 0 and data_index > 0:
                    if binary_message[-16:] == '1111111111111110':
                        return ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message)-16, 8))
    return None

# Function to handle encoding based on user input
def encode():
    image_path = input("Enter the image path: ")
    output_path = input("Enter the output image path: ")
    message = input("Enter the message to hide: ")
    hide_message(image_path, output_path, message)

# Function to handle decoding based on user input
def decode():
    image_path = input("Enter the image path: ")
    message = extract_message(image_path)
    if message:
        print("Extracted message:", message)
    else:
        print("No hidden message found in the image.")

# Function to handle user input using switch case
def steganography():
    while True:
        print("\nSteganography Menu")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            encode()
        elif choice == '2':
            decode()
        elif choice == '3':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Run the steganography function
steganography()
