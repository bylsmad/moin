import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from . import UITest
from . import config
from . import utils

logger = logging.getLogger(__name__)


class TestModifyHtml(UITest):
    def setup_class(self):
        """creates some random item names for these tests"""
        self.base_item_name = "page_" + utils.generate_random_word(5)

    def test_modify_html(self, driver):
        self.driver = driver
        self.create_wiki_item(self.base_item_name, 'HTML')
        driver.get(config.BASE_URL + self.base_item_name)
        driver.find_element(By.CLASS_NAME, "moin-modify-button").click()
        smiley = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'cke_button_smiley')))
        smiley.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-posinset='1']"))).click()
        self.submit_modify('', 'HTML')
        smiley_gif = f'{config.BASE_URL}+serve/ckeditor/plugins/smiley/images/regular_smile.gif'
        assert driver.find_element(By.XPATH, "//div[@id='moin-content-data']"
                                             f"//p/img[@src='{smiley_gif}'][@alt='smiley']")
