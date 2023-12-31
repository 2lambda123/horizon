#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import selenium.common.exceptions as Exceptions
from selenium.webdriver.common import by

from openstack_dashboard.test.integration_tests.pages import navigation
from openstack_dashboard.test.integration_tests.pages import pageobject
from openstack_dashboard.test.integration_tests.regions import bars
from openstack_dashboard.test.integration_tests.regions import menus
from openstack_dashboard.test.integration_tests.regions import messages


class BasePage(pageobject.PageObject):
    """Base class for all dashboard page objects."""

    _heading_locator = (by.By.CSS_SELECTOR, 'div.page-header > h2')
    _help_page_brand = (by.By.CSS_SELECTOR, '.navbar-brand')
    _default_message_locator = (by.By.CSS_SELECTOR, 'div.alert')

    @property
    def heading(self):
        return self._get_element(*self._heading_locator)

    @property
    def topbar(self):
        return bars.TopBarRegion(self.driver, self.conf)

    @property
    def is_logged_in(self):
        return self.topbar.is_logged_in

    @property
    def navaccordion(self):
        return menus.NavigationAccordionRegion(self.driver, self.conf)

    def go_to_login_page(self):
        self.driver.get(self.login_url)

    def go_to_home_page(self):
        self.topbar.brand.click()

    def log_out(self):
        self.topbar.user_dropdown_menu.click_on_logout()

    def go_to_help_page(self):
        self.topbar.user_dropdown_menu.click_on_help()

    def is_help_page(self):
        self._wait_till_element_visible(self._help_page_brand)

    def choose_theme(self, theme_name):
        self.topbar.user_dropdown_menu.choose_theme(theme_name)

    def find_all_messages(self):
        self.driver.implicitly_wait(self.conf.selenium.message_implicit_wait)
        try:
            msg_elements = self.driver.find_elements(
                *self._default_message_locator)
        except Exceptions.NoSuchElementException:
            msg_elements = []
        finally:
            self._turn_on_implicit_wait()
            return msg_elements

    def find_messages_and_dismiss(self):
        messages_level_present = set()
        for message_element in self.find_all_messages():
            message = messages.MessageRegion(
                self.driver, self.conf, message_element)
            messages_level_present.add(message.message_class)
            message.close()
        return messages_level_present

    def change_project(self, name):
        self.topbar.user_dropdown_project.click_on_project(name)


class BaseNavigationPage(BasePage, navigation.Navigation):
    pass
