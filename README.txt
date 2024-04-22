README.txt
Preparation
	Python3: 3.12.2
	Used build-in library: socket, threading, os, datetime
	Compile, run and test

Make sure the abovementioned Preparation is fulfilled.
============================================================
Open a terminal (cmd), change directory to this folder, then type the following command: 
	python httpServer.py

The server is running at http://127.0.0.1:8080/index.html on your localhost, please use your browser to visit http://127.0.0.1:8080/index.html.

After the "HTTP Server Test Page" is displayed in the browser, please following the instructions on the webpage to test server's functions:
(1)	click the links image.html, audio.html and video.html to test text & image file, audio file and video file respectively.
(2)	click the button below the links to test HEAD request and show received header fields
 
(3)(4) Click the buttons for 400 Bad Request/404 Not Found. Both of them will first be printed out and then a .html file is opened, reminding you of possible problems.
(5)	Click the button for 5 to test 304 Not Modified Response and Last-Modified header fields.
 
Received requests and corresponding responses will be printed in the terminal (cmd) and logged into log.txt.

You may also open browser's console by press F12 (fn+F12) to view the responses.

Press Control+C in the terminal (cmd) to shut down the server and exit the program.
=============================================
To Test the handling of HTTP persistent connection:
First, open the terminal, find the directory that httpServer.py and keepAliveTest.py are in. input the command:
	python httpServer.py

Then, open a new terminal, repeat the steps and input the command:
	python keepAliveTest.py

In the terminal running keepAliveTest.py, input 1 for keep-alive test; input 2 for close test, press 0 to exit. If you input other values, the connection will be closed.

You can see the requests sent and the responses received in the terminal. They will also be logged into log.txt.
