import xml.etree.ElementTree as ET
import os

ans=[]

def traverseXml(element):
	if len(element)>0:
		for child in element:
			traverseXml(child)
			ans.append([child.tag,child.attrib])

def parse(filename):
	xmlFilePath = os.path.abspath(filename)
	tree = ET.parse(xmlFilePath)
	root = tree.getroot()
	ans.append([root.tag,root.attrib])
	traverseXml(root)
	return ans
