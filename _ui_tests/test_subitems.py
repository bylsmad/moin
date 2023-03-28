# Copyright: 2012 MoinMoin:HughPerkins
# License: GNU GPL v3 (or any later version), see LICENSE.txt for details.

"""Functional test: create subitem"""

from . import config
from . import conftest
from . import utils
from . import UITest
from selenium.webdriver.common.by import By


class TestSubitems(UITest):
    """Functional test: create subitem"""

    def setup_class(self):
        """creates some random item names for these tests"""
        self.base_item_name = "page_" + utils.generate_random_word(5)
        self.subitem_name = "subitem_" + utils.generate_random_word(5)

    def test_createsubitem(self, driver):
        """Test create subitem"""
        assert driver, 'issue in server or browser startup'
        self.driver = driver

        self.create_wiki_item(self.base_item_name)

        driver.get(config.BASE_URL + self.base_item_name)
        driver.find_element(By.CLASS_NAME, "moin-modify-button").click()
        self.submit_modify("\n[[/" + self.subitem_name + "]]\n")
        driver.find_element(By.LINK_TEXT, "/" + self.subitem_name).click()
        driver.find_element(By.LINK_TEXT, "MoinMoin").click()
        self.submit_modify("This is a test subitem")
        assert "This is a test subitem" in driver.find_element(By.ID, "moin-content-data").text
        assert driver.title.split(" - ")[0] == self.base_item_name + "/" + self.subitem_name


if __name__ == '__main__':
    # This lets us run the test directly, without using pytest
    # This is useful for example for being able to call help, eg
    # 'help(driver)', or 'help(driver.find_element(By.ID, "f_submit"))'
    testSubitems = TestSubitems()
    testSubitems.setup_class()
    testSubitems.test_createsubitem(conftest.driver())
    testSubitems.teardown_class()
