import os.path
import pickle
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from scrapper.models import LinkedInProfile


class Profiles:
    def __init__(self):
        self.time = random.randint(20, 30)
        if not os.path.exists("data"):
            os.makedirs("data")

        print("Starting driver")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def login(self):
        print("Logging in")
        self.driver.get("https://www.linkedin.com/login")
        self.sleep()

        self.driver.find_element(by=By.ID, value='username').send_keys(email())
        self.driver.find_element(by=By.ID, value='password').send_keys(password())

        self.driver.find_element(by=By.XPATH, value="//button[@aria-label='Sign in']").click()
        self.sleep()

    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesFile:
            cookies = pickle.load(cookiesFile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def close_session(self):
        print("Closing session")
        self.driver.close()

    def sleep(self):
        second = self.time
        print(f"wait for {second} second")
        time.sleep(second)

    def get_position_data(self, profile):
        self.sleep()
        name_tag = profile.find_element_by_class_name("app-aware-link")

        name = profile.text.split('\n')[:1][0]
        linkedin_link = name_tag.get_attribute('href')
        post = profile.find_element_by_class_name("entity-result__primary-subtitle").text
        print(f"view:- {name}")
        return [name, linkedin_link, post]

    def run(self):
        self.driver.maximize_window()
        if os.path.exists("data/cookies.txt"):
            self.driver.get("https://www.linkedin.com/")
            self.load_cookie("data/cookies.txt")
            self.driver.get("https://www.linkedin.com/")
        else:
            self.login()
            self.save_cookie("data/cookies.txt")

        print("Start searching...")
        self.sleep()

        page = 1
        profile_count = 10

        for i in range(page, 8):
            try:
                self.driver.get(get_link(i))

                profiles = self.driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")

                for profile in profiles:
                    [name, linkedin_link, post] = self.get_position_data(profile)

                    try:
                        check_profile_item = LinkedInProfile.objects.filter(linkedInUrl=linkedin_link)

                        if len(check_profile_item) == 0:
                            profile_data = {
                                "fullName": name,
                                "jobTitle": post,
                                "linkedInUrl": linkedin_link
                            }
                            profile_item = LinkedInProfile.objects.create(**profile_data)
                            profile_count += 1
                            print(f"{profile_count} {name} saved to {profile_item.id}")

                        else:
                            print(f"{name} data already exists")

                    except Exception as e:
                        print(e)

                self.sleep()

            except Exception as e:
                print(e)

        print("Done scraping")


def email():
    email2 = "sameerkumar081505@gmail.com"
    return email2


def password():
    password2 = "Sameer@123"
    return password2


def get_link(page):
    link = f"https://www.linkedin.com/search/results/people/?geoUrn=%5B%22102713980%22%5D&industry=%5B%2296%22%5D" \
           f"&keywords=%22CEO%22%20OR%20%22FOUNDER%22%20OR%20%22OWNER%22&origin=FACETED_SEARCH&page={page}&sid=%3Bmk "

    all_profile_link = f"https://www.linkedin.com/search/results/people/?industry=%5B%221810%22%2C%2296%22%2C%221594" \
                       f"%22%2C%226%22%2C%224%22%5D&keywords=%22CEO%22%20OR%20%22FOUNDER%22%20OR%20%22OWNER%22&origin" \
                       f"=FACETED_SEARCH&page={page}&serviceCategory=%5B%22602%22%2C%2226904%22%5D&sid=osQ "
    return all_profile_link


def world_start_up(page):
    link = f"https://www.linkedin.com/search/results/people/?industry=%5B%2296%22%5D&keywords=%22CEO%22%20OR%20" \
           f"%22FOUNDER%22%20OR%20%22OWNER%22&origin=FACETED_SEARCH&page={page}&sid=i0q "
    return link


def get_message(name):
    message = f"Hi {name},\n" \
              "Thank you for accepting my request.\n" \
              "I'm a good Android Developer with 6 months of experience in the Kotlin language.\n" \
              "Looking forward to discussing with you if you've any requirements related to Android Developer."
    return message


CSS_SELECTOR = {
    "buttons": "div.pv-top-card-v2-ctas.pt2.display-flex",
    "employees": "span.link-without-visited-state.t-bold.t-black--light",
    "profile_detail": "div.entity-result__content.entity-result__divider.pt3.pb3.t-12.t-black--light",
    "result": "div.pb2.t-black--light.t-14",
    "profile_heading": "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words",
    "desc": "div.text-body-medium.break-words",
    "emp_button": "div.display-flex.mt2.mb1",
    "company_detail": "div.block.mt2",
    "company_website": "a.ember-view.org-top-card-primary-actions__action",
    # driver.find_elements_by_css_selector('div.artdeco-dropdown.artdeco-dropdown--placement-bottom.artdeco-dropdown--justification-left.ember-view')
    'more_button': 'div.artdeco-dropdown.artdeco-dropdown--placement-bottom.artdeco-dropdown--justification-left.ember-view',
    'more_button_dropdown': 'span.display-flex.t-normal',
    'connect_inside_button': 'button.mr2.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--secondary.ember-view',
    'add_note_button': 'button.mr1.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--secondary.ember-view',
    #             textarea.ember-text-area.ember-view.connect-button-send-invite__custom-message.mb3
    'note_area': 'textarea.ember-text-area.ember-view.connect-button-send-invite__custom-message.mb3',
    'send_button': 'button.ml1.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view',
    'connect_button': 'button.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.pvs-profile-actions__action',

}


