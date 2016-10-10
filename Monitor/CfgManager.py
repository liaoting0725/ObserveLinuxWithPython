# coding:utf-8
import ConfigParser
import os

class CfgManager(object):
	configName = ''
	configPath = ''
	configParse = ''
	def __init__(self, configName):
		self.configName = configName
		currentDir = os.getcwd()
		self.configPath = currentDir +'/'+configName
		self.configParse = ConfigParser.ConfigParser()

	def getSections(self):
		self.configParse.read(self.configPath)
		list = self.configParse.sections()
		return list

	def getIntValue(self, sectionHeader, key):
		self.configParse.read(self.configPath)
   		value = self.configParse.getint(sectionHeader,key)
  		return value

	def getBoolValue(self, sectionHeader, key):
		self.configParse.read(self.configPath)
		value = self.configParse.getboolean(sectionHeader, key)
		return value

	def getValue(self,sectionHeader, key):
		self.configParse.read(self.configPath)
		value = self.configParse.get(sectionHeader,key)
		return value

	def getFloatValue(self,sectionHeader, key):
		self.configParse.read(self.configPath)
		value = self.configParse.getfloat(sectionHeader,key)
		return value

  	def setValue(self,sectionHeader,key, value):
		with open(self.configPath,'rw') as cfgfile:
			self.configParse.readfp(cfgfile)
			self.configParse.set(sectionHeader, key,str(value))
			self.configParse.write(open(self.configPath,'r+'))


# if __name__ == '__main__':
# 	manager = CfgManager('config.cfg')
# 	time = manager.getNoticeTime('notice','time')
# 	print time
# 	time = time+1
# 	manager.setNoticeTime('notice','time',time)
# 	time = manager.getNoticeTime('notice','time')
# 	print time




