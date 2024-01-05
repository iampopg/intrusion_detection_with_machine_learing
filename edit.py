
# Import all the required libraries
from tkinter import *
import tkinter.ttk as ttk, random, socket
import requests, os, sys, tempfile, subprocess, base64, time, threading,sys, os, PIL.Image
# import mysql.connector as sql
from PIL import ImageTk
import socket, urllib.request

class OpenVPNClient():
    def __init__(self):
        # if not pyuac.isUserAdmin():
        #     pyuac.runAsAdmin()
        self.vpn_gui = Tk()
        self.vpn_gui.title('iampogg')
        # self.vpn_gui.iconbitmap(self.resource_path('favicon.ico'))
        self.vpn_gui.resizable(False,False)
        self.vpn_gui.geometry('375x450')
        # self.vpn_gui.winfo_rgb("(43,84,126)")
        
        self.toplink = Canvas(self.vpn_gui, width=375, height=450)
        self.toplink.pack(side = "top", expand = YES, fill = BOTH)
        
        self.entryPage()
        # self.winner = ''
        # self.servers = []
        # self.serv_list = []
        self.start_configuration()
        self.vpn_gui.mainloop()
    
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    def entryPage(self):
        self.toplink.destroy()
       
        self.toplink = Canvas(self.vpn_gui, width=375, height=450)
       
        self.toplink.pack(side = "top", expand = YES, fill = BOTH)

        self.info = Label(self.toplink, text="Intrusion Detection BY PopG", bg="skyblue", foreground="white", font=18)
        self.info.place(height=50, width=300, x=40, y=180)
        
    def setBackground(self):
        self.toplink.destroy()
        self.toplink = Frame(self.vpn_gui, bg="#2B547E")
        self.toplink.pack(side = "top", expand = YES, fill = BOTH)
        
        # self.open_image = (PIL.Image.open(self.resource_path('logo.jpg')))
        resized= self.open_image.resize((100, 50))
        image = ImageTk.PhotoImage(resized)
        self.toplogo = Canvas(self.toplink, width=20, height=20, bg="#2B547E", border=False)
        self.toplogo.image = image
        self.toplogo.create_image(5,5,anchor=NW,image=image)
        self.toplogo.place(height=50, width=100, x=150, y=10)
        
        self.info = Label(self.toplink, text='', bg="#2B547E", foreground="white", font=18)
        self.info.place(height=50, width=330, x=20, y=70)
        
        self.toplogin = Frame(self.toplink, bg="#2B547E")
        self.toplogin.place(height=350, width=365, x=5, y=130)
        
        
    def start_configuration(self):
        # self.configThread = threading.Thread(target=self.install_and_config, name='progress_bar', daemon=True)
        # self.configThread.start()
        # if self.configThread.is_alive():
        self.progressbar_start()
       
    def progressbar_start(self):
        """ starts the progress bar """
            
        self.progress_bar = ttk.Progressbar(self.toplink, orient = 'horizontal', mode = 'determinate', length = 280)
        self.progress_bar.place(height=30, width=300, x=40, y=130)
        self.progress_bar.start()

    def progressbar_stop(self):
        """ stops the progress bar """
        self.progress_bar.stop()
        self.progress_bar.destroy()  
       
       
if __name__ == "__main__":
    openVPN = OpenVPNClient()
