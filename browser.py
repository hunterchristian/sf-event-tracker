from selenium import webdriver

def getPageSource(url):
  """
  Returns source code of a web page as a string
  """

  browser = webdriver.Chrome()
  browser.get(url)
  page_source = browser.page_source
  browser.close()

  return page_source