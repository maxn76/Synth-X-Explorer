# Synth-X-Explorer
This software is used to create and edit patches on the Roland S-1 synthesizer

INSTALLATION:
- the rtmidi module must be installed.
pip install python-rtmidi
- not mandatory but recommended to install the digital-7.zip font, you can find it in the main page or search for it on Google.
unzip the .zip file
right click on each individual .ttf file
and select INSTALL from the menu
- the default.ptc file must be in main

USE:
Upon startup, the software automatically searches for and finds the Roland S-1 synthesizer.
Once found, it positions itself by default on bank 3-1 and loads the default patch. The 3-1 bank is temporarily overwritten.

Now you can adjust as many controllers as you want on the user interface or even on the synthesizer itself.
Moving the controllers on the synthesizer will also update those on the interface in real time.

SAVING PATCHES TO A FILE:
Click on SAVE AS then give a name

LOADING A PATCH FROM A FILE:
Make sure you have selected the right bank where you want to upload the file.
Click on LOAD

INITIALIZATION:
Go to the bank you want to initialize then click on INITIALIZE. the default.ptc patch will be loaded

MAKE DEFAULT:
by clicking on make default the current patch will automatically be saved as default.ptc and will be used as the default patch

PERMANENTLY SAVE A PATCH IN THE SYNTHESIZER
To make the bank permanent it is necessary
- hold down the SHIFT key + 16 WRITE key
- confirm with key 2 ENTER

ATTENTION:
- The digital-7 font released as freeware for personal use
- rtmidi released under the MIT license
- The user interface has been done using Pygubu. Pygubu is a RAD tool to enable quick and easy development of user interfaces for the Python's tkinter module
- The name Roland belongs to the Roland company

I AM NOT A PROFESSIONAL PROGRAMMER, I ONLY PROGRAM FOR PASSION AND FUN.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

A compiled version will be created with the pyinstaller tool


WORK IN PROGRESS
