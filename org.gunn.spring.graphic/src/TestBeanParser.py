# -*- coding: utf-8 -*-
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
        self.parser.parse("/Users/gengjet/workbench/esuit/iotrepo/esuite/server/src/plugins/com.easyway.com.espertech.esperdds/META-INF/spring/spring.xml")
        self.parser.parse("/Users/gengjet/workbench/esuit/iotrepo/esuite/server/src/plugins/com.easyway.com.espertech.esperdds/META-INF/spring/osgi.xml")
        #self.assertNotEqual(self.beanParser._beans["subscribeManager"].refs, None, "ref is none") 
        for key in self.beanParser._beans.keys():
            self.beanParser._beans[key].resolve(self.beanParser._beans , self.beanParser._refs)
            print self.beanParser._beans[key].render()
        for key in self.beanParser._services.keys():
            self.beanParser._services[key].resolve(self.beanParser._beans )
            print self.beanParser._services[key].render()
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testParserBeans']
    unittest.main()