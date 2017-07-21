import time
from selenium import webdriver

driver = webdriver.Chrome('/Users/lvhao/Downloads/chromedriver')  # Optional argument, if not specified will search path.
driver.get('https://sz.lianjia.com/');
time.sleep(5)
esf_btn = driver.find_element_by_css_selector("div.nav.typeUserInfo li:first-child")
esf_btn.click()
time.sleep(5)
driver.quit()