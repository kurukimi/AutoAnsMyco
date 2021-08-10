from selenium import webdriver
import time
import math
from sigfig import round as rou
import webdriver_manager.chrome
def main():
    '''Automatisoi vastaamisen MyCoursesin tehtäviin, jossa loputtomat vastauskerrat.
     '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    driver = webdriver.Chrome(webdriver_manager.chrome.ChromeDriverManager().install(), options=chrome_options)
    driver.delete_all_cookies()
    driver.set_window_size(800, 800)
    driver.set_window_position(0, 0)
    '''Luetaan tiedot tiedostosta:
    ensimmäisellä rivillä käyttäjätunnus
    toisella salasana
    kolmannella osoite tehtävän aloituskohtaan
    neljännelle alkuraja,loppuraja,hyppy
    viidennelle haluttu vastauksen tarkkuus annetun tehtävän mukaan
    lopuille vastauskentän nimet, ja niissä käytetty yksikkö esim *m/s'''
    with open('dataa2.txt', 'r') as f:
        rivit = f.readlines()
        user = rivit[0].strip()
        passw = rivit[1].strip()
        osoite = rivit[2].rstrip('\n')
        hyppy = rivit[3].rstrip('\n').split(',')
        yritteetk = [i for i in rivit[5:]]
        tarkkuus = int(rivit[4])
    driver.get(osoite)
    kirjaudu_ja(driver, user, passw)
    arvaa(driver, yritteetk, hyppy, tarkkuus)


def arvaa(driver, yritteetk, hyppy, tarkkuus):
    '''Funktio looppaa arvoja vastauskenttiin ja lähettää vastaukset'''
    yritteet = [i.split(',')[0] for i in yritteetk]
    yks1 = [i.split(',')[1] for i in yritteetk]
    paina = yritteet[0].split('_')[0]
    alku = float(hyppy[0])
    loppu = float(hyppy[1])
    step = float(hyppy[2])

    while alku < loppu:
        time.sleep(1)
        luku = roundaa(float(alku), tarkkuus)
        l = 0
        for j in yritteet:
            driver.find_element_by_xpath(f'//input[contains(@id ,"{j}")]').clear()
            lah = f'{luku}{yks1[l]}'
            l += 1
            driver.find_element_by_xpath(f'//input[contains(@id ,"{j}")]').send_keys(lah)
        time.sleep(1.5)
        element = driver.find_element_by_css_selector(f'input[name*="{paina}_-submit"]')
        driver.execute_script("arguments[0].click();", element)
        if len(yritteet) == 0:
            driver.close()
            break
        alku = alku + step


def kirjaudu_ja(driver, user, passw):
    '''Kirjautuu mycoon'''
    driver.find_element_by_xpath('//a[text()="Login as Aalto user"]').click()
    driver.find_element_by_css_selector('input[id="username"]').send_keys(user)
    driver.find_element_by_css_selector('input[id="password"]').send_keys(passw)
    driver.find_element_by_xpath('//button[text()="Login"]').click()
    driver.find_element_by_xpath('//button[text()="Continue the last attempt"]').click()


def roundaa(x, sigfigs) -> str:
    '''
    palauttaa luvun halutulla määrällä merkitseviä numeroita
    '''

    if sigfigs < 1:
        raise Exception('Cannot have fewer than 1 significant figures. ({} given)'.format(sigfigs))

    order_of_magnitude = math.floor(math.log10(abs(x))) -1
    decimals = (sigfigs) - 1

    x /= pow(10, order_of_magnitude)
    x = rou(x, decimals + 1)
    x *= pow(10, order_of_magnitude)

    decimals -= order_of_magnitude
    decimals = max(0, decimals)
    if decimals > 0:
        decimals -= 1
    return '{:.{dec}f}'.format(x, dec=decimals)


main()