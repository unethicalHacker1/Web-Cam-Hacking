📹🔢 Camera Streaming Client with Calculator GUI
This project is a Python-based client application that performs real-time camera streaming to a server while also functioning as a simple calculator GUI using Tkinter.

🚀 Features
🎥 Live Camera Streaming: Captures webcam frames and sends them over TCP to a server.

🧮 Built-in Calculator: Perform basic arithmetic operations (+, –, ×, ÷).

🧵 Threaded Execution: Camera runs on a separate thread so the GUI remains responsive.

💬 User-Friendly Interface: Clean and simple GUI built with Tkinter.

🛠️ Technologies Used
Python 3

OpenCV (cv2) – for video capture and frame encoding

Sockets – for client-server communication

Pickle & Struct – for serialization of image frames

Tkinter – for the calculator GUI

📦 How to Run
Start the server (ensure it's listening on the same port and IP as set in client.py).

Run the client:

bash
Copy
Edit
python client.py
The GUI will launch with:

A calculator

A background camera stream that sends frames to the server

💡 Make sure your webcam is connected and accessible.

📝 File Overview
client.py: Main application combining camera streaming and calculator GUI

server: Expected to receive and process the video frames (not included here, but required)

📌 Note
Ensure your server IP and port in client.py are correctly set.

To stop the app, simply close the GUI – it will stop the camera stream gracefully.

🧑‍💻 Author
Developed by Soban Saeed
