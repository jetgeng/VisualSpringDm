'''
Created on Aug 11, 2012

@author: gengjet
'''
import unittest
import sys
from xml.sax import make_parser, handler
import IOCParser



class Test(unittest.TestCase):

    def setUp(self):
        self.beanParser = IOCParser.BeanParser("org.gunn.demo.bundle")
        self.parser = make_parser()
        self.parser.setContentHandler(self.beanParser)
        
    def testParserBeans(self):
        #beanParser = IOCParser.BeanParser("org.gunn.demo.bundle")
        #parser = make_parser()
        #parser.setContentHandler(beanParser)
        #parser.parse("/Users/gengjet/workbench/esuit/iotrepo/esuite/server/src/plugins/com.thu.esuite.readerplugin.opticon/META-INF/spring/spring.xml")
        pass
    
    def testBeanCreate(self):
        self.parser.parse("/Users/gengjet/Documents/workspace_for_sos/org.gunn.spring.graphic/resouce/spring.xml")
        self.beanParser.setBundle("org.gunn.demo.good")
        self.parser.parse("/Users/gengjet/Documents/workspace_for_sos/org.gunn.spring.graphic/resouce/osgi.xml")
        #self.assertNotEqual(self.beanParser._beans["subscribeManager"].refs, None, "ref is none") 
        for key in self.beanParser._beans.keys():
            self.beanParser._beans[key].resolve(self.beanParser._beans , self.beanParser._refs)
            print self.beanParser._beans[key].render()
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testParserBeans']
    unittest.main()