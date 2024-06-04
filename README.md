# Script-to-Pepper PythonAnimator

Joseph Conrow's HonorsThesis

## Setup

1. **Download Pycharm (requires JetBrains liscence)**    
When setting up the enviornment, I used Pycharm, and found that to be the easier and most straightforward IDE. It manages the python interpreters well (have not tried any other IDEs to compare, ei. VisualStudio).
3. **Download Program**     
This can be done by using "git clone ..." or by downloading the .zip.
5. **Open Project**     
Click "Open" in under the "File" header. Then select the downloaded folder named "PythonParser". Now we are good to run the program.

## How to Use





## FAQ

### Errors

1. **ModuleNotFoundError: No module named 'BLANK'**
If you get this error, likely there is an issue with your virtual enviornment. That is, a library got misplaced or the wrong Python interpreter was used. This can possible be caused when using a IDE that is not PyCharm (no support for such as of now). To fix it, try redownloading this program from the github page and try setting it up anew. 

2. **Process finished with exit code 137 (interrupted by signal 9:SIGKILL)**
This is caused most certainly due to an over usage of RAM during the processing of your script (mainly the TTS processing occurring). This can be minimized by closing other programs on the computer (especially browsers).
