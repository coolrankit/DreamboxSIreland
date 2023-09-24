import os
import glob
import urllib2
import zipfile
from Plugins.Plugin import PluginDescriptor
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.Input import Input
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Console import Console
from Screens.VirtualKeyBoard import VirtualKeyBoard

class DreamboxSIrelandUpdater(Screen):
	skin = """
		<screen position="130,150" size="460,300" title="Dreambox S Ireland Updater" >
			<widget name="dsiuTextR1" position="10,10" size="440,30" font="Regular;20" scrollbarMode="showOnDemand"/>
			<widget name="dsiuMenuR" position="10,50" size="440,200" font="Regular;20" scrollbarMode="showOnDemand"/>
			<widget name="dsiuTextR2" position="10,260" size="440,30" font="Regular;15" scrollbarMode="showOnDemand"/>
		</screen>"""
	
	def __init__(self, session, args = None):
		self.session = session
		self.rusr = ""
		self.rpwd = ""
		self.fileDir = os.path.dirname(os.path.realpath('__file__'))
		self.url = "http://dreamboxsireland.com/tv.zip"
		self.zip = "/tv.zip"
		self.text = "No username and password captured. Please Enter them before update."
		
		list = []
		list.append(("Input Username", "opt_one"))
		list.append(("Input Password", "opt_two"))
		list.append(("Download Feeds", "opt_three"))
		list.append(("Update Feeds", "opt_four"))
		list.append(("Reboot", "opt_five"))
		list.append((_("Exit"), "opt_exit"))
		Screen.__init__(self, session)
		
		self["dsiuTextR1"] = Label(_("Press OK button to select:"))
		self["dsiuTextR2"] = Label()
		self["dsiuMenuR"] = MenuList(list)
		self["dsiuActionMapR"] = ActionMap(["SetupActions"],
		{
			"ok": self.go,
			"cancel": self.cancel
		}, -1)
		self.onShown.append(self.setMyText)

	def go(self):
		returnValue = self["dsiuMenuR"].l.getCurrentSelection()[1]
		if returnValue is not None:
			if returnValue is "opt_one":
				self.session.openWithCallback(self.askForRusr, VirtualKeyBoard, title=_("Username:"))
				
			if returnValue is "opt_two":
				self.session.openWithCallback(self.askForRpwd, VirtualKeyBoard, title=_("Password:"))
				
			if returnValue is "opt_three":
				self.downloadzip()
				
			if returnValue is "opt_four":
				self.updatefeed()
				
			if returnValue is "opt_five":
				self.bootthebox()
				
			if returnValue is "opt_exit":
				self.cancel()

	
	def askForRusr(self, rusr):
		self.rusr = rusr
		if rusr is None:
			self["dsiuTextR2"].setText("Username is not captured.")
		else:
			self["dsiuTextR2"].setText("Username captured.")
	def askForRpwd(self, rpwd):
		self.rpwd = rpwd
		if rpwd is None:
			self["dsiuTextR2"].setText("Password is not captured.")
		else:
			self["dsiuTextR2"].setText("Password captured.")

	def downloadzip(self):
		path = os.path.join(self.fileDir, self.zip)
		path = os.path.abspath(os.path.realpath(path))
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive'}

		req = urllib2.Request(self.url, headers=hdr)

		try:
			page = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print e.fp.read()
			self["dsiuTextR2"].setText(e.fp.read())

		data = page.read()
		ofile = open(path, 'wb')
		ofile.write(data)
		ofile.close()
		self["dsiuTextR2"].setText("Feeds Downloaded.")
	def updatefeed(self):
		path = os.path.join(self.fileDir, '/etc/enigma2/*.tv')
		path = os.path.abspath(os.path.realpath(path))
		path1 = os.path.join(self.fileDir, '/etc/enigma2')
		path1 = os.path.abspath(os.path.realpath(path1))
		path2 = os.path.join(self.fileDir, self.zip)
		path2 = os.path.abspath(os.path.realpath(path2))
		
		if (os.path.isfile(path2) and os.path.exists(path1)):
			ls =  glob.glob(path)
			for l in ls:
				os.remove(l)
			
			zp = zipfile.ZipFile(path2)
			ls = zp.namelist()
			for l in ls:
				tx = zp.read(l)
				tx = tx.replace('$username', self.rusr)
				tx = tx.replace('$password', self.rpwd)
				filename = os.path.join(self.fileDir, '/etc/enigma2/'+l)
				filename = os.path.abspath(os.path.realpath(filename))
				ofile = open(filename, 'w')
				ofile.write(tx)
				ofile.close()
				os.chmod(filename, 0o777)
		
			zp.close()
			os.remove(path2)
			self["dsiuTextR2"].setText("Feeds Updated.")
		else:
			if os.path.isfile(path2):
				self["dsiuTextR2"].setText("Incompatible version. Feeds cannot be updated.")
				os.remove(path2)
			else:
				self["dsiuTextR2"].setText("No downloaded feeds found, please download before update.")
	def bootthebox(self):
		com = 'reboot'
		self.session.open(Console,_("start shell com: %s") % (com), ["%s" % com])
	def cancel(self):
		self.close(None)
	def setMyText(self):
		self["dsiuTextR2"].setText(self.text)


def main(session, **kwargs):
	session.open(DreamboxSIrelandUpdater)
def Plugins(**kwargs):
	return PluginDescriptor(
		name="Dreambox S Ireland Updater",
		description="Downloads & Updates TV Dreambox S Ireland feeds",
		where = PluginDescriptor.WHERE_PLUGINMENU,
		icon="rsz_loho.png",
		fnc=main)
