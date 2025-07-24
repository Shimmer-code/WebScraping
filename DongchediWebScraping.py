import helium as hl
import codecs
from lxml import etree
import time

driver=hl.start_chrome('https://www.dongchedi.com/community/4865/wenda-release')

def to_file(list,path):
    with codecs.open(path+'懂车帝问答e'+'.txt','a+','utf-8') as t2:
        for i in list:
            t2.write('\t'.join(i).replace('\r','').replace('\n','')+'\r\n')
def extract():
    url=driver.current_url 
    e1=driver.page_source
    e2=etree.HTML(e1)
    e3=e2.xpath('//div[@class="jsx-3811145822 data-wrapper tw-pt-12"]/section')
    z=[]
    for i in e3:
        z0=''.join(i.xpath('.//div[@class="tw-flex tw-items-center"]//div[@class="tw-overflow-hidden tw-flex tw-items-center tw-h-20"]//text()'))#评论人
        z1=''.join(i.xpath('.//div[@class="tw-flex tw-items-center"]//@href'))#评论人网址
        z2=''.join(i.xpath('.//div[@class="tw-flex tw-items-center"]//div[@class="tw-h-16 tw-mt-4 tw-flex tw-items-center"]//text()'))#评论人简介
        z3=''.join(i.xpath('.//div[contains(@class,"jsx-81802501")]//text()'))#内容
        z4=';'.join(i.xpath('.//div[contains(@class,"tw-grid tw-grid-cols-5 2xl:tw-grid-cols-6 tw-gap-8")]//@src'))#图片
        z5=''.join(i.xpath('.//div[@class="jsx-1875074220 right tw-flex tw-items-center tw-flex-none tw-text-12 md:tw-text-14 xl:tw-text-14"]/button[1]//text()'))#回答数
        z6=''.join(i.xpath('.//div[@class="jsx-1875074220 right tw-flex tw-items-center tw-flex-none tw-text-12 md:tw-text-14 xl:tw-text-14"]/button[2]//text()'))#收藏数
        z7=''.join(i.xpath('.//div[@class="jsx-1875074220 tw-flex tw-items-center tw-flex-1 tw-overflow-hidden tw-mr-24 tw-text-12 md:tw-text-14 xl:tw-text-14"]//text()'))#时间

        z.append([url,z0,z1,z2,z3,z4,z5,z6,z7])
    to_file(z,'D:/')
def run(url):
    hl.go_to(url)
    hl.scroll_down(4000)  
    while 1:
        try:
            extract()
            time.sleep(1)
            hl.click(hl.S('//ul[@class="jsx-1325911405 tw-flex"]/li[last()]/a//i[@class="jsx-1325911405 DCD_Icon icon_into_12 tw-text-14"]'))
            time.sleep(2)
            hl.scroll_down(4000)
            time.sleep(1)
        except Exception as e:
            print(e)
            break
urls=['https://www.dongchedi.com/community/4865/wenda-release']
for url in urls:
    run(url)
    
from pyecharts import options as opts
from pyecharts.charts import Bar
import pandas as pd

data=pd.read_excel(r'D:\懂车帝回答e.xlsx','Sheet1')['时间调整']
data_count=data.value_counts()

c = (
    Bar()
    .add_xaxis(data_count.index.values.tolist())
    .add_yaxis("懂车帝问题数", data_count.values.tolist())
    .set_global_opts(title_opts=opts.TitleOpts(title="", subtitle=""))
    .render(r'D:\懂车帝e.html'))

import codecs
import pandas as pd
from collections import Counter
# import jieba
# jieba.load_userdict("D:/自定义.txt")
import jieba.posseg as pseg   #安装jieba库：pip install jieba -i https://pypi.tuna.tsinghua.edu.cn/simple
#读入文件
#把懂车帝问答.xlsx中的[回答文本]列单独保存成：回答.text
x1=codecs.open('D:/提问e.txt','r')
x2=x1.read()
x1.close()
#分词并词性标注
x3=list(pseg.cut(x2))
#统计词频
x4=Counter(x3)
y1=[]
y2=[]
y3=[]
y4=[]
y5=[]
for j in x4:
    y1.append(x4[j])
    y2.append(list(j)[0])
    y3.append(list(j)[1])

z2=pd.DataFrame({'分词':y2,'词频':y1,'词性':y3})
z2=z2.sort_values(by='词频',ascending=False)
z2.to_excel('D:/回答-词频统计e.xlsx',sheet_name='Sheet1',index=False)

import codecs
import pandas as pd
from collections import Counter
import jieba.posseg as pseg
from tqdm import tqdm

w1 = pd.read_excel(r'D:\懂车帝回答e.xlsx', 'Sheet3')
w11 = w1['时间调整'].drop_duplicates()  # 提取时间并去重

for i in tqdm(w11):
    # 提取问题文本并转为字符串
    texts = w1[w1['时间调整'].isin([i])]['问题标题'].astype(str).tolist()
    x2 = '\r\n'.join(texts)

    print(i)
    x3 = list(pseg.cut(x2))  # 分词+词性标注

    # ==== 新增词频统计部分（改动点）====
    word_freq = Counter((word.word, word.flag) for word in x3)  # 统计(词,词性)频率

    # 提取数据
    words = []
    freqs = []
    pos_tags = []
    for (word, pos), count in word_freq.items():
        words.append(word)
        pos_tags.append(pos)
        freqs.append(count)

    # 创建DataFrame（新增'词频'列）
    z1 = pd.DataFrame({'分词': words, '词性': pos_tags, '词频': freqs})
    z1 = z1.sort_values('词频', ascending=False)  # 按词频排序

    # ==== 保存文件（文件名稍作修改）====
    output_filename = f'D:/out2/{str(i)}-词频统计.xlsx'  
    z1.to_excel(output_filename, sheet_name='Sheet1', index=False)

import os
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Page

pos = ['n', 'ng', 'nrfg', 'nrt', 'ns', 'nt', 'nz']  # 要筛选的各类名词

file_dir = os.listdir('D:/out2')  # 列出列表内容

page = Page()
for i in file_dir:
    i1 = pd.read_excel('D:/out2/' + i, 'Sheet1')  # 读入文件
    i2 = i1[i1['词性'].isin(pos)].iloc[0:15, :]  # 筛选
    i3 = (
        Bar()  # 画图
        .add_xaxis(i2['分词'].to_list())  # x轴名称
        .add_yaxis(i.replace('-词频统计.xlsx', ''), i2['词频'].to_list())  # y轴名称
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各月关注点"),
        )
    )
    page.add(i3)
page.render('D:/out2/懂车帝各月关注.html')

import os
import pandas as pd
from collections import Counter
import jieba.posseg as pseg
from tqdm import tqdm
from pyecharts import options as opts
from pyecharts.charts import Bar, Page

# 1. 定义动词词性标记
verb_pos = ['v', 'vd', 'vn', 'vshi', 'vyou', 'vf', 'vx', 'vi', 'vl', 'vg']

# 2. 创建输出目录
output_dir = 'D:/out3'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 3. 读取原始数据
raw_data = pd.read_excel(r'D:\懂车帝回答e.xlsx', 'Sheet2')
time_col = '时间调整'  # 时间列名
text_col = '问题标题'  # 文本列名

# 4. 获取时间列表并去重
time_list = raw_data[time_col].drop_duplicates()

# 5. 准备可视化页面
page = Page()

for month in tqdm(time_list, desc='处理各月份数据'):
    # 提取当月文本
    texts = raw_data[raw_data[time_col] == month][text_col].astype(str).tolist()
    combined_text = '\r\n'.join(texts)

    # 分词和词性标注
    words = pseg.cut(combined_text)

    # 统计词频（只保留动词）
    word_freq = Counter()
    for word, flag in words:
        if flag in verb_pos:
            word_freq[(word, flag)] += 1

    # 转换为DataFrame
    verb_df = pd.DataFrame(
        [(word, pos, count) for (word, pos), count in word_freq.items()],
        columns=['分词', '词性', '词频']
    ).sort_values('词频', ascending=False)

    # 保存到文件
    output_file = os.path.join(output_dir, f'{month}-动词统计.xlsx')
    verb_df.to_excel(output_file, index=False)

    # 准备可视化数据（取前15个）
    top_verbs = verb_df.head(15)

    # 生成柱状图
    chart = (
        Bar()
        .add_xaxis(top_verbs['分词'].tolist())
        .add_yaxis(str(month), top_verbs['词频'].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{month} 高频动词"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
            toolbox_opts=opts.ToolboxOpts()
        )
    )
    page.add(chart)

# 6. 保存可视化结果
output_html = os.path.join(output_dir, '懂车帝各月动词使用情况.html')
page.render(output_html)
print(f'处理完成！结果已保存到 {output_dir}')