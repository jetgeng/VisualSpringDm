# -*- coding: utf-8 -*-
'''
Created on Aug 11, 2012
@author: gengjet
'''
import sys
from xml.sax import make_parser, handler
import uuid

from mako.template import Template


beanTemplate = '''
    
    
    class ${bean._classname } {
    }
   
    % for ref in bean.refs.keys() :
        
    %if bean.refs[ref].pojoclassname == u"Bean" :
    class  ${ bean.refs[ref]._classname } {
    }
    %else:
     interface  ${ bean.refs[ref]._classname } {
    }
    %endif
   
    ${ bean._classname }  --> ${ bean.refs[ref]._classname }
    % endfor

'''
beanRendTemplate = Template(beanTemplate)

class SuperBean():
    '''
    保存所有Bean的父亲
    '''
    
    def __init__(self, bundle, attrs , typebean='SuperBean'):
        if attrs.has_key("id") :
            self._id = attrs["id"] 
        else:
            self._id = uuid.uuid4()
        self._bundle = bundle
        self.pojoclassname = typebean
        
class Bean(SuperBean):
    '''
    只是为<bean> 这个标签服务
    '''
    def __init__(self, bundle ,attrs):
        SuperBean.__init__(self, bundle, attrs , typebean="Bean")
        
        self._classname = attrs["class"]
        self.proterties = {}
        self.refs={}
       
    def addProperty(self, atts):
        '''
        这里的ref，可能是services，和bean。这个有点小麻烦。
        这里有两种情况，
        1. atts 中包括 name和ref两项
        1. atts 中只包括一项name，ref是在他的子节点中给出
        我只要求出ref相关的类名就可以了。
        '''
        if atts["name"] != None :
            self.proterties[atts.get("name")] = atts.get("ref") if atts.get("ref") != None else ""
    def resolve(self,beans,refs):
        for property in self.proterties :
            if beans.has_key(self.proterties[property]) :
                self.refs[self.proterties[property]] = beans[self.proterties[property]]
            elif refs.has_key(self.proterties[property]) :
                self.refs[self.proterties[property]] = refs[self.proterties[property]]
        pass
    
    def render(self):
        return beanRendTemplate.render(bean=self , BeanType = Bean)
    
    def __str__ (self):
        return "Bean (id= %s , bundle = %s , class=%s ) "  \
            %( self._id , self._bundle, self._classname )

class Service(Bean):
    '''
    发布出来的一个服务是一个服务,在这里 _classname,代表的是一个接口。
    '''
    
    def __init__(self, bundle ,attrs):
        SuperBean.__init__(self, bundle, attrs ,typebean="Service")
        self._classname = attrs.get(u"interface")
        self._ref = attrs.get(u"ref")
        
    def resolve(self,beans):
        '''
        获取ref代表的真正的类
        '''
        pass
    
    def __str__ (self):
        return "Services (id= %s , bundle = %s , interface=%s , refName = %s) "  \
            %( self._id , self._bundle, self._classname , self._ref)

class ServiceRef(Bean):
    def __init__(self,bundle,attrs):
        SuperBean.__init__(self, bundle, attrs , typebean="ServiceRef")
        self._classname = attrs["interface"]
        self._bundle = bundle
        
    def __str__ (self):
        return "ServiceRef (id= %s , bundle = %s , interface=%s ) "  \
            %( self._id , self._bundle, self._classname )

class BeanParser(handler.ContentHandler):
    '''
    就是一个简单的Xml解析解析器。获取其中的关于Service的信息。
    '''
    
    def __init__(self,bundle):
        '''
        Constructor
        '''
        self._beans = {}
        self._services={}
        self._refs = {}
        self._bundle = bundle
        
    def setBundle(self , bundle):
        self._bundle = ''.join(bundle)
   
    def startElement(self,name , attrs):
        if u'osgi:service' == name :
            service = Service(self._bundle, attrs)
            self._services[service._id] = service
            print "get a services %s" % service 
        elif u'bean'  == name :
            self.currentBean = Bean(self._bundle , attrs)
        elif u'property' == name :
            self.currentPropertyName = attrs["name"]
            self.currentBean.addProperty(attrs)
            print "add property %s to Bean %s" % (self.currentPropertyName, self.currentBean)
        elif u'ref' == name :
            if self.currentBean != None and self.currentPropertyName != None :
                self.currentBean.addProperty({"name":self.currentPropertyName,"ref":attrs["bean"]})
                print "add property %s to Bean %s" % (self.currentPropertyName, self.currentBean)
        elif u'osgi:reference' == name :
            osgiReference = ServiceRef(self._bundle,attrs)
            self._refs[osgiReference._id] = osgiReference
            print "handle bean interface is : %s" % attrs.get("interface") 
        #print name ,attrs
    
    def endElement(self, name):
        if u'bean' == name and self.currentBean != None:
            self._beans[self.currentBean._id] = self.currentBean
            self.currentBean = None
        elif u'property' == name :
            self.currentPropertyName = None
            #print "add bean id is : %s" % self.currentBean
        handler.ContentHandler.endElement(self, name)
        
