from flask import Flask, render_template, request
import secrets

app = Flask(__name__)

# Dictionary to store encrypted messages
encrypted_messages = {}

# Encryption and decryption functions


def caesar_cipher(text, shift):
    # Implement Caesar cipher logic
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            decrypted_text += chr(shifted)
        else:
            decrypted_text += char
    return decrypted_text


def rot13_cipher(text):
    # Implement ROT13 cipher logic
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                decrypted_text += chr((ord(char) - ord('a') - 13) %
                                      26 + ord('a'))
            elif char.isupper():
                decrypted_text += chr((ord(char) - ord('A') - 13) %
                                      26 + ord('A'))
        else:
            decrypted_text += char
    return decrypted_text


def generate_decryption_key():
    return secrets.token_hex(16)  # Generate a random decryption key

# Routes


@app.route('/', methods=['GET', 'POST'])
def index():
    decrypted_message = None
    if request.method == 'POST':
        # Check if the message field is present (encryption)
        if 'message' in request.form:
            message = request.form['message']
            cipher = request.form['cipher']

            encrypted_text = ''
            decryption_key = ''

            if cipher == 'Caesar':
                # Get the shift value from the form
                shift = int(request.form.get('shift', 0))
                # Encrypt the message using Caesar cipher
                encrypted_text = caesar_cipher(message, shift)
                decryption_key = generate_decryption_key()  # Generate decryption key
                # Store the original shift value with the encrypted message
                encrypted_messages[message] = {
                    'encrypted_text': encrypted_text, 'cipher': cipher, 'shift': shift, 'decryption_key': decryption_key}
            elif cipher == 'ROT13':
                # Encrypt the message using ROT13 cipher
                encrypted_text = rot13_cipher(message)
                decryption_key = generate_decryption_key()  # Generate decryption key
                # Store encrypted message and decryption key in the dictionary
                encrypted_messages[message] = {
                    'encrypted_text': encrypted_text, 'cipher': cipher, 'decryption_key': decryption_key}

            return render_template('index.html', encrypted_text=encrypted_text, decryption_key=decryption_key, encrypted_messages=encrypted_messages)

        # Check if the decryption key field is present (decryption)
        elif 'decryption_key' in request.form:
            decryption_key = request.form['decryption_key']
            for message, data in encrypted_messages.items():
                if data['decryption_key'] == decryption_key:
                    if data['cipher'] == 'Caesar':
                        # Retrieve the original shift value for decryption
                        original_shift = data['shift']
                        # Calculate the shift value for decryption
                        shift_for_decryption = 26 - original_shift
                        decrypted_message = caesar_cipher(
                            data['encrypted_text'], shift_for_decryption)
                    elif data['cipher'] == 'ROT13':
                        decrypted_message = rot13_cipher(
                            data['encrypted_text'])
                    break

    return render_template('index.html', encrypted_messages=encrypted_messages, decrypted_message=decrypted_message)


if __name__ == "__main__":
    app.run(debug=True)
