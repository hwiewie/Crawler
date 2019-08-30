#-*- coding:UTF-8 -*-
import re , ast

#from google.appengine.ext import webapp
#from google.appengine.ext.webapp.util import run_wsgi_app
import webapp2
from google.appengine.api import urlfetch 

#import datetime
from vo.SsqInfo import SsqInfo

'''
获取最新双色球开奖数据
'''
class GetLastSsqData(webapp2.RequestHandler):
    def lastDataByIssue(self,doc,issue):
        """根据开奖期号分析双色球原数据，并把目标数据转换为期望的数据结构"""
        if doc is None:
            return None
        
        self.response.out.write( 'we need issue is %s <br/>' % str(issue))
        
        ssqInfo = SsqInfo()
        
        kjDataRE = re.compile(r'var kjData_1 = eval\(\'\(\' \+ \''
                              r'(?P<data>.*)\' \+ \'\)\'\)\;')
        
        zjDataRE = re.compile(r'var zjData_1 = eval\(\'\(\' \+ \''
                              r'(?P<data>.*)\' \+ \'\)\'\)\;')
        
        for l in doc.split('\n'):
            kjData = kjDataRE.search(l)
            if kjData:
                kjDict = ast.literal_eval(kjData.group('data'))
                if kjDict.has_key(str(issue)):
                    self.response.out.write( 'date :\t %s <br/>' % kjDict[str(issue)]['kjDate'])
                    self.response.out.write( 'issue :\t %s <br/>' % kjDict[str(issue)]['kjIssue'])
                    self.response.out.write( 'red :\t %s <br/>' % kjDict[str(issue)]['kjZNum'])
                    self.response.out.write( 'blue :\t %s <br/>' % kjDict[str(issue)]['kjTNum'])
                    
                    ssqInfo.kjDate = kjDict[str(issue)]['kjDate']
                    ssqInfo.issue = kjDict[str(issue)]['kjIssue']
                    ssqInfo.red = kjDict[str(issue)]['kjZNum']
                    ssqInfo.blue = kjDict[str(issue)]['kjTNum']
                
            zjData = zjDataRE.search(l)
            if zjData:
                zjDict = ast.literal_eval(zjData.group('data'))
                if zjDict.has_key(str(issue)):
                    self.response.out.write( '本期开奖采用 :\t 第%s套球<br/>' % zjDict[str(issue)]['QNum'])
                    self.response.out.write( '奖池累计金额 :\t %d<br/>' % zjDict[str(issue)]['jcMoney'])
                    self.response.out.write( '本期销售额 :\t %d<br/>' % zjDict[str(issue)]['tzMoney'])
                    
                    ssqInfo.ballNum = zjDict[str(issue)]['QNum']
                    ssqInfo.poolMoneyAmount = zjDict[str(issue)]['jcMoney']
                    ssqInfo.soldMoneyAmount = zjDict[str(issue)]['tzMoney']
                    
                    self.response.out.write( '一等奖 单注中奖金额（元） :\t %d<br/>' % zjDict[str(issue)]['oneJ'])
                    self.response.out.write( '一等奖 中奖注数（注） :\t %d<br/>' % zjDict[str(issue)]['oneZ'])
                    ssqInfo.oneBetAmount = zjDict[str(issue)]['oneZ']
                    ssqInfo.oneMoneyAmount = float(zjDict[str(issue)]['oneJ'])
                    
                    self.response.out.write( '二等奖 单注中奖金额（元） :\t %d<br/>' % zjDict[str(issue)]['twoJ'])
                    self.response.out.write( '二等奖 中奖注数（注） :\t %d<br/>' % zjDict[str(issue)]['twoZ'])
                    ssqInfo.twoBetAmount = zjDict[str(issue)]['twoZ']
                    ssqInfo.twoMoneyAmount = float(zjDict[str(issue)]['twoJ'])
                    
                    self.response.out.write( '三等奖 单注中奖金额（元） :\t %d<br/>' % zjDict[str(issue)]['threeJ'])
                    self.response.out.write( '三等奖 中奖注数（注） :\t %d<br/>' % zjDict[str(issue)]['threeZ'])
                    ssqInfo.threeBetAmount = zjDict[str(issue)]['threeZ']
                    ssqInfo.threeMoneyAmount = float(zjDict[str(issue)]['threeJ'])
                    
                    self.response.out.write( '四等奖 单注中奖金额（元） :\t %d<br/>' % zjDict[str(issue)]['fourJ'])
                    self.response.out.write( '四等奖 中奖注数（注） :\t %d<br/>' % zjDict[str(issue)]['fourZ'])
                    ssqInfo.fourBetAmount = zjDict[str(issue)]['fourZ']
                    ssqInfo.fourMoneyAmount = float(zjDict[str(issue)]['fourJ'])
                    
                    self.response.out.write( '五等奖 单注中奖金额（元） :\t %d<br/>' % zjDict[str(issue)]['fiveJ'])
                    self.response.out.write( '五等奖 中奖注数（注） :\t %d<br/>' % zjDict[str(issue)]['fiveZ'])
                    ssqInfo.fiveBetAmount = zjDict[str(issue)]['fiveZ']
                    ssqInfo.fiveMoneyAmount = float(zjDict[str(issue)]['fiveJ'])
                    
                    self.response.out.write( '六等奖 单注中奖金额（元） :\t %d<br/>' % zjDict[str(issue)]['sixJ'])
                    self.response.out.write( '六等奖 中奖注数（注） :\t %d<br/>' % zjDict[str(issue)]['sixZ'])
                    ssqInfo.sixBetAmount = zjDict[str(issue)]['sixZ']
                    ssqInfo.sixMoneyAmount = float(zjDict[str(issue)]['sixJ'])
                    
                    ssqInfo.save()
                
        self.response.out.write( '<br/><br/>All things have DONE!!')
              
          
    def get(self):
        issue = 2013001   #需要的开奖期号
        
        ssqInfo = None
        q = SsqInfo.all()
        q.order('-issue')
        results = q.fetch(limit=1)
        if len(results) > 0:
            ssqInfo = results[0]
        
        if ssqInfo is not None:
            issue = int(ssqInfo.issue) + 1
        
        
        url = "http://kj.zhcw.com/kjData/2012/zhcw_ssq_index_last30.js"  
        result = urlfetch.fetch(url)  
        if result.status_code == 200:  
            doc = result.content  
            
            self.lastDataByIssue(doc,issue)
            
            
            
            
#            self.response.out.write(doc)
        
#        uiList = UserInfo.gql('order by createDate desc')
#        
#        self.response.out.write(unicode('''
#            <html>
#            <head>
#                <meta charset="utf-8" />
#                <title>Untitled</title>
#            </head>
#            <body>
#            <table border=1>
#                <tr>
#                    <td>ID</td>
#                    <td>IMEI</td>
#                    <td>IMSI</td>
#                    <td>最后GPS位置</td>
#                    <td>设备名称</td>
#                    <td>MAC地址</td>
#                    <td>登陆次数</td>
#                    <td>最后登陆时间</td>
#                </tr>
#            ''','UTF-8'))
#        
#        for ui in uiList:
#            self.response.out.write('''
#                <tr>
#                    <td>%s</td>
#                    <td>%s</td>
#                    <td>%s</td>
#                    <td>%s</td>
#                    <td>%s</td>
#                    <td>%s</td>
#                    <td>%s</td>
#                    <td>%s</td>
#                </tr>'''%(ui.key().id()
#                          ,ui.imei
#                          ,ui.imsi
#                          ,ui.gps
#                          ,ui.deviceName
#                          ,ui.macAddress
#                          ,ui.loginCount
#                          ,ui.createDate+ datetime.timedelta(hours=+8)))
#        
#        self.response.out.write('''
#            </table>
#            </body>
#            </html>
#            ''')

