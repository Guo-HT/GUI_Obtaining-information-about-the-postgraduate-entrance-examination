# GUI-硕士研究生招生考试信息获取

#### 介绍
-  从中国研究生信息网中获取硕士研究生招生考试爬取用户输入专业对应的所有开设院校、各院校开设所有研究方向及各方向的部分考试范围（如：数学、专业课）。
-  数据分别为：
    （学校代码）学校名称 | 研招网对应网址 | 所在地 | - | 开设院系 | 研究方向 | 链接 | 考试范围（仅业务课）|-[ 开设院系 | 研究方向 | 链接 | 考试范围（仅业务课）]


#### 软件架构
- 通过python语言，主要通过requests模块获取数据，用json、lxml模块进行数据解析及定位，xlwt模块对.xls文件的写操作。
- 通过Qt框架完成界面部分

#### 安装说明

1.  pip install requests
2.  pip install lxml
3.  pip install xlwt
4.  pip install Sip  
5.  pip install PyQt5
6.  pip install PyQt5-tools
7.  pip install retry


#### 使用说明

1.  从下拉菜单中选中希望获取信息的专业
2.  在文本框中输入想要保存文件的名称
3.  在单选框中选择需要保存的文件类型
4.  点击 “确定” 按钮
5.  从同级目录中打开对应文件


#### *注：
1.  如有数据遗漏、错误，一切以研招网、学校网站数据为准。作者不承担任何责任！！！
2.  如果程序闪退，请确定网络情况，稍后重试。
3.  三项输入均为必填。

### 制作不易，欢迎扫码支持
![QRCode1](https://images.gitee.com/uploads/images/2021/0202/222055_b3da7d2b_8545662.png "alipay-qrcode.png")
![QRCode2](https://images.gitee.com/uploads/images/2021/0202/222150_0ef18ad8_8545662.png "wechatpay-qrcode.png")
