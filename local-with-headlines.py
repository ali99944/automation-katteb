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
date = now.strftime("%d%m%y")


def main():
    json_file = open('configs.json')
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

    keywords_path = 'keywords.txt'
    keywords = open(keywords_path, mode='r', encoding='utf-8', errors='ignore')

    def makeTitles(keyword):
        driver.switch_to.window(main_window_handle)
        if driver.current_url.count != 'https://katteb.com/ar/dashboard/':
            driver.get('https://katteb.com/ar/dashboard/')

        WebDriverWait(driver, 10).until(
            EC.url_matches('https://katteb.com/ar/dashboard/')
        )

        try:
            iframe_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'LOU_PLAYER_MAINFRAME'))
            )
            driver.switch_to.frame(iframe_element)
            close_start_dialog = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-gPpHY.ilrxnI"))
            )

            close_start_dialog.click()

        except:
            pass

        driver.switch_to.window(driver.current_window_handle)

        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="owl-item active"]//a[@href]'))
        )

        for link in links:
            match_word = "عناوين جذابة"
            if link.get_attribute('textContent') == match_word or link.get_attribute('textContent') == 'Headlines':
                driver.execute_script("arguments[0].click();", link)


        # driver.switch_to.window(driver.window_handles[-1])
        dropDown = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'div.-katteb-generator-drawer-templates-button.hoverable.activable'))
        )

        driver.execute_script("arguments[0].click();", dropDown)

        dropDownItem = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//a[@href="https://katteb.com/ar/dashboard/generate/headlines/"]'))
        )

        driver.execute_script("arguments[0].click();", dropDownItem)




        # Find the textarea element inside the popup
        textarea = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "-templatefield-headlines_selectedTab_h1"))
        )

        driver.execute_script(f"arguments[0].value = '{keyword}';", textarea)

        # sgDropDown = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, ''))
        # )
        #
        # lanDropDown = WebDriverWait(driver,10).until(
        #     EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/form/div/generate-phase-root-body-tab/divelem[1]/divelem[1]/divelem[1]/divelem[2]/divelem/divelem[1]'))
        # )
        #
        # driver.execute_script("arguments[0].click();", sgDropDown)

        pickers = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'divelem.-selectbox'))
        )

        print("pickers are ")
        print(pickers)
        print(pickers[0])
        print(pickers[1])

        # driver.execute_script("arguments[0].click", pickers[1])
        pickers[1].click()
        arabic_choice = driver.find_element(By.XPATH, f'//divelem[@data-widget-value="{configs["language_code"]}"]')
        arabic_choice.click()

        pickers[0].click()

        suggestion =WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH, '//divelem[@data-widget-value="3"]'))
        )
        suggestion.click()
        # driver.execute_script("arguments[0].click", suggestion)

        # Find the custom element using its attribute values
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "generate-button.hoverable.activable"))
        )

        # Execute JavaScript to click on the custom element
        driver.execute_script("arguments[0].click();", button)

        # Switch back to the main window
        driver.switch_to.window(driver.window_handles[0])

        # # Close the popup window
        # driver.close()

        wait = WebDriverWait(driver, 90)
        wait.until(EC.url_contains('/activities/'))

        print('url changed to done genration')

        elements = driver.find_element(By.CSS_SELECTOR, 'div.fr-element.fr-view')
        paragraphs = elements.find_elements(By.TAG_NAME, 'p')
        # Remove numbers and dots, and split the text into lines
        headlines = []
        for paragraph in paragraphs:
            lines = [line.strip().strip("1234567890.-[] ") for line in paragraph.text.splitlines() if line.strip()]
            headlines.extend(lines)

        # Print each line and store them in an array
        headlines_file = f"headlines/headlines-{date}.txt"
        try:
            with open(headlines_file, mode='w', encoding='utf-8', errors='ignore') as file:
                for headline in headlines:
                    file.write(f"{headline}\n")
        except:
            os.mkdir('headlines')
            with open(headlines_file, mode='w', encoding='utf-8', errors='ignore') as file:
                for headline in headlines:
                    file.write(f"{headline}\n")

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

        for headline in headlines:
            make_article(headline)

    for keyword in keywords:
        keyword = keyword.replace('\n', '')
        makeTitles(keyword)

    driver.quit()


if __name__ == '__main__':
    main()