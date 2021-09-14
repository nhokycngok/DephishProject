from selenium import webdriver
import time

f = open("D:\\Code\\dephish\\front-end\\url\\whitelist\\tinnhiemmang.txt", "r").read()
count=0
for url in f.splitlines():
    count+=1
    if count==171: break
    elif 0<count<171:
        try:
            options = webdriver.ChromeOptions()
            options.add_extension("D:\\Code\\dephish\\front-end.crx")
            prefs = {"download.default_directory" : "D:\\Code\\dephish\\front-end\\db\\whitelist\\tinnhiemmang-json\\"}
            options.add_experimental_option("prefs",prefs)
            driver = webdriver.Chrome(options=options)
            if (url.endswith('*')) :
                driver.get(url.split('*')[0])
            else : 
                driver.get(url)
            driver.quit()
        except:
            print(count)
            driver.quit()
            pass
        