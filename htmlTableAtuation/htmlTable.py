#_*_ coding : utf8 _*-
# writer : lgy
# dateTime : 2018-06-29

from pyh import *
import datetime

class ToHtml:
    '''
       此类主要用来生成html文件

    '''

    def str3tocoma(self, num):  # 每三个数字加一个逗号
        e = list(str(num))
        if len(e) <= 3:
            return num
        else:
            for i in range(len(e))[::-3][1:]:
                e.insert(i + 1, ",")
            return "".join(e)

    def Gentable(self, pro, data):
        def k(x, y):
            try:
                return float(x - y) / float(y)
            except ZeroDivisionError:
                return 0

        t = table(caption='%s' % pro, border="1", cl="table1", cellpadding="0", cellspacing="0")
        t << tr(td('%s' % pro, bgColor='#0099ff') + td('当前数据') + td('上周同比数据') + td('上周同比百分比'))
        if data.has_key('dau'):
            N = k(data.get('dau')[0], data.get('dau')[1])
            if N > 0.3:
                t << tr(
                    td('DAU') + td(self.str3tocoma(data.get('dau')[0])) + td(self.str3tocoma(data.get('dau')[1])) + td(
                        "%5.2F%%" % (N * 100), bgColor='#ff0000'))
            elif N < 0:
                t << tr(
                    td('DAU') + td(self.str3tocoma(data.get('dau')[0])) + td(self.str3tocoma(data.get('dau')[1])) + td(
                        "%5.2f%%" % (N * 100), bgColor='#00ff00'))
            else:
                t << tr(
                    td('DAU') + td(self.str3tocoma(data.get('dau')[0])) + td(self.str3tocoma(data.get('dau')[1])) + td(
                        "%5.2f%%" % (N * 100)))

        else:
            t << tr(td('DAU') + td(0) + td(0) + td(0))
        if data.has_key('load'):
            N = k(data.get('load')[0], data.get('load')[1])
            if N > 0.2:
                t << tr(td('负载') + td(data.get('load')[0]) + td(data.get('load')[1]) + td("%5.2F%%" % (N * 100),
                                                                                          bgColor='#ff0000'))
            elif N < 0:
                t << tr(td('负载') + td(data.get('load')[0]) + td(data.get('load')[1]) + td("%5.2F%%" % (N * 100),
                                                                                          bgColor='#00ff00'))
            else:
                t << tr(
                    td('负载') + td(self.str3tocoma(data.get('load')[0])) + td(self.str3tocoma(data.get('load')[1])) + td(
                        "%5.2F%%" % (N * 100)))
        else:
            t << tr(td('负载') + td(0) + td(0) + td(0))
        if data.has_key('num'):
            N = k(data.get('num')[0], data.get('num')[1])
            if N > 0.2:
                t << tr(td('服务器数量') + td(data.get('num')[0]) + td(data.get('num')[1]) + td("%5.2F%%" % (N * 100),
                                                                                           bgColor='#ff0000'))
            elif N < 0:
                t << tr(td('服务器数量') + td(data.get('num')[0]) + td(data.get('num')[1]) + td("%5.2F%%" % (N * 100),
                                                                                           bgColor='#00ff00'))
            else:
                t << tr(td('服务器数量') + td(data.get('num')[0]) + td(data.get('num')[1]) + td("%5.2F%%" % (N * 100)))
        else:
            t << tr(td('服务器数量') + td(0) + td(0) + td(0))
        if data.has_key('cdn'):
            N = k(data.get('num')[0], data.get('num')[1])
            if N > 0.3:
                t << tr(td('CDN流量') + td(data.get('cdn')[0]) + td(data.get('cdn')[0]) + td("%5.2F%%" % (N * 100),
                                                                                           bgColor='#ff0000'))
            elif N < 0:
                t << tr(td('CDN流量') + td(data.get('cdn')[0]) + td(data.get('cdn')[0]) + td("%5.2F%%" % (N * 100),
                                                                                           bgColor='#00ff00'))
            else:
                t << tr(td('CDN流量') + td(data.get('cdn')[0]) + td(data.get('cdn')[0]) + td("%5.2F%%" % (N * 100)))
        else:
            t << tr(td('CDN流量') + td(0) + td(0) + td(0))
        if data.has_key('idc'):
            N = k(data.get('num')[0], data.get('num')[1])
            if N > 0.3:
                t << tr(td('IDC流量') + td(data.get('idc')[0]) + td(data.get('idc')[0]) + td("%5.2F%%" % (N * 100),
                                                                                           bgColor='#ff0000'))
            elif N < 0:
                t << tr(td('IDC流量') + td(data.get('idc')[0]) + td(data.get('idc')[0]) + td("%5.2F%%" % (N * 100),
                                                                                           bgColor='#00ff00'))
            else:
                t << tr(td('IDC流量') + td(data.get('idc')[0]) + td(data.get('idc')[0]) + td("%5.2F%%" % (N * 100)))
        else:
            t << tr(td('IDC流量') + td(0) + td(0) + td(0))
        return t

    def Tohtml(self, tables):
        page = PyH('本周报告')
        page.addCSS('common.css')
        page << h1('本周报告', align='center')
        tab = table(cellpadding="0", cellspacing="0", cl="table0")
        for t in range(0, len(tables), 2):
            tab << tr(td(tables[t - 1], cl="table0_td") + td(tables[t], cl="table0_td"))
        page << tab
        page.printOut()
