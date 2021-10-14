# encoding: utf-8

import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

class Selenium():

  def __init__(self, tmp_folder, browser=False):

    chrome_options = webdriver.ChromeOptions()

    ## stop any orphaned processes
    #print('stopping orphaned processes..')
    #os.system('killall chromedriver')
    #os.system('killall chromium-browser')

    self._tmp_folder = tmp_folder

    ## set chromedriver options

    if browser == False:
      chrome_options.add_argument('--headless')
    
    if browser == True:
      chrome_options.add_argument('--window-size=1440×764')

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    chrome_options.add_argument('--homedir={}'.format(tmp_folder))
    chrome_options.add_argument('--data-path={}'.format(tmp_folder + '/data-path'))
    chrome_options.add_argument('--disk-cache-dir={}'.format(tmp_folder + '/cache-dir'))
    chrome_options.add_argument('--user-data-dir={}'.format(tmp_folder + '/user-data'))
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--log-path={}'.format(tmp_folder + '/chromedriver.log'))

    ## set experimental chromedriver options
    prefs = {
    "download.default_directory": tmp_folder + '/downloads',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,
    "safebrowsing.disable_download_protection": True,
    }

    chrome_options.add_experimental_option('prefs', prefs)


    ## instantiate chromedriver
    self._driver = webdriver.Chrome(chrome_options=chrome_options)
    

    ## hack to enable downloads in headless mode
    self._driver.command_executor._commands['send_command'] = (
        'POST',
        '/session/$sessionId/chromium/send_command'
        )

    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': tmp_folder + '/downloads'
            }
        }

    self._driver.execute('send_command', params)
    ## end init

  # selenium handlers

  def add_cookie(self, dict):
    self._driver.add_cookie(dict)

  def clear_input_value(self, xpath, len):
    elem_send = self._driver.find_element_by_xpath(xpath)
    for i in range(len):
      elem_send.send_keys(getattr(Keys, 'BACKSPACE'))

  def click(self, xpath):
    elem_click = self._driver.find_element_by_xpath(xpath)
    elem_click.click()

  def click_css(self, css):
    elem_click = self._driver.find_element_by_css_selector(css)
    elem_click.click()

  def click_element(self, element):
    element.click()

  def close(self):
    self._driver.close()
    self._driver.quit()
    os.system('killall chromedriver')
    os.system('killall chromium-browser')

  def current_url(self):
    return self._driver.current_url

  def delete_cookie(self, name):
    return self._driver.delete_cookie(name)

  def delete_cookies(self):
    return self._driver.delete_all_cookies()
  
  def edit_css_class(self, element, node, value):
    self._driver.execute_script("document.getElementsByClassName(arguments[0])[0].style." + node + "='" + value + "';", element) # 
    
  def find_elements(self, xpath):
    return self._driver.find_elements_by_xpath(xpath)

  def get_cookie(self, name):
    return self._driver.get_cookie(name)
    
  def get_cookies(self):
    return self._driver.get_cookies()

  def get_inner_html(self, xpath):
    elem_value = self._driver.find_element_by_xpath(xpath)
    return elem_value.get_attribute('innerHTML')

  def get_screenshot(self, filename):
    self._driver.save_screenshot(self._tmp_folder + '/screenshots/' + filename + '.png')

  def get_url(self, url):
    self._driver.get(url)

  def scroll_window(self, x, y):
    self._driver.execute_script('window.scrollBy(arguments[0],arguments[1]);', x, y)

  def scroll_element(self, x, y):
    self._driver.execute_script('element.scrollBy(arguments[0],arguments[1]);', x, y)

  def scroll_to_element(self, element, position='top'):
    if position == 'top':
      self._driver.execute_script('arguments[0].scrollIntoView(true);', element);
    else:
      self._driver.execute_script('arguments[0].scrollIntoView(false);', element);

  def scroll_to_xpath(self, xpath, position='top'):
    if position == 'top':
      self._driver.execute_script('document.evaluate(arguments[0],document,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null).snapshotItem(0).scrollIntoView(true);', xpath)
    else:
      self._driver.execute_script('document.evaluate(arguments[0],document,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null).snapshotItem(0).scrollIntoView(false);', xpath)

  def select_by_value(self, xpath, value):
    elem_select = Select(self._driver.find_element_by_xpath(xpath))
    elem_select.select_by_value(value)

  def select_xpath(self, xpath):
    elem_select = Select(self._driver.find_element_by_xpath(xpath))
    elem_select.select_by_value(value)

  def set_input_value(self, xpath, value):
    elem_send = self._driver.find_element_by_xpath(xpath)
    elem_send.clear()
    elem_send.send_keys(value)

  def set_input_value_keys(self, xpath, value):
    elem_send = self._driver.find_element_by_xpath(xpath)
    #elem_send.clear()
    elem_send.send_keys(getattr(Keys, value))

  def set_input_value_css(self, css, value):
    elem_send = self._driver.find_element_by_css_selector(css)
    elem_send.clear()
    elem_send.send_keys(value)

  def switch_to_frame(self, name):
    self._driver.switch_to.frame(name)

  def switch_to_default_content(self):
    self._driver.switch_to_default_content()

  def version_download(self, version):
    # use to handle multiple downloads with identical filenames
    folder = self._tmp_folder + '/downloads/'

    if os.listdir(folder):
      filename = max([f for f in os.listdir(folder)], key=lambda xa : os.path.getctime(os.path.join(folder,xa)))
      time_counter = 0

      while '.part' in filename:
        time.sleep(1)
        time_counter += 1
        if time_counter > 60:
          raise Exception('Waited too long for file to download')
              
      filename = max([f for f in os.listdir(folder)], key=lambda xa : os.path.getctime(os.path.join(folder,xa)))
      newfilename = '{}{}{}{}{}'.format(filename.split('.')[0],'_',version,'.',filename.split('.')[1])
      os.rename(os.path.join(folder, filename), os.path.join(folder, newfilename))
      
    else:
        pass

  def wait_for_element_id(self, element_id):
    elem_wait = self._driver.WebDriverWait(self._driver, 30).until(
    EC.presence_of_element_located((By.ID, element_id))
    )

  def wait_for_element_css(self, element_css):
    elem_wait = WebDriverWait(self._driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, element_css))
    )
