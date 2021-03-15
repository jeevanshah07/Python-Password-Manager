"""
from PyQt5.QtWidgets import *
app = QApplication([])
button = QPushButton('Click')
def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec_()

button.clicked.connect(on_button_clicked)
button.show()
app.exec_()
"""

from cryptography.fernet import Fernet
key = Fernet.generate_key()

file = open('key.key', 'wb')  # Open the file as wb to write bytes
file.write(key)  # The key is type bytes still
file.close()

file = open('key.key', 'rb')  # Open the file as wb to read bytes
key = file.read()  # The key will be type bytes
file.close()

message = "my deep dark secret".encode()

f = Fernet(key)
encrypted = f.encrypt(message)  # Encrypt the bytes. The returning object is of type bytes

print(encrypted)

f = Fernet(key)
decrypted = f.decrypt(encrypted)  # Decrypt the bytes. The returning object is of type bytes
print(decrypted)