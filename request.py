import requests
url = 'http://www.doutula.com/'

headers = {
'Referer':'http://www.doutula.com/',#防止盗用，防跨越请求字段设置，表明请求来自网站
'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',#模拟浏览器访问,UA在网站F12
    #-network（所有的请求信息都在这）网站名点击-requests-(请求头)request header
}
resp = requests.get(url,headers=headers)
# print(resp.text)#debug text 查看字符串信息
#拿到响应数据


#开始解析
from lxml import etree
html = etree.HTML(resp.text)
#解析图片链接
srcs = html.xpath('.//img/@data-original')
for src in srcs:
    filename = src.split('/')[-1]#字符串分割
    img = requests.get(src,headers=headers)#图片下载的知识点，Referer，img是图片响应，不能用字符串解析，img.content是图片字节内容
    with open('imgs/'+filename,'wb') as file:#'wb'是二进制，with打开能自己关闭
        file.write(img.content)
    print(src,filename)
print(len(srcs))



'''
http://img.doutula.com/production/uploads/image/2017/07/07/20170707422127_mRFMUJ.gif
http://img.doutula.com/production/uploads/image/2017/06/09/20170609022241_DdVgZK.gif
http://img.doutula.com/production/uploads/image/2016/10/23/20161023233712_FrEozv.gif
http://img.doutula.com/production/uploads/image/2016/01/04/20160104869236_TbDyma.gif
http://img.doutula.com/production/uploads/image/2016/06/22/20160622572926_eRkCvp.gif
'''


'''
<img referrerpolicy="no-referrer" 
class="lazy image_dtb img-responsive" 
src="//static.doutula.com/img/loader.gif?33" 
data-original="http://img.doutula.com/production/uploads/image/2020/04/29/20200429144626_SIegEr.gif" 
data-backup="http://img.doutula.com/production/uploads/image/2020/04/29/20200429144626_SIegEr.gif" 
alt="">
'''
#分析加载的真实图片的位置