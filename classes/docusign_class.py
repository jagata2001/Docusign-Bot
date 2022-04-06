from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from time import sleep
from sys import exit

class Docusign:
    def __init__(self,url,delay=10):
        self.url = url
        self.driver = webdriver.Chrome(executable_path="./chromedriver")
        self.driver.maximize_window()
        self.driver.implicitly_wait(delay)

    def next_button_find_click(self,class_name):
        button = self.driver.find_element_by_class_name(class_name)
        button.click()

    def login(self,username,password):
        self.driver.get(self.url)
        try:
            email_input = self.driver.find_element_by_name("email")
            email_input.send_keys(username)
            self.next_button_find_click("olv-button.olv-ignore-transform.css-10u8ymx")
            password_input = self.driver.find_element_by_name("password")
            password_input.send_keys(password)
            self.next_button_find_click("olv-button.olv-ignore-transform.css-10u8ymx")
            #Check if successfully logged in
            WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located((By.CLASS_NAME, "olv-avatar.olv-ignore-transform.css-xg4di2"))
            )
        except NoSuchElementException:
            exit("Can't lacate element in login function")
        except TimeoutException:
            exit("Username or password is incorrect.\nor Something went wrong!")
        except Exception as e:
            exit(f"Login function something went wrong: {e}")

    def load_templates_page(self):
        try:
            templates_page = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='css-1lyhfj9']/span[text()='Templates']/parent::button"))
            )
            templates_page.click()
        except TimeoutException:
            exit("Can't locate templates page button")
        except StaleElementReferenceException:
            self.driver.find_element_by_xpath("//button[@class='css-1lyhfj9']/span[text()='Templates']/parent::button").click()
        except Exception as e:
            exit(f"Load template page function something went wrong: {e}")

    def open_more_options_click_edit(self,template_name,prerform={"open_menu":True,"click_on_edit":True},current_try=0,max_try=6):
        if current_try>max_try:
            return False
        if prerform["open_menu"]:
            try:
                self.driver.find_element_by_xpath(f"//div[@class='u-ellipsis' and text()='{template_name}']/ancestor::tr//button[@class='olv-button olv-ignore-transform css-kjjrx0']").click()
            except StaleElementReferenceException:
                print(f"second try of clicking on more options try: {current_try}")
                current_try+=1
                return self.open_more_options_click_edit(template_name,prerform,current_try,max_try)
            except NoSuchElementException:
                exit(f"Can't lacate more options button in open template edit function")
            except Exception as e:
                exit(f"Open template edit page 'open options' something went wrong: {e}")

        if prerform["click_on_edit"]:
            try:
                self.driver.find_element_by_xpath("//ul[@role='menu']/li/button/span[text()='Edit']/parent::button").click()
            except StaleElementReferenceException:
                print("second try of clicking on edit")
                current_try+=1
                prerform={"open_menu":False,"click_on_edit":True}
                return self.open_more_options_click_edit(template_name,prerform,current_try,max_try)
            except NoSuchElementException:
                print("Can't lacate edit button in open template edit function")
                current_try+=1
                prerform={"open_menu":True,"click_on_edit":True}
                return self.open_more_options_click_edit(template_name,prerform,current_try,max_try)
            except Exception as e:
                exit(f"Open template edit page 'edit button' something went wrong: {e}")
        return True

    def open_template_edit_page(self,template_name):
        #wait for the element presence
        wait = WebDriverWait(self.driver, 15)
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, f"//div[@class='u-ellipsis' and text()='{template_name}']"))
            )
        except TimeoutException:
            exit("Can't locate some element in open template edit function")
        except Exception as e:
            exit(f"Open template edit page something went wrong: {e}")

        action = self.open_more_options_click_edit(template_name)
        print(f"perform open of more options and click on edit: {action}")
        # #open more options
        # try:
        #     self.driver.find_element_by_class_name("olv-button.olv-ignore-transform.css-kjjrx0").click()
        # except StaleElementReferenceException:
        #     print("second try of clicking on more options")
        #     self.driver.find_element_by_class_name("olv-button.olv-ignore-transform.css-kjjrx0").click()
        # except NoSuchElementException:
        #     exit("Can't lacate more options button in open template edit function")
        # except Exception as e:
        #     exit(f"Open template edit page 'open options' something went wrong: {e}")
        #
        # #click on edit button in menu
        # try:
        #     self.driver.find_element_by_xpath("//ul[@role='menu']/li/button/span[text()='Edit']/parent::button").click()
        # except StaleElementReferenceException:
        #     print("second try of clicking on edit")
        #     self.driver.find_element_by_xpath("//ul[@role='menu']/li/button/span[text()='Edit']/parent::button").click()
        # except NoSuchElementException:
        #     exit("Can't lacate edit button in open template edit function")
        # except Exception as e:
        #     exit(f"Open template edit page 'edit button' something went wrong: {e}")

        #end section
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-qa='uploaded-file']"))
            )
            self.next_button_find_click("olv-button.olv-ignore-transform.css-10u8ymx")
            self.next_button_find_click("olv-button.olv-ignore-transform.css-10u8ymx")
        except NoSuchElementException:
            exit("Can't find next button in open template edit function")
        except TimeoutException:
            exit(f"Open template edit page cant locate upload file div")
        except Exception as e:
            exit(f"Open template edit page 'end section' something went wrong: {e}")

    def custom_text_check(self,elements,wait,text,delay=0.125):
        for _ in range(int(wait/delay)):
            element_text = " ".join([element.text for element in elements]).strip()
            if element_text==text:
                return True
            sleep(delay)
        return False

    def input_field_text_validation(self,parent,input,text,max_try=8):
        text=text.strip()
        for _ in range(max_try):
            input.click()
            input.send_keys(Keys.CONTROL + "a")
            input.send_keys(Keys.DELETE)
            input.send_keys(text)
            tspan = parent.find_elements_by_tag_name("tspan")
            check = self.custom_text_check(tspan,5,text)
            if text == input.text and check:
                return True
        return False
    def edit_template(self,data=None):
        try:
            input_fields = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[@data-view-name='DataTabView']"))
            )
            for i,input in enumerate(input_fields):
                    rect = input.find_element_by_xpath("//*[local-name()='rect' and  @fill='#ffd65b']")
                    rect.click()
                    textarea = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.TAG_NAME, "textarea"))
                    )
                    text_validation = self.input_field_text_validation(input,textarea,f"hey you {i}")
                    print(f"text validation: {text_validation}")
            self.next_button_find_click("olv-button.olv-ignore-transform.css-10u8ymx")
            self.next_button_find_click("olv-button.olv-ignore-transform.css-10u8ymx")
        except NoSuchElementException:
            exit("Can't find some element in edit template function")
        except TimeoutException:
            exit(f"Can't locate input fields in edit template function")
        except Exception as e:
            exit(f"Edit template something went wrong: {e}")

    def use_template(self,name,email):
        wait = WebDriverWait(self.driver, 15)
        try:
            use_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "olv-button.olv-ignore-transform.css-c3k90z"))
            )
            use_button.click()
            input_fields = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//input[@data-qa='recipient-name' or @data-qa='recipient-email']"))
            )
            #name field
            input_fields[0].send_keys(name)
            #email field
            input_fields[1].send_keys(email)

            #send
            sleep(1)
            self.driver.find_element_by_xpath("//button[@data-qa='quick-send-envelope-send']").click()
        except NoSuchElementException:
            exit("Can't find some element in use template function")
        except TimeoutException:
            exit(f"Can't locate some element in use template function")
        except Exception as e:
            exit(f"Use template something went wrong: {e}")

        try:
            wait.until(
                                                      #//h1[@class='emptyState_title' and text()='Your document is on its way.']
                EC.element_to_be_clickable((By.XPATH, "//h1[@class='emptyState_title']"))
            )
        except TimeoutException:
            exit("Can't find success message after send mail")
        except Exception as e:
            exit("Something went wrong during checking mail status")
    def __del__(self):
        self.driver.close()
        pass
