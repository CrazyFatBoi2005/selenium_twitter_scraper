import re
import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge import options
from selenium.webdriver.edge import webdriver as webdEdge
from selenium.common.exceptions import NoSuchElementException

# хештеги
hashtags = ['#covid', '#covid19', '#covid-19', '#коронавирус', '#ковид', '#пандемия']


# данные твита
def get_tweet_data(card):
    username = card.find_element_by_xpath('.//span').text
    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except NoSuchElementException:
        return

    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return

    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    try:
        t = comment + responding
        t = t.split('\n')
        name = t[0].strip(' ')
        username = t[1]
        date = t[3][:t[3].find('2020 г.')] + '2020 г.'
        text = t[3][len(date):]
        hashtag = []
        for h in hashtags:
            if h in text.lower():
                hashtag.append(h)
        hashtag = ' '.join(hashtag)
        tweet = (name, username, date, text, hashtag)
        print(*tweet, sep='\n')
        return tweet
    except IndexError:
        return


# даты для поиска
search_base1 = [
    ['01-31', '01-30'],
    ['03-05', '03-04'],
    ['03-21', '03-20'],
    ['03-25', '03-24'],
    ['03-27', '03-26'],
]

search_base2 = [
    ['04-21', '04-20'],
    ['05-28', '05-27'],
    ['08-01', '07-31'],
    ['08-11', '08-10'],
]
user = ''# username ввести
my_password = ''# ваш пароль

# Здесь я использовал Edge браузер, поэтому надо подгрузить драйвера для него
options = options.Options()
options.use_chromium = True
driver = webdEdge.WebDriver(executable_path='C:\Program Files\msedge\msedgedriver')# здесь вам нужно установить exe файл для вашего браузера и путь к этому драйверу

# Логин
driver.get('https://www.twitter.com/login')
driver.maximize_window()
sleep(5)
username = driver.find_element_by_xpath('//input[@name="text"]')
username.send_keys(user)
username.send_keys(Keys.RETURN)
sleep(3)

password = driver.find_element_by_xpath('//input[@name="password"]')
password.send_keys(my_password)
password.send_keys(Keys.RETURN)
sleep(3)

# данные
tweet_ids = set()
data = []
# Перебор по ключам(датам
for key in search_base2:
    search_term = f"(#Covid OR #Covid19 OR #Covid-19 OR #Пандемия OR #Коронавирус OR #Ковид) lang:ru until:2020-{key[0]} since:2020-{key[1]}"
    # find search input and search for term
    search_input = driver.find_element_by_xpath(f'//input[@aria-label="Поисковый запрос"]')
    search_input.send_keys(search_term)
    search_input.send_keys(Keys.RETURN)
    sleep(1)

    # У меня браузер был на русском поэтому поиск по кнопке Последнее
    driver.find_element_by_link_text('Последнее').click()

    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    while scrolling:
        # все твиты
        page_cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
        for card in page_cards[-15:]:
            # данные тивта
            tweet = get_tweet_data(card)
            # если данные найдены, то парсим
            if tweet:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    # Вывод всей инфоррмации для проверки и отслеживания работы
                    print(tweet)
                    a = tweet[2].split(' ')[0]
                    if len(a) == 1:
                        a = '0' + a
                    if a == key[0][3:]:
                        tweet_ids.add(tweet_id)
                        data.append(tweet)
                    else:
                        print(tweet[2].split(' ')[0], key[0][3:])
                        scrolling = False
                        break

        scroll_attempt = 0
        while True:
            # Скролим страницу
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(3)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # если страница кончилась
                if scroll_attempt >= 3:
                    scrolling = False
                    print(data)
                    break
                else:
                    sleep(2)  # задержка между скролами
            else:
                last_position = curr_position
                break

    # После поиска по одному щапросу возвращаемся на Главную страницу и повторяем =)
    home_button = driver.find_element_by_xpath(f'//a[@href="/home"]')
    home_button.click()
    sleep(5)

# Закрываем
driver.close()

# записываем в csv
with open('result2.csv', 'w', newline='', encoding='utf-8') as f:
    header = ['Имя пользователя', 'Ссылка', 'Время', 'Текст', 'Хэштеги']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
