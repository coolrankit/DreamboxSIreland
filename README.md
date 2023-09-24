# DreamboxSIreland
Enigma2 Plugin Extension for DreamboxSIreland

**Enigma2 Plugin Description:**
1. The plugin is developed in python 2.7.13
2. The plugin downloads zip file from http://dreamboxsireland.com/tv.zip and then gets all the containing files and replaces every instances of “$username” and “$password” by provided username and password respectively of the contents of those files.
3. The plugin then deletes every .tv file under ‘etc/enigma2 ‘ folder and copies the downloaded files in this directory along with changed contents. Any other files (except .tv) if exists are replaced. Then restarts the box.
4. The plugin is created based on the folder structure of:
/	usr/lib/enigma2/python/Plugins/Extensions/RegulusPlugin/<plugin files>
Where .tv files locates on:
/	etc/enigma2/<.tv files>
6. Please note: It needs read, write and delete permission on these files and folders, so make sure it has so.

**Installation and testing:**
1.	Please backup necessary files before installing the plugin
2.	Then install the plugin using provided .ipk file
3.	Check the folder structure of installed plugin is as mentioned above or not. And also it has necessary permissions or not.
4.	Run the plugin and check if the plugin is working as expected or not.
5.	Report and show me on teamviewer or skype if anything is problematic. As I do not have any access to any box, I couldn’t final test it.
