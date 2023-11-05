# Peer-to-Peer File Transfer Project

## Overview
This project is a demonstration of a simple peer-to-peer file transfer system. It consists of a server component, a client component (both server and client-side), and a graphical user interface (GUI) for easy interaction with the client.

## Project Structure
1. **Server (server.py):** 
   - The server is the central component that needs to be started first. It handles the central server's functionalities and connects to a database (dtb) to manage user information.

2. **Client (client3.py):**
   - The client component is responsible for managing peer-to-peer file transfer.
   - The client has both server-side and client-side functionalities. You can run multiple clients simultaneously by adjusting the 'local_port' setting.

3. **GUI (signUpsignIn.py):**
   - The graphical user interface (GUI) offers an intuitive way to interact with the client component. It allows you to sign in, sign up, select a file path for sending files, choose a destination folder for storing received files, and perform actions such as fetching and publishing files.

## Getting Started
1. Start the central server:
   - Run the `server.py` script to start the central server. Ensure the server is running before proceeding with client actions.

2. Client Setup:
   - Edit the `local_port` setting in the `client.py` file to configure the port for each client. Ensure unique ports for different clients.

3. GUI Interaction:
   - Launch the GUI using the `signUpsignIn.py` script. You can use the GUI to sign in, sign up, and perform file transfer actions with ease.

## Usage
1. **Sign In/Sign Up:**
   - Use the GUI to sign in with your username and password or create a new account by signing up.

2. **Select File Path:**
   - After signing in, you can select the file path from which you want to make repository.

3. **Choose Publish Folder:**
   - Choose the destination folder where you want to a publish file in thier.

4. **Fetch and Publish:**
   - Use the GUI to fetch or publish files with ease.

## Notes
- The project demonstrates a simple peer-to-peer file transfer system.
- Please adjust the `local_port` for running multiple clients on different ports.

## Requirements
- Python 3
- Tkinter (for GUI)
- Additional Python libraries specified in `requirements.txt`.

## License

Feel free to customize and use this project for your file transfer needs. If you encounter any issues or have suggestions for improvements, please feel free to create an issue or contribute to the project.

Enjoy using the Peer-to-Peer File Transfer Project!
