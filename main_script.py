import undetected_chromedriver as uc
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy
import time
from datetime import datetime
import winsound
import re
import traceback
import os
import skippable_timer
import codecs
from playsound import playsound
from dotenv import load_dotenv
import chromedriver_autoinstaller


def login():
    username = os.getenv("LICENCE")
    password = os.getenv("REFERENCE")
    user_field = WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.ID, 'driving-licence-number')))
    RandomWait(0.5, 1)
    user_field.send_keys(username)
    printAndLog("Username entered")

    RandomWait(0.5, 1)
    password_field = driver.find_element(By.ID, 'application-reference-number')
    password_field.send_keys(password)
    printAndLog("Password entered")

    RandomWait(0.5, 1)
    driver.find_element(By.ID, 'booking-login').click()
    printAndLog("Credentials submitted\n")


def RandomWait(minimum=float(1), maximum=float(10)):
    time.sleep(numpy.random.uniform(minimum, maximum))


def get_search_results():
    result_list = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'test-centre-results')))

    inner_results = []
    soup = bs(driver.page_source, 'html.parser')

    centres = soup.find_all('li', class_='clear')

    for centre in centres:
        header = centre.span
        location = header.h4.text

        if not any([x in location for x in wanted_sites]):  # skip if doesn't match wanted places
            continue

        availability = header.h5.text
        match = re.search('(\d+/\d+/\d+)', availability)

        if match is None:
            availability = None
            availability_number = None
        else:
            availability = match[0]
            availability_number = int(datetime.strptime(availability, '%d/%m/%Y').timestamp())

        link = base_url + centre.find(class_='test-centre-details-link')['href']

        inner_results.append({
            'location': location,
            'availability': availability,
            'availability_number': availability_number,
            'link': link
        })

    return inner_results


def moveOffscreen():
    driver.set_window_position(2000, 0)


def moveOnscreen():
    driver.set_window_position(10, 10)


def LoadSite():
    try:
        printAndLog("Loading site")
        driver.get(login_url)

        for i in range(1, page_limit):
            UpdatePageID()
            if page_id != -1:
                break

    except:
        printAndLog("Error during loading site")


def NavToSearchPage():
    # navigate to test centre change
    element = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'test-centre-change')))
    RandomWait(0.5, 1)
    element.click()
    printAndLog("Navigated to search page")


def Beep():
    for i in range(1, 10):
        winsound.Beep(i * 200, 300)
    for i in range(1, 10):
        winsound.Beep((i + 2) * 200, 300)


def Dead():
    winsound.Beep(2500, 1500)


def SubmitNewDate():
    # submit changes
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'confirm-changes')))
    scroll_to_element(element)
    RandomWait(0.5, 1)
    element.click()

    driver.exit()
    exit()


def printAndLog(txt, header=''):
    if len(header) != 0:
        print(header + ': ')

    print(txt)
    LogIt(txt, header)


def LogIt(txt, header=''):
    if len(header) != 0:
        LOG.write(header + ': ')

    if type(txt) is str:
        LOG.write(txt + '\n')
    elif type(txt) == type(None):
        LOG.write('None' + '\n')
    elif type(txt) is list:
        txt = ['None' if x is None else x for x in txt]
        LOG.write(', '.join(txt) + '\n')

    LOG.flush()


def InitialiseDirectory():
    paths = [log_folder_master, log_folder_instance]
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)


def MakeLine():
    printAndLog('\n##############################\n')


def UpdatePageID(sleep_for=float(2), print_id=True):
    # 0 = login page
    # 100 = summary page
    # 201 = search page - before search
    # 200 = search page - after search
    # 202 = search limit reached
    # 300 = calendar page
    # 400 = alternative centres page (means no dates available when clicked)
    # 500 = candidate confirmation page
    # 501 = change booking confirmation
    # 502 = search limit reached
    # 503 = you went away and came back page
    # 1 = queue
    # -1 = unrecognised page
    # 666 = recapcha page
    # 667 = no page
    # 600 = problem with the service

    global page_id, page_counter

    time.sleep(sleep_for)

    body_tag = driver.find_element(By.TAG_NAME,'body')
    page_html = driver.page_source

    try:
        body_id = driver.find_element(By.TAG_NAME,'body').get_attribute('id')

        if body_id == '':
            body_id = driver.find_element(By.TAG_NAME,'body').get_attribute('data-pageid')

        if body_id == "page-login":
            new_id = 0
        elif body_id == "queue":
            new_id = 1
        elif body_id == 'page-ibs-summary':
            new_id = 100
        elif body_id == "page-test-centre-search":
            if len(driver.find_elements(By.ID, "search-results")) > 0:
                new_id = 200
            else:
                new_id = 201
        elif body_id == "page-available-time":
            if not driver.find_element(By.ID, 'slot-warning-continue').is_displayed():
                new_id = 300  # calendar page
            elif "time chosen is no longer available" in driver.page_source:
                new_id = 302
            else:
                new_id = 301  # confirm 15 minute warning
        elif body_id == "page-alternative-centres":
            new_id = 400
        elif body_id == "page-confirm-booking":
            if len(driver.find_elements(By.ID, 'candidate-or-not')) > 0:
                new_id = 500  # confirm candidate page
            elif "Search limit reached" in page_html:
                new_id = 502
            elif "Oops! You went away and came back again" in page_html:
                new_id = 503
            else:
                new_id = 501  # change booking page
        elif body_id == "page-vehicle-information":
            new_id = 600
        else:
            if "Incapsula" in body_tag.text:
                if "This request was blocked by the security rules" in body_tag.text:
                    new_id = 665
                else:
                    new_id = 666
            elif body_id == 't':
                new_id = 667
            else:
                new_id = -1
                page_counter = page_counter + 1

        if page_counter >= page_limit:
            new_id = 667
            page_counter = 0

        if print_id:
            print('Body ID: ', body_id)
            print('Page ID: ', new_id)


        if new_id != page_id:
            page_id = new_id
            UpdatePageID()
        else:
            page_id = new_id
    except:
        traceback.print_exc()
        UpdatePageID()


def PrintDates(loc, dat):
    # print dates
    printAndLog([x[0] for x in dat],
                header=loc)
    # print dates in search range
    printAndLog([x[0] for x in dat if start_date_num <= int(x[2][0].timestamp()) <= end_date_num],
                header="In range")


def CheckValidTime():
    current_time = datetime.now()
    current_secs = (current_time.hour * 60 * 60) + (current_time.minute * 60)

    if current_secs > termination_secs:
        MakeLine()
        printAndLog("The site has closed. Shutting down.")

        try:
            driver.quit()
        finally:
            exit()


def HoldDate(day_element, time_element):
    try:
        MakeLine()
        month = datetime.strptime(day_element.get_attribute('data-date'), '%Y-%m-%d').month
        month_calendar = months.index(driver.find_element(By.CLASS_NAME, 'BookingCalendar-currentMonth').text) + 1

        if month != month_calendar:
            buttons = driver.find_element(By.CLASS_NAME, 'BookingCalendar-header').find_elements(By.TAG_NAME, 'a')

            while month != month_calendar:
                if month_calendar > month:
                    buttons[0].click()
                elif month_calendar < month:
                    buttons[1].click()

                month_calendar = months.index(driver.find_element(By.CLASS_NAME, 'BookingCalendar-currentMonth').text) + 1
                RandomWait(0.5, 1)

        printAndLog("Holding earliest slot")
        # clicking date on calendar
        RandomWait(0.5, 1)
        scroll_to_element(day_element)
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(day_element))

        day_element.click()
        printAndLog("Day clicked")

        # clicking time
        RandomWait(0.5, 1)
        time_clickable = time_element.find_element(By.XPATH, '..')
        scroll_to_element(time_clickable)
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(time_clickable))
        time_clickable.click()
        printAndLog("Time clicked")

        # submitting
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        RandomWait(0.5, 1)

        submit_btn = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, 'slot-chosen-submit')))
        scroll_to_element(submit_btn)
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(submit_btn))
        submit_btn.click()
        printAndLog("Date submitted for confirmation")
    except:
        driver.refresh()
        printAndLog("Holding date failed")
        traceback.print_exc()


def DismissCalendarWarning():
    # continue
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'slot-warning-continue')))
    scroll_to_element(element)
    RandomWait(0.5, 1)
    element.click()
    print("15 minute warning dismissed")


def ConfirmCandidate():
    # verify the candidate
    element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'i-am-candidate')))
    scroll_to_element(element)
    RandomWait(0.5, 1)
    element.click()
    print("Continued to confirmation page")


def HoldForAWhile():
    # moveOnscreen()
    play_found_booking_sound()

    print("After 15 minutes program will resume.\nPress enter to abort.")
    timer_broken = skippable_timer.timer(15 * 60)
    if timer_broken:
        answer = ""
        print("Would you like to continue or terminate the program?")
        while answer.lower() not in ['continue', 'terminate']:
            answer = input("(continue/terminate): ")

        if answer.lower() == 'terminate':
            try:
                driver.quit()
            finally:
                exit()

    while page_id not in [100, 200, 201]:
        printAndLog("Going back hold")
        driver.back()
        WebDriverWait(driver, 60).until(EC.url_changes)
        UpdatePageID(1)


def InitialSearch():
    # searching test centers
    RandomWait(0.5, 1)
    element = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'test-centres-input')))
    element.clear()
    element.send_keys(post_code)
    printAndLog("Search entered")

    RandomWait(0.5, 1)
    driver.find_element(By.ID, 'test-centres-submit').click()
    SearchLoop(first=True)


def SearchLoop(first=False):
    def Wait():
        wait_time = numpy.random.uniform(0.8, 1.2)
        printAndLog("\nWaiting: " + "{:.2f}".format(wait_time))
        time.sleep(60 * wait_time)

    try:

        driver.execute_script("window.scrollTo(0,0)")
        time.sleep(1)

        if not first:
            driver.find_element(By.ID, 'test-centres-submit').click()

        search_results = get_search_results()

        printAndLog("")
        printAndLog(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

        for res in search_results:
            printAndLog(res['availability'], res['location'] + "(Rough Dates)")

        available_sites = [x for x in search_results if x['availability'] is not None]

        if len(available_sites) != 0:
            RandomWait(0.5, 1)
            for site in available_sites:
                driver.get(site['link'])
                date_submitted = CalendarLoop()

                if date_submitted:
                    return
            Wait()
        else:
            Wait()
    except:
        play_error_sound()


def scrape_calendar():
    available_dates = []
    soup = bs(driver.page_source, 'html.parser')

    for day in soup.find_all(class_='BookingCalendar-date--bookable'):
        times = []
        datetime_obj = []

        day_element = day.find(class_='BookingCalendar-dateLink')
        day_str = day_element['data-date']

        time_slot_container = soup.find(id='date-' + day_str)

        time_elements = time_slot_container.find_all('input')

        time_click_box_ids = [x['id'] for x in time_elements]

        for time_str in time_elements:
            time_str = time_str['data-datetime-label']
            times.append(time_str)
            datetime_obj.append(datetime.strptime(time_str, '%A %d %B %Y %I:%M%p'))

        available_dates.append({
            'date_str': day_str,
            'times': times,
            'datetimes': datetime_obj,
            'day_element_ref': day_element['href'],
            'time_box_ids': time_click_box_ids
        })

    return available_dates

def scroll_to_element(element):
    action = ActionChains(driver)
    action.move_to_element(element).perform()

def CalendarLoop():
    centre_banner = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'chosen-test-centre')))

    location = centre_banner.text.split('\n')[0].lower()
    for key in wanted.keys():
        if key.lower() in location:
            location = key
            break

    available_days = scrape_calendar()

    printAndLog('', header=location + " (Full Dates)")

    for day in available_days:
        time_strings = [re.search('\d+:\d+\w{2}', x)[0] for x in day['times']]
        printAndLog(time_strings, header=day['date_str'])

    if HOLD:
        for day in available_days:
            if wanted[location].start_num <= int(day['datetimes'][0].timestamp()) <= wanted[location].end_num:
                for i in range(0, len(day['datetimes'])):
                    if day['datetimes'][i].hour >= 9:
                        day_element = driver.find_element(By.XPATH, '//a[@href="' + day['day_element_ref'] + '"]')
                        time_element = driver.find_element(By.ID, day['time_box_ids'][i])

                        HoldDate(day_element, time_element)
                        return True

        printAndLog("No suitable dates")

    printAndLog("")
    printAndLog("Going back to calendar")
    RandomWait(0.5, 1)
    driver.back()
    return False


def back_to_search():
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, 'change-test-centre'))).click()


def play_error_sound():
    try:
        Dead()
        printAndLog("Played error sound")
    except:
        Dead()
        printAndLog("Failed to play error sound")


def play_found_booking_sound():
    try:
        Beep()
        printAndLog("Played booking found sound")
    except:
        Dead()
        printAndLog("Failed to play booking found sound")


def save_error_html():
    try:
        error_time = datetime.now().strftime('%Y-%m-%d %H;%M;%S')
        with codecs.open(log_folder_instance + '\\Errors\\' + error_time) as file:
            file.write(driver.page_source)
        print("Saved Error HTML at: ", error_time)
    except:
        printAndLog("Couldn't save error HTML")


class wantedLocation:
    def __init__(self, start_str=None, end_str=None, exclusion_dates=None):
        def get_exclusion_dates_num(exclusion_in):
            if type(exclusion_in) is str:
                return int(datetime.strptime(exclusion_in, '%d/%m/%Y').timestamp())
            elif type(exclusion_in) is list:
                return [int(datetime.strptime(x, '%d/%m/%Y').timestamp()) for x in exclusion_in]
            else:
                return None

        if start_str is None:
            start_str = start_date_str
        if end_str is None:
            end_str = end_date_str
        if exclusion_dates is not None and type(exclusion_dates) is not list:
            exclusion_dates = [exclusion_dates]

        self.start_str = start_str
        self.end_str = end_str

        self.start_num = int(datetime.strptime(self.start_str, '%d/%m/%Y').timestamp())
        self.end_num = int(datetime.strptime(self.end_str, '%d/%m/%Y').timestamp())

        self.exclusion_dates_str = exclusion_dates

        if self.exclusion_dates_str is not None:
            self.exclusion_dates_num = get_exclusion_dates_num(self.exclusion_dates_str)
        else:
            self.exclusion_dates_num = None


def captcha_loop():
    captcha_counter = 0
    while page_id == 666:
        RandomWait(0.5, 1)
        UpdatePageID(1, print_id=False)
        #click_captcha()
        captcha_counter = captcha_counter + 1
        if captcha_counter % 10 == 0:
            print('%i seconds passed' % captcha_counter)

def click_captcha():
    for i in range(2):
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))

    checkbox = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'rc-anchor-center-container')))
    checkbox.click()
    try:
        driver.switch_to.parent_frame()
        frames = driver.find_elements(By.TAG_NAME, 'iframe')
        if len(frames) == 1:
            driver.switch_to.frame(frames[0])
            frames = driver.find_elements(By.TAG_NAME, 'iframe')

        driver.switch_to.frame(frames[2])
        controls = driver.find_element(By.CLASS_NAME, 'rc-buttons')
        loc = controls.location
        items = controls.find_elements(By.TAG_NAME, 'div')
        loc2 =items[2].location

        RandomWait(0.5,1)
        action = ActionChains(driver)
        action.move_to_element_with_offset(controls, loc2['x'] - loc['x'], 0)
        action.click()
        action.perform()
    except:
        print("Captcha solution not clicked")


def print_wanted_sites():
    for site in wanted_sites:
        printAndLog("WANTED LOCATIONS")
        printAndLog(site + ':')
        printAndLog(wanted[site].start_str + " - " + wanted[site].end_str, header='Date Range')
        printAndLog(wanted[site].exclusion_dates_str, header="Exclusion Dates")

def get_driver():
    pth = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
    chrome_path =  chromedriver_autoinstaller.install()
    print("Chrome path: {}".format(chrome_path))
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--enable-javascript')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    prefs = {"profile.managed_default_content_settings.images": 2} # Hide images (experimental)
    chrome_options.add_experimental_option("prefs", prefs)

    driver_out = uc.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
    driver_out.execute_cdp_cmd('Network.enable', {})

    return driver_out


if __name__ == '__main__':
    load_dotenv()
    page_limit = 20
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    post_code = "OX12"

    start_date_str = '10/06/2022'
    end_date_str = '08/07/2022'
    start_date_num = int(datetime.strptime(start_date_str, '%d/%m/%Y').timestamp())
    end_date_num = int(datetime.strptime(end_date_str, '%d/%m/%Y').timestamp())

    end_time = datetime.strptime('23:40', '%H:%M')
    termination_secs = (end_time.hour * 60 * 60) + (end_time.minute * 60)

    wanted = {
        'Newbury': wantedLocation(
            start_date_str,
            end_date_str,
            None
        )
    }

    wanted_sites = list(wanted.keys())

    base_url = 'https://driverpracticaltest.dvsa.gov.uk'
    login_url = base_url + "/login"
    now_time = datetime.now().strftime('%Y-%m-%d %H;%M;%S')

    log_folder_master = "logs"
    log_folder_instance = "logs\\" + now_time

    log_path = log_folder_instance + '\\' + now_time + '.txt'

    HOLD = True
    proxies = []

    InitialiseDirectory()

    with open(log_path, 'w') as LOG:
        MakeLine()

        printAndLog(now_time, "Start Time")

        print_wanted_sites()

        MakeLine()

        while True:

            try:
                with get_driver() as driver:

                    page_id = None
                    page_counter = 0

                    while True:
                        CheckValidTime()
                        for test_loop in range(5):
                            print('Test_{}'.format(test_loop+1))
                            UpdatePageID(0)

                        if page_id == -1:
                            LoadSite()
                            # input("Waiting for you")
                        elif page_id == 1:
                            pass
                        elif page_id == 0:
                            login()
                        elif page_id == 100:
                            NavToSearchPage()
                        elif page_id == 200:
                            SearchLoop()
                        elif page_id == 201:
                            InitialSearch()
                        elif page_id == 300:
                            CalendarLoop()
                        elif page_id == 301:
                            DismissCalendarWarning()
                        elif page_id == 302:
                            driver.refresh()
                        elif page_id == 400:
                            back_to_search()
                            printAndLog("Date no longer available. Going back to search page")
                        elif page_id == 500:
                            ConfirmCandidate()
                        elif page_id == 501:
                            HoldForAWhile()
                        elif page_id == 502:
                            printAndLog("Search limit reached. Starting over")
                            driver.quit()
                        elif page_id == 503:
                            printAndLog("Oops! You went away and came back, restarting")
                            driver.quit()
                        elif page_id == 600:
                            printAndLog("There was a problem with the service")
                            driver.quit()
                        elif page_id == 665:
                            printAndLog("Blocked by security rules, restarting")
                            driver.quit()
                        elif page_id == 666:
                            play_error_sound()
                            captcha_loop()
                        elif page_id == 667:
                            printAndLog("Server error")
                            raise Exception("Server Error")

            except Exception as e:
                MakeLine()
                MakeLine()
                MakeLine()

                play_error_sound()
                save_error_html()

                try:
                    driver.quit()
                finally:
                    LogIt(traceback.format_exc())
