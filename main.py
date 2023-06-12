from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import os
import sys
from datetime import datetime

application_path = os.path.dirname(sys.executable)

now = datetime.now()


def main():
    json_file = open(os.path.join(application_path,'configs.json'))
    configs = json.load(json_file)
    # Specify the path to the ChromeDriver executable
    chrome_driver_path = os.path.join(application_path, 'chromedriver.exe')

    options = Options()
    options.add_experimental_option('detach', True)
    # options.headless = True

    # Create an instance of Chrome WebDriver
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    # Open the webpage
    driver.get('https://katteb.com/ar/sign-in/')
    driver.maximize_window()

    email_element = driver.find_element(By.ID, 'username')
    email_element.send_keys(configs['katteb_email'])
    password_element = driver.find_element(By.ID, 'password')
    password_element.send_keys(configs['katteb_password'])

    # Find and click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button.validation-submit-btn')
    login_button.click()

    wait = WebDriverWait(driver, 15)
    wait.until(EC.url_contains('/dashboard/'))

    kaleema_admin_email = configs['admin_kaleema_email']
    kaleema_admin_password = configs['admin_kaleema_password']
    main_window_handle = driver.current_window_handle

    driver.execute_script("window.open('about:blank', 'new_window')")

    # Switch to the new window
    driver.switch_to.window("new_window")

    # Navigate to a URL
    url = "https://kalmeeh.com/"
    driver.get(url)

    login_popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'li.has-title.popup-login-icon.menu-item.custom-menu-link'))
    )
    login_popup.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.container-wrapper'))
    )

    email_field = driver.find_element(By.NAME, 'log')
    password_field = driver.find_element(By.NAME, 'pwd')

    email_field.send_keys(kaleema_admin_email)
    password_field.send_keys(kaleema_admin_password)

    kaleema_submit = driver.find_element(By.CSS_SELECTOR, 'button.button.fullwidth.login-submit')
    kaleema_submit.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains('https://kalmeeh.com/wp-login.php')
    )

    captcha = driver.find_element(By.XPATH, '//label[@for="jetpack_protect_answer"]')
    captcha_result = eval(captcha.text.replace('&nbsp', '').replace(' ', '').replace('=', ''))

    captcha_input = driver.find_element(By.ID, 'jetpack_protect_answer')
    captcha_input.send_keys(captcha_result)

    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    email_field = driver.find_element(By.NAME, 'log')
    password_field = driver.find_element(By.NAME, 'pwd')

    email_field.send_keys(kaleema_admin_email)
    password_field.send_keys(kaleema_admin_password)

    driver.find_element(By.CSS_SELECTOR, 'input[name="wp-submit"]').click()

    WebDriverWait(driver, 10).until(
        EC.url_contains('https://kalmeeh.com/wp-admin/')
    )

    driver.switch_to.window(main_window_handle)

    def make_article(headline):
        driver.switch_to.window(main_window_handle)
        driver.get('https://katteb.com/ar/dashboard/generate-full-article/')
        form = driver.find_elements(By.TAG_NAME, 'multistep-form-body-field')

        form[0].click()
        form[0].find_element(By.NAME, 'topic_title').send_keys(headline)

        form[1].click()
        arabic_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                    f'multistep-form-body-field-fill-selectbox-item[data-value="{configs["language_code"]}"]')))
        arabic_option.click()

        form[2].click()
        search = driver.find_elements(By.CSS_SELECTOR, 'input.-multistep-selectbox-search')[-1]
        driver.execute_script(f"arguments[0].value = '{configs['audience_full_country_name']}';", search)
        search.send_keys(Keys.ENTER)
        jordan_aud = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                    f'multistep-form-body-field-fill-selectbox-item[data-value="{configs["audience_country_code"]}"'))
        )
        jordan_aud.click()

        driver.implicitly_wait(2)

        title = form[3].click()
        numbers_of_lines = driver.find_element(By.ID, 'topic_numberofwords')
        driver.execute_script(f"arguments[0].value = {configs['length_of_article']}", numbers_of_lines)

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "multistep-form-next"))
        )

        next_button.click()

        write_button = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.-start-generating-button.hoverable.activable'))
        )

        write_button.click()

        show_article = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'عرض المقال'))
        )

        show_article.click()

        articles_holder = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'div.fr-element.fr-view'))
        )  # Replace 'your_div_id' with the actual ID of the div element

        ActionChains(driver).click(articles_holder).key_down(Keys.CONTROL).send_keys('a').send_keys('c').key_up(
            Keys.CONTROL).perform()

        # Copy the selected text to clipboard
        driver.execute_script('document.execCommand("copy");')

        driver.switch_to.window('new_window')

        driver.get('https://kalmeeh.com/wp-admin/post-new.php')

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[aria-label="إضافة عنوان"]'))
        )

        headline_x = driver.find_element(By.CSS_SELECTOR, 'h1[aria-label="إضافة عنوان"]')

        driver.execute_script('arguments[0].textContent = arguments[1];', headline_x, headline)

        medical_checkbox = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'label[for="inspector-checkbox-control-6"]'))
        )
        health_checkbox = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'label[for="inspector-checkbox-control-5"]'))
        )

        medical_checkbox.click()
        health_checkbox.click()

        add_component = driver.find_element(By.CSS_SELECTOR,
                                            'button.components-button.block-editor-inserter__toggle.has-icon')
        add_component.click()

        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input.components-search-control__input'))
        )

        search.send_keys('Table')

        driver.find_element(By.CSS_SELECTOR,
                            'button.components-button.block-editor-block-types-list__item.editor-block-list-item-rank-math-toc-block').click()
        headline_x.click()

        p_document = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.block-editor-default-block-appender__content'))
        )

        p_document.click()

        p_role_document = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'p.block-editor-rich-text__editable.block-editor-block-list__block.wp-block.is-selected.wp-block-paragraph.rich-text'))
        )
        ActionChains(driver).click(p_role_document).key_down(Keys.CONTROL).send_keys('v').key_up(
            Keys.CONTROL).perform()

        draft_button = driver.find_element(By.CSS_SELECTOR, 'button.components-button.is-tertiary')
        draft_button.click()

    headlines_file = os.path.join(application_path,"headlines.txt")
    with open(headlines_file,mode='r',encoding='utf-8',errors='ignore') as file:
            for line in file.readlines():
                make_article(line)

    driver.quit()


if __name__ == '__main__':
    main()