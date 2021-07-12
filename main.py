from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException
# Для скачиваний
import requests
# Для папок
import os


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

    # Метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):
        browser = self.browser

        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

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

    # Метод собирает ссылки на все посты пользователя
    def get_all_posts_urls(self, userpage):
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

    # Метод ставит лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, userpage):
        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

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

    # Метод для скачивания контента со страницы пользователя
    # Данный метод не качает фотографии из публикаций, где больше одной фотографий
    def download_userpage_image(self, userpage):
        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # создаём папку с именем пользователя
        if os.path.exists(f"{file_name}"):
            print("Папка уже есть")
        else:
            os.mkdir(file_name)

        img_and_video_src_urls = []
        with open(f'{file_name}.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list[0:1]:
                try:
                    browser.get(post_url)
                    time.sleep(5)
                    img_src = "//div/article/div[2]/div/div/div[1]/img"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    else:
                        # print("Что-то не так!")
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки")
                    print(f"Контент из поста {post_url} успешно скачан!")

                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()
        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")


# Старт бота
my_bot = InstagramBot(username, password)
# Обязательно авторизация
my_bot.login()

# Дополнительные функции:
# my_bot.like_photo_by_hashtag('voleyball')
# my_bot.put_exactly_like("https://www.instagram.com/p/CQoFNBqLJqk/")
my_bot.download_userpage_image("https://www.instagram.com/alexei_shcherbakov_tm/")
