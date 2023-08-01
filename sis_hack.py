
from selenium import webdriver
from selenium.webdriver.common.by import By
from yaml import load, CLoader
from bs4 import BeautifulSoup
from requests import get
import lxml
import time

conf = load(open('login_details.yml'), CLoader)

sis_email = conf['sis_login']['user_name']
sis_password = conf['sis_login']['password']

driver = webdriver.Chrome()

login_url = "https://auth.galvanize.com/sign_in"
sis_url = "https://sis.galvanize.com/dashboards/students/21/days/2439/"

sis_sso_btn = "is-info"

sis_token_name = "authenticity_token"
sis_email_field = "user_email"
sis_password_field = "user_password"
sis_submit_name = "commit"

token_link_data_title = "You're Here!"


def login(
        login_url, user_name_id, user_name,
        password_id, password, submit_button_name,
        sis_url
):
    driver.get(login_url)
    # token = driver.find_element(
    #     by='name', value=sis_token_name
    # ).get_attribute('value')
    # driver.find_element(by='name', value=sis_token_name).send_keys(token)
    driver.find_element(by='id', value=user_name_id).send_keys(user_name)
    driver.find_element(by='id', value=password_id).send_keys(password)
    driver.find_element(by='name', value=submit_button_name).click()
    driver.get(sis_url)
    driver.find_element(by='name', value='csrfmiddlewaretoken').submit()
    driver.get("https://sis.galvanize.com/cohorts/21/attendance/mine/")
    # source = driver.page_source
    # source_soup = BeautifulSoup(source, 'lxml')
    token_standin = False
    while token_standin is False:
        try:
            # input_tag = source_soup.find('main').find('form').find('h1').string
            list = driver.find_element(By.TAG_NAME, 'main')
            span = list.find_element(By.TAG_NAME, "span")
            if len(span.text) > 4:
                print("***waiting for token***")
                driver.refresh()
            # print(input_tag)
                continue
            token_standin = span.text
        except Exception:
            print("***waiting for token Error***")
            driver.refresh()

    driver.find_element(by='id', value='form-token').send_keys(token_standin)
    driver.find_element(by='id', value='form-token').submit()
    time.sleep(15)
    driver.quit()


login(
    login_url, sis_email_field, sis_email,
    sis_password_field, sis_password, sis_submit_name,
    sis_url
)
# sesh = requests.session()
