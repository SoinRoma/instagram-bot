from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException

class InstagramBot():

    # Конструктор
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver/chromedriver.exe")

    # Метод для закрытия браузера
    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    # Метод логина
    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    # Метод ставит лайки по hashtag
    def like_photo_by_hashtag(self, hashtag):
        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(3)
                like_button = browser.find_element_by_xpath('//section[1]/span[1]/button').click()
                time.sleep(random.randrange(10, 30))
            except Exception as ex:
                print(ex)
                self.close_browser()

    # Метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):
        browser = self.browser

        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # Метод ставит лайк на пост по прямой ссылке
    def put_exactly_like(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "//section/main/div/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = "//section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(2)

            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

    # Метод ставит лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "//section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден!")
            time.sleep(2)

            posts_count = int(browser.find_element_by_xpath("//section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            if loops_count == 0:
                loops_count = 1

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))

            file_name = userpage.split("/")[-2]

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

            with open(f'{file_name}.txt') as file:
                urls_list = file.readlines()

                for post_url in urls_list:
                    try:
                        browser.get(post_url)
                        time.sleep(2)

                        like_button = browser.find_element_by_xpath('//section[1]/span[1]/button').click()
                        # time.sleep(random.randrange(80, 100))
                        time.sleep(2)

                        print(f"Лайк на пост: {post_url} успешно поставлен!")
                    except Exception as ex:
                        print(ex)
                        self.close_browser()

            self.close_browser()


my_bot = InstagramBot(username, password)
my_bot.login()
#my_bot.put_exactly_like("https://www.instagram.com/p/CQoFNBqLJqk/")
my_bot.put_many_likes("https://www.instagram.com/the_witcher_serial_netflix/")

