# import webdriver
from selenium import webdriver
 
# create webdriver object
driver = webdriver.Chrome()
 
# URL of the website
url = "https://www.geeksforgeeks.org/"
 
# Opening the URL
driver.get(url)
 
# Getting current URL source code
get_source = driver.page_source
 
# Text you want to search
search_text = "Floor"
 
# print True if text is present else False
print(search_text in get_source)
