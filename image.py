from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import numpy as np
from PIL import Image
import os

def pad(data):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    return padder.update(data) + padder.finalize()

def unpad(data):
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(data) + unpadder.finalize()

def encrypt_image(image_path, key, iv):
    # Load and process the image
    image = Image.open(image_path)
    image = image.convert("RGB")
    image_array = np.array(image)
    flat_image_data = image_array.tobytes()

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Encrypt the image data
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(pad(flat_image_data)) + encryptor.finalize()

    return encrypted_data, image.size, image.mode

def decrypt_image(encrypted_data, key, iv, image_size, image_mode):
    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Decrypt the image data
    decryptor = cipher.decryptor()
    decrypted_data = unpad(decryptor.update(encrypted_data) + decryptor.finalize())

    # Convert decrypted data back to image
    decrypted_image_array = np.frombuffer(decrypted_data, dtype=np.uint8).reshape(image_size[1], image_size[0], -1)
    decrypted_image = Image.fromarray(decrypted_image_array, image_mode)

    return decrypted_image

# Example usage
key = os.urandom(32)  # AES-256 key
iv = os.urandom(16)   # AES block size is 16 bytes

encrypted_data, size, mode = encrypt_image('D:\\program\\task3\\imageencription.jpg.webp', key, iv)
decrypted_image = decrypt_image(encrypted_data, key, iv, size, mode)
decrypted_image.save('decrypted_image.jpg')
