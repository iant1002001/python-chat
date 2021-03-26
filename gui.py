import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import client
from threading import Thread

IP = '127.0.0.1'
PORT = 3000


class Gui:

    index = "1.0"

    def __init__(self):

        # Get a username before launching the main chat application
        username_popup = tkinter.Tk()
        username_popup.withdraw()

        self.username = simpledialog.askstring(
            "Username",
            "Please enter a username",
            parent=username_popup
        )
        # Connect to the server and assign the username entered above
        if not client.connect(IP, PORT, self.username, show_error):
            return

        # Start the GUI
        Thread(target=self.loop).start()
        # Start listening for messages from the server
        client.start_listening(self.receive_message, show_error)

    def loop(self):
        # Create the main window for the GUI
        self.window = tkinter.Tk()
        self.window.configure(bg="gray")
        # Create a label for the chat history
        self.chat_label = tkinter.Label(
            self.window, text="Chat History", bg="gray")
        self.chat_label.configure(font=("Arial", 12))
        self.chat_label.pack(padx=50, pady=5)
        # Create a scrollable area for the chat history
        self.text_area = tkinter.scrolledtext.ScrolledText(self.window)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.configure(state='disabled')
        # Prompt the user to enter a message with a label
        self.message_label = tkinter.Label(
            self.window, text="Enter a message:", bg="gray")
        self.message_label.configure(font=("Arial", 12))
        self.message_label.pack(padx=50, pady=5)
        # Create a text input area
        self.input_area = tkinter.Text(self.window, height=3)
        self.input_area.pack(padx=20, pady=5)
        # Set focus to text input after the program launches
        self.input_area.focus_force()
        # Create a button to send messages
        self.send_button = tkinter.Button(
            self.window, text="Send", command=self.send_message)
        self.send_button.configure(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        # Binding keys to specific functions. Return sends messages,
        # escape exits the program.
        self.window.bind('<Return>', self.send_message)
        self.window.bind('<Escape>', self.stop)
        # Allows the user to click to close the program
        self.window.protocol("WM_DELETE_WINDOW", self.stop_click)
        # Start the GUI loop
        self.window.mainloop()

    # Displaying messages and sending them over the client socket
    def send_message(self, event):
        # This line gets the message from the text input area.
        message = self.input_area.get('1.0', 'end')
        client.send(message)
        self.input_area.delete('1.0', 'end')
        self.text_area.configure(state='normal')
        self.text_area.insert('end', f"{self.username}: {message}")
        # Assign a text color to the current user
        self.text_area.tag_add("blue", str(self.index),
                f"{str(self.index).rstrip('0') + str(len(self.username))}")
        self.text_area.tag_config("blue", foreground="blue")
        self.index = float(self.index) + 2
        self.text_area.yview('end')
        self.text_area.configure(state='disabled')

    # Displaying messages received over the client socket
    def receive_message(self, username, message):
        self.text_area.configure(state='normal')
        self.text_area.insert('end', f"{username}: {message}")
        # Assign a different text color for other users
        self.text_area.tag_add("red", str(self.index),
                f"{str(self.index).rstrip('0') + str(len(username))}")
        self.text_area.tag_config("red", foreground="red")
        self.index = float(self.index) + 2
        self.text_area.yview('end')
        self.text_area.configure(state='disabled')

    # Exit when pressing escape
    def stop(self, event):
        self.window.destroy()
        client.client_socket.close()
        exit(0)

    # Exit on click
    def stop_click(self):
        self.window.destroy()
        client.client_socket.close()
        exit(0)

# Display error messages
def show_error(message):
    print(f"Error: {message}")


# Launch the GUI
Gui()
