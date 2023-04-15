from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import keyring

class TestAjax:
    # run next command first time
    # keyring.set_password('system', 'qa.ajax.app.automation@gmail.com', 'type_your_password')

    users = {
        'positive': ('qa.ajax.app.automation@gmail.com', keyring.get_password('system', 'qa.ajax.app.automation@gmail.com')),
        'negative': ('test@google.com', 'test_pass')
    }

    @staticmethod
    def log_actions(driver):
        """Write Appium log to file"""
        with open('test_appium.log', 'a', encoding='utf-8') as file:
            logs = driver.get_log('logcat')
            for log in logs:
                file.write(str(log) + '\n')

    @staticmethod
    def find_element(driver, resource_id):
        """Wait for an element to appear and return it"""
        return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((AppiumBy.ID, resource_id)))

    @pytest.mark.parametrize('email, password', [users.get('positive'), users.get('negative')])
    def test_login(self, driver, email, password):
        """Test login functionality"""
        # click on the login button
        self.find_element(driver, 'com.ajaxsystems:id/login').click()
        # enter email
        self.find_element(driver, 'com.ajaxsystems:id/login').send_keys(email)
        # enter password
        self.find_element(driver, 'com.ajaxsystems:id/password').send_keys(password)
        # click on the confirm button
        self.find_element(driver, 'com.ajaxsystems:id/next').click()
        # click on the alert dismiss button
        # self.find_element(driver, 'com.ajaxsystems:id/cancel_button').click()
        # verify that the 'addFirstHub' element is displayed and contains the expected text
        assert 'start managing the security system' in self.find_element(driver, 'com.ajaxsystems:id/addFirstHub').text

        # log actions to file
        self.log_actions(driver)

    def test_sidebar(self, driver):
        """Test sidebar functionality"""
        # login with correct credentials
        self.test_login(driver, 'qa.ajax.app.automation@gmail.com', keyring.get_password('system', 'qa.ajax.app.automation@gmail.com'))
        # click on the sidebar button
        self.find_element(driver, 'com.ajaxsystems:id/menuDrawer').click()
        # verify that the sidebar is displayed
        assert self.find_element(driver, 'com.ajaxsystems:id/design_navigation_view').is_displayed()
        # verify that the 'addHub' button is displayed and enabled
        add_hub = self.find_element(driver, 'com.ajaxsystems:id/addHub')
        assert add_hub.is_displayed() and add_hub.is_enabled()
        # verify that the 'settings' button is displayed and enabled
        app_settings = self.find_element(driver, 'com.ajaxsystems:id/settings')
        assert app_settings.is_displayed() and app_settings.is_enabled()
        # verify that the 'help' button is displayed and enabled
        help_ = self.find_element(driver, 'com.ajaxsystems:id/help')
        assert help_.is_displayed() and help_.is_enabled()
        # verify that the 'logs' button is displayed and enabled
        report = self.find_element(driver, 'com.ajaxsystems:id/logs')
        assert report.is_displayed() and report.is_enabled()

        # log actions to file
        self.log_actions(driver)
        driver.quit()