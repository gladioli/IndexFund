# IndexFund
使用 Scrapy+Selenium 在天天基金网爬去指定指数类型的宽基基金，并做定投初步筛选导出xlsx

## 环境依赖
Python3.6.2
```
openpyxl==2.4.8
Scrapy==1.3.3
selenium==3.141.0
lxml==4.4.2
```

## 部署步骤
1. **clone**
```
git clone https://github.com/gladioli/IndexFund.git
```
2. **安装依赖**
```
cd IndexFund
pip install -r requriements.txt
```
3. **修改指数类型**  
打开spiders/csi_500.py,  
将[search_key](https://github.com/gladioli/IndexFund/blob/ad2684c8fa7ff680f8ade6b7dde01bc6af5dd794/spiders/csi_500.py#L13)的值修改成想要查询的指数类型，如：上证50、中证500、沪深300
```
    search_key = '中证500'
```
