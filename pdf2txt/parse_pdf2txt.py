import importlib
import sys,re,string
import random
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

importlib.reload(sys)

def parse_pdf2txt(argv):
    content = ''
    if len(argv) > 1:
        _path = argv[1]
    fp = open(_path, 'rb')  # rb以二进制读模式打开本地pdf文件
    
    # 用文件对象来创建一个pdf文档分析器
    praser_pdf = PDFParser(fp)

    # 创建一个PDF文档
    doc = PDFDocument()

    # 连接分析器 与文档对象
    praser_pdf.set_document(doc)
    doc.set_parser(praser_pdf)

    # 提供初始化密码
    # doc.initialize("123456")
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()

        # 创建一个PDF参数分析器
        laparams = LAParams()

        # 创建聚合器
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # 创建一个PDF页面解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        if len(argv) > 3:
            mlist = range(int(argv[2])-1,int(argv[3]) )
        elif len(argv) == 3:
            mlist = range(int(argv[2])-1,int(argv[2]) )    
        i = 0    
        # 循环遍历列表，每次处理一页的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            # 使用页面解释器来读取
            interpreter.process_page(page)

            # 使用聚合器获取内容
            layout = device.get_result()

            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for out in layout:
                # 判断是否含有get_text()方法，图片之类的就没有
                # if hasattr(out,"get_text"):
                if isinstance(out, LTTextBoxHorizontal):
                    if i in mlist:
                        results = out.get_text().encode('gbk','ignore')
                        content +=  str(results, encoding = 'gbk') + '\n'

            i += 1                
        return content
            
if __name__ == '__main__':         
    strs = parse_pdf2txt(sys.argv)
    #输出结果
    f = open("result.txt","w")
    s = re.findall("[a-z]+",str.lower(strs))
    #去除列表中的重复项
    l = list(set(s))
    #去除含有数字和符号，以及长度小于4的字符串
    for i in l:
        m = re.search("\d+",i)
        n = re.search("\W+",i)
        if not m and  not n and len(i)>4:
            f.write(i +"\n")
    f.close()


