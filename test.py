from selenium import webdriver
from selenium.webdriver.edge.options import Options

options = Options()
driver = webdriver.Edge(options=options)
driver.get("https://hh.ru/vacancy/126828244?query=Python&hhtmFrom=vacancy_search_list")
print(driver.title)
driver.quit()