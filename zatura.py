from selenium import webdriver
import time
import math
from sigfig import round as rou
import numpy as np
from selenium.common.exceptions import NoSuchElementException
import webdriver_manager.chrome
def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    driver = webdriver.Chrome(webdriver_manager.chrome.ChromeDriverManager().install(), options=chrome_options)
    driver.delete_all_cookies()
    driver.set_window_size(800, 800)
    driver.set_window_position(0, 0)

    with open('dataa2.txt', 'r') as f:
        rivit = f.readlines()
        user = rivit[0].strip()
        passw = rivit[1].strip()
        osoite = rivit[2].rstrip('\n')
        hyppy = rivit[3].rstrip('\n').split(',')
        yritteet = [i for i in rivit[6:]]
        tarkkuus = int(rivit[4])
        unit = rivit[5]
    driver.get(osoite)
    kirjaudu_ja(driver, user, passw)
    arvaa(driver, yritteet, hyppy, unit, tarkkuus)


def arvaa(driver, yritteet, hyppy, unit, tarkkuus):
    paina = yritteet[0].split('_')[0]
    unit = f'*{unit}'
    A = np.arange(float(hyppy[0]), float(hyppy[1]), float(hyppy[2]))
    num = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for i in range(len(A)):
        for y in yritteet:
            driver.find_element_by_xpath(f'//input[contains(@id ,"{y}")]').clear()
        time.sleep(3)
        luku = roundaa(float(A[i]), tarkkuus)
        for j in yritteet:
            lah = f'{luku}{unit}'
            driver.find_element_by_xpath(f'//input[contains(@id ,"{j}")]').send_keys(lah)
            time.sleep(3)
        element = driver.find_element_by_css_selector(f'input[name*="{paina}_-submit"]')
        driver.execute_script("arguments[0].click();", element)
        for k in yritteet:
            a = int(k.split('s')[1]) - 1
            try:
                onko = driver.find_element_by_xpath(f'//div[contains(@class, "{num[a]}kohdanpuu")]//div[contains(@style, "color: rgb(0, 128, 0)")]')
                print(onko.text)
                if onko.text == f'{num[a]}-kohta on oikein!':
                    juu = num[int(yritteet[k].split('s')[1])-1]
                    del yritteet[num.index(juu)]
            except NoSuchElementException:
                pass
        if len(yritteet) == 0:
            break


#driver.find_element_by_xpath('//*[contains(@id,"username")]').send_keys(user)

def kirjaudu_ja(driver, user, passw):
    #driver.find_element_by_xpath('//button[text()="Jatka"]').click()
    driver.find_element_by_xpath('//a[text()="Login as Aalto user"]').click()
    time.sleep(2)
    driver.find_element_by_css_selector('input[id="username"]').send_keys(user)
    time.sleep(2)
    driver.find_element_by_css_selector('input[id="password"]').send_keys(passw)
    time.sleep(2)
    driver.find_element_by_xpath('//button[text()="Login"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//button[text()="Continue the last attempt"]').click()
    time.sleep(2)


def roundaa(x, sigfigs) -> str:
    '''
    Suppose we want to show 2 significant figures. Implicitly we want to show 3 bits of information:
    - The order of magnitude
    - Significant digit #1
    - Significant digit #2
    '''

    if sigfigs < 1:
        raise Exception('Cannot have fewer than 1 significant figures. ({} given)'.format(sigfigs))

    order_of_magnitude = math.floor(math.log10(abs(x))) -1
    # Because we get one sigfig for free, to the left of the decimal
    decimals = (sigfigs) - 1


    x /= pow(10, order_of_magnitude)
    x = rou(x, decimals + 1)
    x *= pow(10, order_of_magnitude)

    # Subtract from decimals the sigfigs we get from the order of magnitude
    decimals -= order_of_magnitude
    # But we can't have a negative number of decimals
    decimals = max(0, decimals)
    if decimals > 0:
        decimals -= 1
    return '{:.{dec}f}'.format(x, dec=decimals)

main()