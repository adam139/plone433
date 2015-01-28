#-*- coding: UTF-8 -*-
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from plone.app.layout.navigation.interfaces import INavigationRoot

from my315ok.socialorgnization import _

from my315ok.products.product import Iproduct
from plone.app.collection.interfaces import ICollection

from plone.memoize.instance import memoize

fmt = '%Y/%m/%d %H:%M:%S'
import re
from datetime import datetime,timedelta
import socket
import time
import urllib2
try:
    from BeautifulSoup import BeautifulSoup,SoupStrainer
except:
    print "ERROR: could not import BeautifulSoup Python module"
    print
    print "You can download BeautifulSoup from the Python Cheese Shop at"
    print "http://cheeseshop.python.org/pypi/BeautifulSoup/"
    print "or directly from http://www.crummy.com/software/BeautifulSoup/"
    print
    raise
from my315ok.portlet.fetchouterhtml.fetchouterportlet import FetchOutWebPage

from Products.CMFCore import permissions
grok.templatedir('templates') 

class HomepageView(grok.View):
     
    grok.context(ISiteRoot)
    grok.template('homepage')
    grok.name('homepage')
    grok.require('zope2.View')    
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
    
    def show_more(self):
        return True

    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm
    
    def cropTitle(self,text, length, ellipsis='...'):
        if length == 0 or length == None:
            return text
        context = aq_inner(self.context)
        pview = getMultiAdapter((context,self.request),name=u"plone")
#        pview = getMultiAdapter((self.parent(), self.request), name=u'earthqk_event_view')
        croped = pview.cropText(text, length)
        return croped
            
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal,self.context) 

    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain='my315ok.socialorgnization',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="chengli")
        return title   
        
    def fromid2title(self,id):
        """根据对象id，获得对象title"""
       
        
        brains = self.catalog()({'id':id})
        if len(brains) >0:
            return brains[0].Title
        else:
            return id
############################ JQ swf portlet
    def swf_locid(self):
        """return swf css id"""
        return "mainflash"
    
    @memoize
    def swf_js_settings(self,**parameters):

        out = """genswf("%(swfile)s","transparent",%(ht)s,%(wh)s,"#%(swfLocid)s");""" \
        % dict(swfile=parameters['swf'],ht=parameters['height'],wh=parameters['width'],swfLocid=self.swf_locid())
        return out                       


        

#######carousel    
    def carouselid(self):
        return "carouselid"
    
    def active(self,i):
        if i == 0:
            return "active"
        else:
            return ""
        
    @memoize
    def carouselresult(self,path=None):
        """ path is absolute path.example:'/pub'"""
        
        out = """
        <div id="carousel-generic" class="carousel slide">
  <!-- Indicators -->
  <ol class="carousel-indicators">
    <li data-target="#carousel-generic" data-slide-to="0" class="active"></li>
    <li data-target="#carousel-generic" data-slide-to="1"></li>
    <li data-target="#carousel-generic" data-slide-to="2"></li>
  </ol>

  <!-- Wrapper for slides -->
  <div class="carousel-inner">
    <div class="item active">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>    
  </div>

  <!-- Controls -->
  <a class="left carousel-control" href="#carousel-generic" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="#carousel-generic" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>

</div>
        """ 
        
        if path == None:
            queries = {'object_provides':Iproduct.__identifier__, 
                                    'b_start':0,
                                    'b_size':3,
                             'sort_order': 'reverse',
                             'sort_on': 'created'}
        else:
            queries = {'object_provides':Iproduct.__identifier__, 
                                    'b_start':0,
                                    'b_size':3,
                                    'path':path,
                             'sort_order': 'reverse',
                             'sort_on': 'created'}
        braindata = self.catalog()(queries)
        brainnum = len(braindata)
        if brainnum == 0:return out        

        outhtml = """<div id="%s" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
        """ % (self.carouselid())
        outhtml2 = '</ol><div class="carousel-inner">'
        for i in range(brainnum):            
            out = """<li data-target='%(carouselid)s' data-slide-to='%(indexnum)s' class='%(active)s'>
            </li>""" % dict(indexnum=str(i),
                    carouselid=''.join(['#',self.carouselid()]),
                    active=self.active(i))
                                               
            outhtml = ''.join([outhtml,out])   # quick concat string
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            outimg = """<div class="%(classes)s">
                        <img src="%(imgsrc)s" alt="%(imgtitle)s"/>
                          <div class="carousel-caption">
                            <h3>%(imgtitle)s</h3>
                              </div>
                                </div>""" % dict(classes=''.join(["item ", self.active(i)]),
                     imgsrc=''.join([objurl, "/@@images/image/preview"]),imgtitle=objtitle)
            outhtml2 = ''.join([outhtml2,outimg])   # quick concat string                    
#        outhtml = outhtml +'</ol><div class="carousel-inner">'
        result = ''.join([outhtml,outhtml2])   # quick concat string
        out = """
        </div><a class="left carousel-control" href="%(carouselid)s" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="%(carouselid)s" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>
</div>""" % dict(carouselid = ''.join(["#", self.carouselid()]))
        return ''.join([result,out])
                
              
# roll zone

    def rollwrapperclass(self):
        return "roll-wrapper"
        
    def rollheader(self):
        return u"新闻"
    
    def rollmore(self):
        return "http://315ok.org/"
    
    @memoize
    def rollresult(self,collection=None,limit=7):
        """return roll zone html"""
        
        if collection == None:
            braindata = self.catalog()({'meta_type':'ATNewsItem',
                                    'b_start':0,
                                    'b_size':limit,
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        else:

            queries = {'object_provides':ICollection.__identifier__, 
                                    'id':collection}
            ctobj = self.catalog()(queries)
            if ctobj is not None:
                # pass on batching hints to the catalog
                braindata = ctobj[0].getObject().queryCatalog(batch=True)
            else:           
                braindata = None
                      
        outhtml = """<div class="%s" data-pause="1000" data-step="1" data-speed="30" data-direction="up">
            <ul class="rolltext">
        """ % (self.rollwrapperclass())
        brainnum = len(braindata)
        if brainnum == 0 : return "roll zone"
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            objtitle = self.cropTitle(objtitle, 12)
            modifydate = braindata[i].modified.strftime('%Y-%m-%d')
            
            out = """<li class="rollitem">
            <span>
            <a href="%(objurl)s" title="%(title)s">%(title)s</a>
            </span>
            <span class="portletItemDetails">%(date)s</span></li>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            date= modifydate)
                                               
            outhtml = ''.join([outhtml,out])   #quick concat string
        outhtml = "%s</ul></div>" % outhtml
        return outhtml                
        
##### roll images portlet
    def roll_images_js(self,**parameters):
        """roll images js"""
  
        out="""$(document).ready(function(){ajaxfetchimg("%(topid)s","%(url)s",".%(mid)s",%(text)s);});"""
        out=out % dict(topid=topid,url=imgsrc,mid=cssid,text=showtext)
        return out           
        
    def roll_images(self,**parameters):
        """
        output roll images
        parameters:
        topid: roll zone wrapper CSS id
        href:portlet header link to url
        title:portlet header text
        pause: pause time, seconds
        step:  roll step
        direction:up,down,left,right
        speed:roll speed
        ajaxsrc: images source url
        mid:roll zone inner css id
        text:1,display text under image;0 No...  
        """ 
        out = """
    <div class="portlet roll_imageportlet">
        <h4 class="portletHeader">        
        <a href="%(href)s">%(title)</a>
        </h4>    
        <div id="%(topid)s">
        <div class="marquee" pause="%(pause)s" step="%(step)s" speed="%(speed)s" direction="%(direction)s">
            <ul class="img"></ul>          
        </div>
        </div>  
        <div>
        <script>%(scripts)s</script>         
        </div>
    </div>
        """ 
        out = out % dict(topid=parameters["topid"],
                         href=parameters["href"],
                         title=parameters["title"],
                         pause=parameters["pause"],
                         step=parameters["step"],
                         speed=parameters["speed"],
                         direction=parameters["direction"],
                         scripts=self.render_imgjs(topid=parameters["topid"],
                                                   url=parameters["ajaxsrc"],
                                                   mid=parameters["mid"],
                                                   text=parameters["text"])) 
        return out            
        
# outer html zone


    
    def outhtmlheader(self):
        return u"论坛热帖"
    
    def outhtmlmore(self):
        return "http://plone.315ok.org/"
    
# scrap code
    def isfetch(self,id):
        from time import mktime
        container = self.target_folder()
        if id == None:
            return 1
        obj = getattr(container,id,None)
        if obj == None: 
            return 1       
        #imevalue = self.folder.doc.modified()
        timevalue = obj.modified()        
        
        di = time.strptime(timevalue.strftime(fmt),fmt)
        dt = datetime.fromtimestamp(mktime(di))

        now =   datetime.now()
        if (now - dt) > timedelta(hours = self.dataparameter()['interval']):
            return 1        
        return 0       
    
    def target_baseurl(self):
        tmp = self.dataparameter()['target']
        g = tmp.split("/")
        baseurl = g[0] + "//" + g[2]
        return baseurl        
        
    def portlet_header(self):        
        return  self.data.header    

    @memoize         
    def target_folder(self):

        folder = self.catalog()({'portal_type': 'Folder','id':'pub'})
      
        if (len(folder) > 0):
            return folder[0].getObject()
        else:
            self.context.invokeFactory(type_name="Folder", id='pub')
            folder = self.context['pub']
            folder.setExcludeFromNav(True)
            folder.reindexObject() 
            return folder            


    
    def dataparameter(self):
        data = {
                'code':"utf-8",
                'filter':True,
                'target':"http://plone.315ok.org/",
                'tag':"div",
                'cssid':"portal_block_52_content",
                'cssclass':"dxb_bc",
                'attribute':"",
                'regexp':"",
                'index':0,   #fetch first block
                'interval':24
                }
        return data
    @memoize
    def get_htmlsrc(self): 
#        import pdb
#        pdb.set_trace()
        data = self.dataparameter()
        results = []               
        dapi = FetchOutWebPage()
        srccode = data['code']
        filter = data['filter']
        gotdata = dapi._query(data['target'])
        if gotdata:
            if filter:                
                htmlsource = dapi._extract_data(dapi._tidysrc(gotdata,srccode),data['tag'],data['cssid'],data['cssclass'],\
                                                data['attribute'],data['regexp'],data['index'])
            else:
                htmlsource = dapi._extract_data(gotdata,data['tag'],data['cssid'],data['cssclass'],\
                                                data['attribute'],data['regexp'],data['index'])                 
            return htmlsource
        else:
            return results
            
    @memoize
    def outhtmlresult(self):

        try:
            return self.outer("outhtml")
        except:
            return u''
        
    @memoize        
    def prettyformat(self):
        """transform the relative url to absolute url"""        
        import re
        html = self.get_htmlsrc()
#        import pdb
#        pdb.set_trace()
        if type(html) == type([]):
            html = html[0]
        if type(html) != type(""):
            try:
                html = str(html)
            except:
                html = html.__str__()            
        tmp = BeautifulSoup(html)
        base = self.target_baseurl()
#        aitems = tmp.findAll("a",href=re.compile("^\/"))
        aitems = tmp.findAll("a",href=re.compile("^[^hH]"))
        for i in aitems:
            u = i['href']
            if u[0] != '/':
                i['href'] = ''.join([base,'/', u])          #quick concat string
            else:                
                i['href'] = ''.join([base, u])
#        imgitems = tmp.findAll("img",src=re.compile("^\/"))
        imgitems = tmp.findAll("img",src=re.compile("^[^hH]"))
        for j in imgitems:
            v = j['src']
            if v[0] != '/':
                j['src'] = ''.join([base,'/', v])
            else:                
                j['src'] = ''.join([base, v])
        return tmp                      
        
        
    def outer(self,id):
#        import pdb
#        pdb.set_trace()
        if self.isfetch(id):
            try:                
                tmp = self.prettyformat()
                if type(tmp) == type([]):
                    tmp = tmp[0]
                try:
                    tmp = str(tmp)
                except:
                    tmp = tmp.__str__()
                saved = self.store_tmp_content(id, tmp)
#                import pdb
#                pdb.set_trace()
                return tmp                
            except:
                return self.fetch_tmp_content(id)
        else:                
            return self.fetch_tmp_content(id)
            
    @memoize 
    def fetch_tmp_content(self,id):
#        import pdb
#        pdb.set_trace()
        container = self.target_folder()
        try:
            obj = container[id]
        except:
            return u""
        cached = obj.getText()
        return cached     
            
       
    def store_tmp_content(self,id,content):

        container = self.target_folder()
        if id == None:
            return
        obj = getattr(container,id,None)
        if obj == None:           
            container.invokeFactory(type_name="Document", id=id)
            obj = container[id]      
        obj.setText(content)
        obj.setTitle(id)
#        obj.reindexObject()
        obj.setModificationDate(datetime.now().strftime(fmt))
        return 1    
    
#n output js 
    def outputjs(self):
        cssid = self.rollwrapperclass()
       
        out="""$(document).ready(function(){rolltext(".%(mid)s");});""" % dict(mid=cssid)
        return out  
####################
#slide bar
    def target(self):
        """
        返回面板标题链接地址，用于继承类覆盖时调用
        """
        return "http://www.315ok.org"
    
    def title(self):
        """
        返回面板标题
        """
        return u"产品展示"
    
    def ajaxsrc(self):
        return "http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/@@barsview_preview"
    
    def inteval(self):
        return 6000

    @memoize
    def render_imgjs(self,**parameters):
        """
        parameters:dictionary 
        outid, outest cssid
        ajaxsrc, image data source ,a url of simple multiproducts page
        intervalset, loop time
        """
        out="""$(document).ready(function()
        {imgPlayer("%(slideid)s", "%(url)s",function()
          {setTimeout(function(){ $("#%(slideid)s").show();},200);});
         var interval = setInterval('showNumImg("%(slideid)s")', %(ms)s);
         $("#%(slideid)s .num").bind("mouseenter",function(){clearInterval(interval);})
         $("#%(slideid)s .num").bind("mouseleave",function(){interval = setInterval('showNumImg("%(slideid)s")', %(ms)s);})
 });""" % dict(slideid=parameters["outerid"],url=parameters["ajaxsrc"],ms=parameters["intervalset"])
        return out
    
    def output_sidebar(self):
        """
        输出ajax图片轮换面板    
        """
        out="""
        <div class="portlet portletslidebar_portlet">
            <h4 class="portletHeader text-center">        
            <a href="%(target)s">%(title)s</a>        
            </h4>
            <div>
            <script src="http://images.315ok.org/imgPlayer.nojq.js"></script>       
            <div id="slidecontainer" class="txtBanner noMarginTop">
                <div id="sliderimages" class="slideBanner">
                    <ul class="img"></ul>
                    <div class="panel"></div>
                    <ul class="num"></ul>
                </div>
            </div>    
        <script>%(scripts)s</script> 
        </div>  
        </div>        
        """
        return out % dict(target=self.target(),
                          title=self.title(),
                          scripts=self.render_imgjs(
                                                    outid="sliderimages",
                                                    ajaxsrc=self.ajaxsrc(),
                                                    intevalset=self.inteval()))
            
#### kuputable container ####
    
    def groupcollection_size(self):
        return 7
    
    def collection_url(self,target_collection):
        if not target_collection:
            return None
        queries = {'object_provides':ICollection.__identifier__, 
                                    'id':target_collection}
        ctobj = self.catalog()(queries)
        return ctobj[0].getPath()        
        
    @memoize
    def collection(self,target_collection,limit):
        """   target_collection collection id     """
#        collection_path = target_collection
        if not target_collection:
            return None
        queries = {'object_provides':ICollection.__identifier__, 
                                    'id':target_collection}
        ctobj = self.catalog()(queries)
        if ctobj is not None:
                # pass on batching hints to the catalog
            braindata = ctobj[0].getObject().queryCatalog(batch=True, b_size=limit)
        else:           
            braindata = None
        return braindata        
    
