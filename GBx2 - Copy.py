from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from random import random
import random
import time
import datetime
import os

#time parameter
b = datetime.time(7, 30, 00, 00000)
c = datetime.time(7, 40, 00, 00000)
d = datetime.time(13, 30, 00, 00000)

options = Options()
options.add_argument('--headless')
options.add_argument('--log-level=3')
print(chr(27) + "[2J")
os.system('cls' if os.name == 'nt' else 'clear')

#since the website checks for user agent to verify if you're using the same device, 
#this "simple" hack allows you to access the website using 2 different device as long as the user-agent is the same
while True:
    UA = input('1. Chrome 94, Windows 10\n2. Chrome 90, Android 9\nChoose User Agent: ')
    if (UA == '1'):
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")
        break
    if (UA == '2'):
        options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 9; SM-N950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36")
        break
    else:
        print('Invalid input')

PATH = "D:\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)
driver.minimize_window()
print(chr(27) + "[2J")
os.system('cls' if os.name == 'nt' else 'clear')
print('Absen Simple v1.5a by Yuzu')

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

loadUrl = ('') # emptied on purpose

# Initial web page load and loop if fail to load.
while (driver.current_url != loadUrl):
    driver.get('aWebsite')
    if (check_exists_by_xpath('/html/body/div[3]/div/div/div/form/div[2]/div[1]/div/input') == True): #This checks for the username input field to verify website load status
        break
    if (check_exists_by_xpath('/html/body/div[3]/div/div/div/form/div[2]/div[1]/div/input') == False):
        print('Failed to load page. Retry in 5s')
        time.sleep(5)

if UA == '1':
    print('Using Chrome on Windows 10 User-Agent')
if UA == '2':
    print('Using Chrome on Android 9 User-Agent')

#Function to search for username field and enter the user inputted text
def userInput():
    Username = input("Masukkan Username ")
    idsearch = driver.find_element_by_name("email")
    idsearch.send_keys(Username)

#Function to search for pw field and enter password
def pwInput():
    pswd = getpass.getpass('Masukkan Password ')
    pwsearch = driver.find_element_by_name("password")
    pwsearch.send_keys(pswd)
    pwsearch.send_keys(Keys.RETURN)

# Login function to combine both usename and password input
def login():    
    userInput()
    pwInput()
    print('\nLogging In\n')
    time.sleep(1)

# Login loop and status check
while(check_exists_by_xpath('//*[@id="epresensi-title"]') == False):
    login()
    if (check_exists_by_xpath('//*[@id="epresensi-title"]') == True):
        print('Login Sukses')
        break
    if (check_exists_by_xpath('//*[@id="epresensi-title"]') == False):
        print('Login Gagal. Coba lagi\n')
        time.sleep(5)

def loginCheck():
    while(check_exists_by_xpath('//*[@id="epresensi-title"]') == False):
        print('Logged out, Attempting to login')
        login()
        if (check_exists_by_xpath('//*[@id="epresensi-title"]') == True):
            print('\n Login Sukses')
            break

# driver.execute_script("window.scrollTo(0, 80)") 

H = ('/html/body/div[3]/div/div/div[2]/div/div/b/b/div/div[1]/div[1]/div[1]/a')
K = ('/html/body/div[3]/div/div/div[2]/div/div/b/b/div/div[1]/div[1]/div[2]/a')
K1 = ('/html/body/div[3]/div/div/div[2]/div/div/b/b/div/div[1]/div[1]/div[3]/a')
btnAbsenH = check_exists_by_xpath(H)
btnAbsenK = check_exists_by_xpath(K)
btnAbsenK1 = check_exists_by_xpath(K1)
#btnAbsenH_new = //*[@id="hadir-btn"]

#Function Absen Kehadiran
def executeAbsen():
    while(True):
        print('Current time is', datetime.datetime.now().time())
        if (((datetime.datetime.now().time() >= b) and (datetime.datetime.now().time() <= c)) == False):
            print('Invalid time, Retrying in 10s')
            time.sleep(10)
        if (((datetime.datetime.now().time() >= b) and (datetime.datetime.now().time() <= c)) == True):
            absenHari = driver.find_element_by_xpath(H)
            absenHari.click()
            time.sleep(2) # wait after clicking for the page to load
            print("\nAbsen Harian sukses")
            driver.refresh()
            time.sleep(3)
            break

#Function Absen KBM.
def executeAbsen_KBM(xpath):
    absenKBM = driver.find_element_by_xpath(xpath)
    absenKBM.click()
    print("\nAbsen KBM Sukses. Waktu sekarang:", datetime.datetime.now().time())
    driver.refresh()
    time.sleep(2)

#Cek Absen Harian dan KBM, jika belum maka jalankan executeAbsen masing2
if (btnAbsenH == True):
    executeAbsen()
    time.sleep(1)
if (btnAbsenK == True):
    executeAbsen_KBM(K)
if btnAbsenK1 == True:
    executeAbsen_KBM(K1)

#Jika tombol absen tidak ada, print ke terminal
if btnAbsenH == False:
    print("\nAbsen Kehadiran sudah direkam")
if (btnAbsenK == False):
    print("Absen KBM sudah direkam")

#Standby for Absen KBM, idk how i managed to make it work
def standbyKBM():
    while (True):
        if (datetime.datetime.now().time() >= d):
            print('It is past school time, Quitting...')
            time.sleep(3)
            driver.quit()
            exit()
        if (check_exists_by_xpath(K) == False):
            pass
        if (check_exists_by_xpath(K1) == False):
            print('Tombol Absen Mata Pelajaran belum ada. Cobalagi dalam 2-5m.', 'Waktu sekarang:',datetime.datetime.now().time())
            time.sleep(random.randint(120, 300))
            driver.refresh()
            print('Refreshing')
            time.sleep(3)
        if (check_exists_by_xpath(K) == True):
            executeAbsen_KBM(K)
            time.sleep(1800)
        if (check_exists_by_xpath(K1) == True):
            executeAbsen_KBM(K1)

standbyKBM()
standbyKBM()
standbyKBM()
standbyKBM()
standbyKBM()
standbyKBM()

##while True:
##     pilihan = input('\n1.Exit program\n2.Standby Absen Mata Pelajaran\nPilihan: ')
##     if (pilihan == '1'):
##         driver.quit()
##         exit()
##     if (pilihan == '2'):
##         standbyKBM()
##         time.sleep(2)
##         standbyKBM()
##     else:
##         print("Invalid input")

# Geo Spoofing Parameter, coordinates emptied on purpose
# latRandomA = round(random.uniform(),6)
# longRandomA = round(random.uniform(),6)
# latRandomB = round(random.uniform(),6) 
# longRandomB = round(random.uniform(),6)
# accuracy = random.randint(50,125)
#Push GPS Coordinate values to webdriver
# GPSinput = input('\n1. A \n2. B\n Choose Where to be: ')
# while True:
#     if GPSinput == '1':
#         driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
#         "latitude": latRandomA,
#         "longitude": longRandomA,
#         "accuracy": accuracy 
#         })
#         os.system('cls' if os.name == 'nt' else 'clear')
#         print("GPS spoofed to",latRandomA,longRandomA,"with Accuracy of ~",accuracy," meters") #print the coordinates used
#         break
#     if GPSinput == '2':
#         driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
#         "latitude": latRandomB,
#         "longitude": longRandomB,
#         "accuracy": accuracy 
#         })
#         os.system('cls' if os.name == 'nt' else 'clear')
#         print("GPS spoofed to",latRandomB,longRandomB,"with Accuracy of ~",accuracy," meters") #print the coordinates used
#         break
#     else:
#         print('Invalid input')

# def loopAbsenK():
##    while True:
##     pilihan = input('\n1.Sleep 30 min \n2. Lanjut standby\nPilihan: ')
##     if (pilihan == '1'):
##         print('OK')
##         print("Waktu sekarang:", datetime.datetime.now().time())
##         time.sleep(1800)
##         loginCheck()
##         print(driver.current_url)
##         break
##     if (pilihan == '2'):
##         print('OK')
##         break
##     else:
##         print("Invalid input")




#Changelog
# 1.4a => first working release
# 1.4b => the b suffix from now will be the difference between my personal version and the version that has username/password input
# 1.5a => added checks for both KBM button, option to choose which UserAgent to use, remove gps spoofing (temp), added time check to standbykbm
