import requests                         #导入模块
from lxml import etree
from fake_useragent import UserAgent
#简单的反爬，设置一个请求头来伪装成浏览器
def request_header():
    # headers = {
    #     #'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
    #     'User-Agent': UserAgent().Chrome #谷歌浏览器
    # }
    headers = {'User-Agent': "PostmanRuntime/7.32.3"}
    return headers

'''
创建两个列表用来存放代理ip
'''
all_ip_list = []  #用于存放从网站上抓取到的ip
usable_ip_list = [] #用于存放通过检测ip后是否可以使用

normal_url = "http://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice"
#发送请求，获得响应
def send_request(init_params):
    #爬取7页，可自行修改
    for i in range(1,8):
        print(f'正在抓取第{i}页……')
        response = requests.get(url=f'https://www.kuaidaili.com/free/intr/1/?page={i}', headers=request_header())
        text = response.text.encode('utf-8')
        # print(text.decode('gbk'))
        #使用xpath解析，提取出数据ip，端口
        html = etree.HTML(text)

        tr_list = html.xpath('/html/body/div[3]/main/div/section/div[3]/div[1]/table/tbody/tr')
        for td in tr_list:
            ip_ = td.xpath('./td[1]/text()')[0] #ip
            port_ = td.xpath('./td[2]/text()')[0]  #端口
            proxy = ip_ + ':' + port_   #115.218.5.5:9000
            all_ip_list.append(proxy)
            p=test_ip(proxy,init_params)      #开始检测获取到的ip是否可以使用
            if p!=None:
                return p
    print('抓取完成！')
    print(f'抓取到的ip个数为：{len(all_ip_list)}')
    print(f'可以使用的ip个数为：{len(usable_ip_list)}')
    print('分别有：\n', usable_ip_list)
#检测ip是否可以使用
def test_ip(proxy,init_params):
    #构建代理ip
    proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy,
        # "http": proxy,
        # "https": proxy,
    }
    try:
        response = requests.get(url=normal_url,headers=request_header(),proxies=proxies,params=init_params,timeout=1) #设置timeout，使响应等待1s
        response.close()
        if response.status_code == 200:
            usable_ip_list.append(proxy)
            print(proxy, '\033[31m可用\033[0m')
            return response
        else:
            print(proxy, '不可用')
            return None
    except:
        print(proxy,'请求异常')
        return None

if __name__ == '__main__':
    print(
        len(str(send_request()))
    )
    # from fake_useragent import UserAgent
    #
    # print(UserAgent().random)
