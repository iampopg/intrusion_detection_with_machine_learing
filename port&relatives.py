import socket
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from code import IntrusionDetectionClassifier
from PIL import Image, ImageTk
import time

class PortScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('20d/47cs/01255')
        self.geometry("450x600")
        self.configure(bg='black')
        # self.toplink = Canvas(self.vpn_gui, width=375, height=450)
        # self.toplink.pack(side = "top", expand = YES, fill = BOTH)
        
        self.create_frames()
        self.create_buttons()
        self.create_scan_frame()
        self.create_general_frame()
        self.create_about_frame()
        
        self.display_home()
        
    def create_frames(self):
        self.button_frame = tk.LabelFrame(self, width=450, height=50, bg='black')
        self.button_frame.pack(side=tk.BOTTOM)

        self.scan_frame = tk.LabelFrame(self, text='Port Scanner', width=450, height=500, bg='black', fg='white')
        self.scan_frame.pack(pady=50)

        self.general_frame = tk.LabelFrame(self, text='General Page', width=450, height=500, bg='black', fg='white')
        self.about_frame = tk.LabelFrame(self, text='About Page', width=450, height=500, bg='black', fg='white')
        
    def create_buttons(self):
        self.home_button = ttk.Button(self.button_frame, text='Home', command=self.display_home)
        self.home_button.grid(row=0, column=0)

        self.general_button = ttk.Button(self.button_frame, text='General', command=self.display_general)
        self.general_button.grid(row=0, column=1)

        self.about_button = ttk.Button(self.button_frame, text='About', command=self.display_about)
        self.about_button.grid(row=0, column=2)
        
    def create_scan_frame(self):
        start_port_label = tk.Label(self.scan_frame, text='Start Port:', bg='black', fg='white')
        start_port_label.grid(row=0, column=0, padx=10, pady=10)
        self.start_port_entry = tk.Entry(self.scan_frame)
        self.start_port_entry.grid(row=0, column=1, padx=10, pady=10)

        end_port_label = tk.Label(self.scan_frame, text='End Port:', bg='black', fg='white')
        end_port_label.grid(row=1, column=0, padx=10, pady=10)
        self.end_port_entry = tk.Entry(self.scan_frame)
        self.end_port_entry.grid(row=1, column=1, padx=10, pady=10)

        scan_button = tk.Button(self.scan_frame, text='Scan Ports', command=self.scan_ports)
        scan_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.result_text = tk.Text(self.scan_frame, width=40, height=10, bg='black', fg='white')
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_general_frame(self):
        self.general_frame.pack()

        general_button = tk.Button(self.general_frame, text='SCAN FOR INTRUSION', font=('Verdana', 16), bg='black', fg='white', command=self.general_button_click)
        general_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def general_button_click(self):
        # Add code here to handle the button click action
        self.toplink = Canvas(width=375, height=450)
        self.toplink.pack(side = "top", expand = YES, fill = BOTH)
        
        self.progress_bar = ttk.Progressbar(self.toplink, orient = 'horizontal', mode = 'determinate', length = 280)
        self.progress_bar.place(height=30, width=300, x=40, y=130)
        self.progress_bar.start()
        time.sleep(2)
        
        train_file = "train.csv"
        test_file = "test.csv"
        intrusion_detection = IntrusionDetectionClassifier(train_file, test_file)
        intrusion_detection.explore_data()
        intrusion_detection.plot_class_distribution()
        intrusion_detection.clean_data()
        intrusion_detection.feature_selection()
        intrusion_detection.train_and_evaluate_model()
        intrusion_detection.predict_test_data()
        # print("General button clicked!")

    def create_about_frame(self):
        about_text = '''The intrusion detection systems are 
    an integral part of modern communication networks. The business environments require a high level of security to safeguard their private data from any unauthorized personnel. The current intrusion detection systems are a step upgrade from the conventional anti-virus software. Two main categories based on their working. These are:
    • Network Intrusion Detection Systems (NIDS): These systems continuously monitor the network traffic and analyze the packets for a possible rule infringement.
    • Host-based Intrusion Detection Systems (HIDS): These systems monitor the operating system files of an end-user system to detect malicious software that might temper with its normal functioning.
    
    for more details, visit: www.github.com/iampopg/intrusion_detection_with_machine_learing'''

        self.about_text_widget = tk.Text(self.about_frame, bg='black', fg='white', wrap='word', font=('Verdana', 12))
        self.about_text_widget.insert(tk.END, about_text)
        self.about_text_widget.pack(pady=50, padx=50)

    def is_port_open(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Adjust the timeout value as needed
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0

    def scan_ports(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        start_port = int(self.start_port_entry.get())
        end_port = int(self.end_port_entry.get())

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Scanning ports {start_port}-{end_port} on {ip_address}...\n")

        for port in range(start_port, end_port + 1):
            if self.is_port_open(ip_address, port):
                self.result_text.insert(tk.END, f"Port {port} is open on {ip_address}\n")

        self.result_text.insert(tk.END, "Scan completed.")
        
    def display_home(self):
        self.button_frame.config(bg='black')
        self.scan_frame.pack()
        self.general_frame.pack_forget()
        self.about_frame.pack_forget()

    def display_general(self):
        self.button_frame.config(bg='black')
        self.scan_frame.pack_forget()
        self.general_frame.pack()
        self.about_frame.pack_forget()

    def display_about(self):
        self.button_frame.config(bg='black')
        self.scan_frame.pack_forget()
        self.general_frame.pack_forget()
        self.about_frame.pack()

if __name__ == "__main__":
    app = PortScannerApp()
    app.mainloop()
