from . import config
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UITest:
    driver: WebDriver

    def submit_modify(self, content, item_type='MoinMoin'):
        driver = self.driver
        if item_type == 'HTML':
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//*[@id='cke_contents_f_content_form_data_text']/iframe")))
            text_area = driver.find_elements(By.XPATH, '//body')[0]
        else:
            text_area = driver.find_element(By.ID, "f_content_form_data_text")
        text_area.send_keys(content)
        if item_type == 'HTML':
            driver.switch_to.parent_frame()
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "moin-save-text-button")))
        button.click()

    def create_wiki_item(self, item_name, item_type='MoinMoin'):
        """Creates a new wiki item with name 'item_name'"""
        driver = self.driver
        driver.get(config.BASE_URL + "/" + item_name)
        driver.find_element(By.LINK_TEXT, item_type).click()
        self.submit_modify("This is a test item\n", item_type)
