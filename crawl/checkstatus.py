import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys


def get_status(url):
    try:
        response= requests.get(url, timeout=1)
        status= response.status_code
        # print(url, status)
        if status == 200:
            return url
    except:
        pass

def getlink(file):
    f = open(file, "r")
    return f.read().splitlines()

def checkempty(s):
    if isinstance(s, str):
        return(s)
    else:
        pass

f = open('D:\\Code\\dephish\\front-end\\url\\whitelist\\gov_domain(w).txt', 'w+')
c = 0
for i in getlink('D:\\Code\\dephish\\front-end\\url\\whitelist\\gov_domain.txt'):
    s = get_status("https://" + i)
    # print(c)
    if s:
        print(s)
    #     f.write(s+"\n")
    # else:
    #     s2 = get_status("http://" + i)
    #     if s2:
    #         f.write(s2+"\n")
    # s = get_status(i)
    # print(c)
    # if s:
    #     f.write(s+"\n")
    # c+=1