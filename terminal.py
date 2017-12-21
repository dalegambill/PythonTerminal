#
# Serial COM Port terminal program
# 8/17/2017, Dale Gambill
# I wrote 2 modules for this program: terminal.py and serial_rx_tx.py.
#
import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext
from tkinter import *
from tkinter import filedialog
import serial_rx_tx
import _thread
import time
import webbrowser
from tkinter import messagebox

# globals
serialPort = serial_rx_tx.SerialPort()
logFile = None

root = tk.Tk() # create a Tk root window
root.title( "TERMINAL - Serial Data Terminal v1.01" )
# set up the window size and position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width/2
window_height = screen_width/3
window_position_x = screen_width/2 - window_width/2
window_position_y = screen_height/2 - window_height/2
root.geometry('%dx%d+%d+%d' % (window_width, window_height, window_position_x, window_position_y))

# scrolled text box used to display the serial data
frame = tk.Frame(root, bg='cyan')
frame.pack(side="bottom", fill='both', expand='no')
textbox = tkscrolledtext.ScrolledText(master=frame, wrap='word', width=180, height=28) #width=characters, height=lines
textbox.pack(side='bottom', fill='y', expand=True, padx=0, pady=0)
textbox.config(font="bold")

#COM Port label
label_comport = Label(root,width=10,height=2,text="COM Port:")
label_comport.place(x=10,y=26)
label_comport.config(font="bold")

#COM Port entry box
comport_edit = Entry(root,width=10)
comport_edit.place(x=100,y=36)
comport_edit.config(font="bold")
comport_edit.insert(END,"COM2")

# serial data callback function
def OnReceiveSerialData(message):
    str_message = message.decode("utf-8")
    textbox.insert('1.0', str_message)

# Register the callback above with the serial port object
serialPort.RegisterReceiveCallback(OnReceiveSerialData)

def sdterm_main():
    root.after(200, sdterm_main)  # run the main loop once each 200 ms

#
#  commands associated with button presses
#
def OpenCommand():
    if button_openclose.cget("text") == 'Open COM Port':
        comport = comport_edit.get()
        baudrate = baudrate_edit.get()
        serialPort.Open(comport,baudrate)
        button_openclose.config(text='Close COM Port')
        textbox.insert('1.0', "COM Port Opened\r\n")
    elif button_openclose.cget("text") == 'Close COM Port':
        if button_replaylog.cget('text') == 'Stop Replay Log':
            textbox.insert('1.0',"Stop Log Replay first\r\n")
        else:
            serialPort.Close()
            button_openclose.config(text='Open COM Port')
            textbox.insert('1.0',"COM Port Closed\r\n")


def ClearDataCommand():
    textbox.delete('1.0',END)

def SendDataCommand():
    message = senddata_edit.get()
    if serialPort.IsOpen():
        message += '\r\n'
        serialPort.Send(message)
        textbox.insert('1.0',message)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")

def ReplayLogFile():
    try:
      if logFile != None:
        readline = logFile.readline()
        global serialPort
        serialPort.Send(readline)
    except:
      print("Exception in ReplayLogFile()")

def ReplayLogThread():
    while True:
        time.sleep(1.0)
        global logFile
        if serialPort.IsOpen():
            if logFile != None:
                ReplayLogFile()

def OpenLogFile():
    if not serialPort.IsOpen():
        textbox.insert('1.0', "Open COM port first\r\n")
    else:
        if button_replaylog.cget('text') == 'Replay Log':
            try:
                root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                           filetypes=(("log files", "*.log"), ("all files", "*.*")))
                global logFile
                logFile = open(root.filename,'r')
                _thread.start_new_thread(ReplayLogThread, ())
                button_replaylog.config(text='Stop Log Replay')
                textbox.insert('1.0', "Sending to open COM port from: " + root.filename + "\r\n")
            except:
                textbox.insert('1.0', "Could not open log file\r\n")
        else:
            button_replaylog.config(text='Replay Log')
            textbox.insert('1.0', "Stopped sending messages to open COM port\r\n")
            logFile = None


def DisplayAbout():
    tk.messagebox.showinfo(
    "About",
    "Written by Dale Gambill (same as 'Software Guy For You' on Youtube)\r\n\r\n" 
    "SDTERM demonstrates event-handling of serial COM port data as follows:\r\n\r\n" 
    "1 - getting messages from a COM port via a callback function\r\n" 
    "2 - sending messages from a file to the COM port, one at a time\r\n" 
    "3 - sending log file messages and receiving messages at the same time\r\n\r\n" 
    "Source code at: Github URL: https://github.com/dalegambill/PythonTerminal\r\n")

def TutorialsWebPage():
    webbrowser.open("https://www.youtube.com/channel/UCouhHzMMU9c-Qh-TkZl5GDg",
                    new=1, autoraise=True)

# COM Port open/close button
button_openclose = Button(root,text="Open COM Port",width=20,command=OpenCommand)
button_openclose.config(font="bold")
button_openclose.place(x=210,y=30)

#Clear Rx Data button
button_cleardata = Button(root,text="Clear Rx Data",width=20,command=ClearDataCommand)
button_cleardata.config(font="bold")
button_cleardata.place(x=210,y=72)

#Send Message button
button_senddata = Button(root,text="Send Message",width=20,command=SendDataCommand)
button_senddata.config(font="bold")
button_senddata.place(x=420,y=72)

#Replay Log button
button_replaylog = Button(root,text="Replay Log",width=20,command=OpenLogFile)
button_replaylog.config(font="bold")
button_replaylog.place(x=420,y=30)

#About button
button_about = Button(root,text="About",width=16,command=DisplayAbout)
button_about.config(font="bold")
button_about.place(x=620,y=30)

#Tutorials
button_tutorials = Button(root,text="Tutorials",width=16,command=TutorialsWebPage)
button_tutorials.config(font="bold")
button_tutorials.place(x=780,y=30)

#
# data entry labels and entry boxes
#

#Send Data entry box
senddata_edit = Entry(root,width=34)
senddata_edit.place(x=620,y=78)
senddata_edit.config(font="bold")
senddata_edit.insert(END,"Message")

#Baud Rate label
label_baud = Label(root,width=10,height=2,text="Baud Rate:")
label_baud.place(x=10,y=70)
label_baud.config(font="bold")

#Baud Rate entry box
baudrate_edit = Entry(root,width=10)
baudrate_edit.place(x=100,y=80)
baudrate_edit.config(font="bold")
baudrate_edit.insert(END,"38400")

#
# The main loop
#
root.after(200, sdterm_main)
root.mainloop()
#


