"""使用selenium套件擷取各銀行牌告匯率,並使用pandas套件建立dataframe物件,再使用matplotlib套件繪圖"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import matplotlib.pyplot as plt

# 建立Driver物件實體，用程式操作瀏覽器運作
driver = webdriver.Chrome()                         # 打開chrome瀏覽器

# 連線到臺灣銀行牌告匯率網頁取得牌告匯率
driver.get("https://rate.bot.com.tw/xrt?Lang=zh-TW") 
country = driver.find_elements(By.CSS_SELECTOR, "[data-table=幣別]")
buy = driver.find_elements(By.CSS_SELECTOR, "[data-table=本行現金買入]")
sell = driver.find_elements(By.CSS_SELECTOR, "[data-table=本行現金賣出]")

countrylist = [(c.text.strip().replace(")","")[-3:]) for c in country if c.text != '']
countrylist.remove("ZAR")
countrylist.remove("SEK")
buylist = [b.text for b in buy if b.text != '' and b.text != '-']
selllist = [s.text for s in sell if s.text != '' and s.text != '-']
# 建立dataframe物件
tw = dict(zip(countrylist, list(zip(buylist, selllist))))
exchangerate = pd.DataFrame(tw, index=["臺銀現金買入", "臺銀現金賣出"])
pd.set_option('display.unicode.east_asian_width', True)     # 中文標籤欄位和數據內容對齊


# 連線到兆豐銀行牌告匯率網頁取得牌告匯率
driver.get("https://www.megabank.com.tw/personal/foreign-service/forex")
time.sleep(1.5)
country2 = driver.find_elements(By.CSS_SELECTOR, "[data-loc=Name]")
buy2 = driver.find_elements(By.CSS_SELECTOR, "[data-th=現金銀行買入]")
sell2 = driver.find_elements(By.CSS_SELECTOR, "[data-th=現金銀行賣出]")

countrylist2 = [c2.text.strip()[-3:] for c2 in country2 if c2.text != '']
countrylist2.remove("ZAR")
countrylist2.remove("SEK")
buylist2 = [b2.text for b2 in buy2 if b2.text != '']
selllist2 = [s2.text for s2 in sell2 if s2.text != '']
# 建立dataframe物件
mg = dict(zip(countrylist2, list(zip(buylist2, selllist2))))
exchangerate2 = pd.DataFrame(mg, index=["兆豐現金買入", "兆豐現金賣出"])


# 連線到玉山銀行牌告匯率網頁取得牌告匯率
driver.get("https://www.esunbank.com/zh-tw/personal/deposit/rate/forex/foreign-exchange-rates") 
time.sleep(1.5)
country3 = driver.find_elements(By.CSS_SELECTOR, "[class=row]")
data3 = driver.find_elements(By.CSS_SELECTOR, "[label=現金匯率]")

countrylist3 = [c3.text[-3:] for c3 in country3 if c3.text != ''][1 : 9]
datalist3 = [d3.text for d3 in data3 if d3.text != '']
datalist3.remove('銀行買入')
buylist3 = []
selllist3 = []
for i in datalist3:
    x, y = i.split()
    buylist3.append(x)
    selllist3.append(y)
# 建立dataframe物件
es = dict(zip(countrylist3, list(zip(buylist3, selllist3))))
exchangerate3 = pd.DataFrame(es, index=["玉山現金買入", "玉山現金賣出"])


# 連線到台新銀行牌告匯率網頁取得牌告匯率
driver.get("https://www.taishinbank.com.tw/TSB/personal/deposit/lookup/realtime/") 
country4 = driver.find_elements(By.CSS_SELECTOR, "[class=td-txt]")
data4 = driver.find_elements(By.CSS_SELECTOR, "[class=currency]")

countrylist4 = [c4.text[-3:] for c4 in country4 if c4.text != ''][0 : 9]
datalist4 = [d4.text for d4 in data4 if d4.text != ''][14 : 50]
buylist4 = []
selllist4 = []
for j in range(2, 36, 4):
    if  "\n" in datalist4[j]:
        x2 , y2 = str(datalist4[j]).split("\n")
        buylist4.append(x2)
    else:
        buylist4.append(datalist4[j])
for k in range(3, 37, 4):
    if  "\n" in datalist4[k]:
        x3 , y3 = str(datalist4[k]).split("\n")
        selllist4.append(x3)
    else:
        selllist4.append(datalist4[k])
# 建立dataframe物件
ts = dict(zip(countrylist4, list(zip(buylist4, selllist4))))
exchangerate4 = pd.DataFrame(ts, index=["台新現金買入", "台新現金賣出"])

# 合併dataframe物件
all = pd.concat([exchangerate, exchangerate2, exchangerate3, exchangerate4]).astype(float)
print(all)

# 繪圖
plt.rc("font", family = "Arial Unicode MS")
fig, ax = plt.subplots(2,2)
fig.suptitle("匯率")
fig.supylabel("現金匯率")
fig.autofmt_xdate(rotation=45)

ax[0,0].set_title('USD')
ax[0,0].bar(x = all.index, height = all.get("USD"),color = ['r', 'r', 'b', 'b', 'g', 'g', 'm', 'm'], label = all.index)
ax[0,0].set_ylim(31, 33)

ax[0,1].set_title("JPY")
ax[0,1].bar(x = all.index, height = all.get("JPY"),color = ['r', 'r', 'b', 'b', 'g', 'g', 'm', 'm'])
ax[0,1].set_ylim(0.20, 0.23)

ax[1,0].set_title("EUR")
ax[1,0].bar(x = all.index, height = all.get("EUR"),color = ['r', 'r', 'b', 'b', 'g', 'g', 'm', 'm'])
ax[1,0].set_ylim(34, 37)

ax[1,1].set_title("CNY") 
ax[1,1].bar(x = all.index, height = all.get("CNY"),color = ['r', 'r', 'b', 'b', 'g', 'g', 'm', 'm'])
ax[1,1].set_ylim(4.3, 4.6)

plt.tight_layout()
fig.legend(loc='upper right')
plt.show()
