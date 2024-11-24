import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import HtmlTestRunner 


class LoginSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.base_url = "http://localhost:3000"
    
    def setUp(self):
        self.driver.get(self.base_url)
    
    def test_login_success(self):
        driver = self.driver
        try:
            username = driver.find_element(By.ID, "username")
            password = driver.find_element(By.ID, "password")
            username.send_keys("admin")
            password.send_keys("1234")
            login_button = driver.find_element(By.TAG_NAME, "button")
            login_button.click()
            time.sleep(3)
            current_url = driver.current_url
            self.assertIn("/main", current_url, "No redirigió a la página principal")
            self.assertIn("¡Bienvenido a la Página Principal!", driver.page_source, "El mensaje de bienvenida no apareció")
        except Exception as e:
            raise

    def test_login_failure(self):
        driver = self.driver
        try:
            username = driver.find_element(By.ID, "username")
            password = driver.find_element(By.ID, "password")
            username.send_keys("wrong_user")
            password.send_keys("wrong_pass")
            login_button = driver.find_element(By.TAG_NAME, "button")
            login_button.click()
            time.sleep(2)
            alert = driver.switch_to.alert
            alert_text = alert.text
            self.assertIn("Credenciales inválidas", alert_text, "El mensaje de alerta es incorrecto")
            alert.accept()
            self.assertNotIn("/main", driver.current_url, "Redirigió incorrectamente a la página principal")
        except Exception as e:
            raise

    def test_redirect_protection(self):
        driver = self.driver
        try:
            driver.get(f"{self.base_url}/main")
            time.sleep(2)
            current_url = driver.current_url
            self.assertEqual(current_url, f"{self.base_url}/", "No redirigió al login correctamente")
        except Exception as e:
            raise

    def test_logout(self):
        driver = self.driver
        try:
            username = driver.find_element(By.ID, "username")
            password = driver.find_element(By.ID, "password")
            username.send_keys("admin")
            password.send_keys("1234")
            login_button = driver.find_element(By.TAG_NAME, "button")
            login_button.click()
            time.sleep(3)
            logout_button = driver.find_element(By.LINK_TEXT, "Logout")
            logout_button.click()
            time.sleep(2)
            current_url = driver.current_url
            self.assertEqual(current_url, f"{self.base_url}/", "No redirigió al login después del logout")
            driver.get(f"{self.base_url}/main")
            time.sleep(2)
            self.assertEqual(driver.current_url, f"{self.base_url}/", "Accedió a la página principal sin autenticación")
        except Exception as e:
            raise
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            output="reportes",
            report_name="Reporte_Tests_Login",
            combine_reports=True,
        )
    )
