from datetime import date, timedelta
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebsiteClocker:
    def __init__(self, url, username, password, driver_path="chromedriver"):
        self.url = url
        self.username = username
        self.password = password
        self.driver_path = driver_path

    @staticmethod
    def from_credentials_file(credentials_path, driver_path="chromedriver"):
        with open(credentials_path, "r") as f:
            creds = json.load(f)
        return WebsiteClocker(
            url=creds["url"],
            username=creds["clock-username"],
            password=creds["clock-password"],
            driver_path=driver_path
        )
    
    def clock_hours(self):
        options = webdriver.ChromeOptions()


        with tempfile.TemporaryDirectory() as tmpdirname:
            options.add_argument(f"user-data-dir={tmpdirname}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--headless")
            service = Service(self.driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            try:
                print("Opening login page...")
                driver.get(self.url)

                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.NAME, "emailid"))
                )
                # LOGIN
                print("Logging in...")
                driver.find_element(By.NAME, "emailid").send_keys(self.username)
                driver.find_element(By.NAME, "password").send_keys(self.password)
                driver.find_element(By.NAME, "login").click()
                # FIRST PAGE

                element_locator = (By.CSS_SELECTOR, "#tasks > div > div > h4 > profile-translation > span")
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(element_locator)
                )
                
                element_locator = (By.CSS_SELECTOR, "body > app-root > profile-layout > div > div.btp-outlet-wrapper > profile-home > div > div:nth-child(1) > p > span > profile-translation > span")  # Update selector as needed

                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(element_locator)
                )

                print("Navigating to hours page...")

                element_locator = (By.CSS_SELECTOR, "#btp-sidebar > div > ul > li:nth-child(3) > a")  # Update selector as needed

                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(element_locator)
                )

                driver.find_element(*element_locator).click()

                # WAITING FOR THE HOURS PAGE TO LOAD
                time.sleep(1)  # Optional: small delay to allow the new window to open
                windows = driver.window_handles
                driver.switch_to.window(windows[-1]) 

                print("Waiting for timesheets to load...")

                element_locator = (By.ID, "timesheettitle")  # Update selector as needed

                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(element_locator)
                )                

                # code to print sunday date in format mm/dd/yyyy
                today = date.today()
                sunday = today + timedelta(days=(6 - today.weekday()))
                link_text = sunday.strftime("%-m/%-d/%Y")  # Change this to the actual link text you want to click

                print("This week's Sunday is:", link_text)
                # print(driver.page_source)

                element_locator = (By.LINK_TEXT, link_text)  # Update selector as needed

                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(element_locator)
                )
                driver.find_element(*element_locator).click()

                print("Filling hours...")
                # MONDAY
                element_locator = (By.CSS_SELECTOR, "#txtmon0")
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(element_locator)
                )
                driver.find_element(*element_locator).click()

                element_locator = (By.CSS_SELECTOR, "#adjustmenthours > div > input")
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(element_locator)
                )
                # PUT 8
                input_box = driver.find_element(*element_locator)
                input_box.clear()
                input_box.send_keys("8")
                time.sleep(1)  # Optional: small delay to allow the new window to open

                driver.save_screenshot('screenshot1.png')
                # COPY TROUGH FRIDAY
                element_locator = (By.CSS_SELECTOR, "#assignmentfooter > div:nth-child(1) > div:nth-child(2) > button")  # Update selector as needed

                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(element_locator)
                )
                driver.find_element(*element_locator).click()
                time.sleep(1)  # Optional: small delay to allow the new window to open

                driver.save_screenshot('screenshot2.png')

                element_locator = (By.CSS_SELECTOR, "#divSites > div:nth-child(2) > div:nth-child(5) > div > div.col-sm-1.col-xs-4.weeklytimesheetdaysbackground.paddingnone.xs-border-left.ng-scope.savedtext.col-sm-push-4 > div.totalhours.hidden-xs.assignmentsavedbackground > div.col-sm-12.paddingnone.ng-pristine.ng-untouched.ng-valid.ng-binding.ng-scope")  # Replace with your selector

                # Wait for the element to be present
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(element_locator)
                )

                # Get and trim the text
                element = driver.find_element(*element_locator)
                text = element.text.strip()

                # Compare to "40"
                if text == "40.00":
                    print("Text is 40.00")
                    time.sleep(5)  # Optional: small delay to allow the new window to open

                    print("Submitting hours...")
                    element_locator = (By.CSS_SELECTOR, "#divSites > div:nth-child(2) > div:nth-child(9) > div > span")  # Update selector as needed

                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(element_locator)
                    )
                    driver.find_element(*element_locator).click()
                    time.sleep(1)  # Optional: small delay to allow the new window to open
                    driver.save_screenshot('success.png')
                    print("✅ Successfully clocked hours.")

                else:
                    print(f"❌ Text is not 40.00, it is: {text}")
            except Exception as e:
                driver.save_screenshot('bad-screenshot.png')
                print(f"❌ An error occurred: {e}")
            finally:
                time.sleep(5)
                driver.quit()

# Example usage
if __name__ == "__main__":
    # Replace with your actual login credentials
    clocker = WebsiteClocker.from_credentials_file("credentials.json", driver_path="/usr/local/bin/chromedriver")
    clocker.clock_hours()
