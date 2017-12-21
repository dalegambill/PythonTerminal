12/19/2017, Dale Gambill
------------------------
I fixed some minor issues, such as requiring the COM port to be open if
the user selects to replay a log file.

8/31/2017, Dale Gambill
-----------------------
I have written serial data terminal programs in C, C++, and C#.  I wanted to
write one in Python 3.5 so I could compare the features of the languages.

I wrote terminal.py and serial_rs_tx.py on Windows 10.  Terminal uses the
the GUI module that comes with Python, tkinter.  Serial_rx_tx.py uses 
the serial.py, which comes with python.

The resulting Python program sends, receives, and displays data
simultaneously, as I would expect.