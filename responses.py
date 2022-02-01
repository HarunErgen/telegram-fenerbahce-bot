import constants as keys
from datetime import datetime, timedelta
import telegram, re
from selenium import webdriver
from selenium.webdriver.common.by import By
import locale

locale.setlocale(locale.LC_ALL, 'tr_TR')

# Instantiating the bot
bot = telegram.Bot(token=keys.API_KEY)

# Regular expressions
match_time_regex = r'(ma(c|ç) (saat )?ka(c|ç)ta|ma(c|ç) ne (za?ma?n))'
time_left_regex = r'(ma(c|ç)a ne kadar (za?ma?n )?(var|kald(ı|i)))'
time_left_to_specific_match_regex = r'[a-zA-Z0-9ığüşçö]+\sma(c|ç)(ı|i)na ne kadar (var|kald(ı|i)|za?ma?n var)'
fenerbahce_fixture_regex = r'(fiks(t(u|ü)r)?)\s\d'
get_fixture_regex = r'[a-zA-Z0-9ığüşçö\s]+\sfikst(ü|u)r'
get_ticket_regex = r'\sma(c|ç)(ı|i)?(na)?\s*bilet((ler)?i)?'

# Calculation of which week it is in Süper Lig
league_start_date = datetime(2021,8,16)
week_count = int(((datetime.now() - timedelta(days=datetime.now().weekday())) - (league_start_date - timedelta(days=league_start_date.weekday()))).days / 7)

fenerbahce_fixture = {
"Fenerbahçe - Başakşehir": datetime(2022,2,5, 19,00), "Fenerbahçe - Kayserispor": datetime(2022,2,8, 20,30),
"Giresunspor - Fenerbahçe": datetime(2022,2,12, 16,00), "Fenerbahçe - Slavia Prag": datetime(2022,2,17, 20,45),
"Fenerbahçe - Hatayspor": datetime(2022,2,20, 19,00), "Slavia Prag - Fenerbahçe": datetime(2022,2,24, 23,00),
"Kasımpaşa - Fenerbahçe": datetime(2022,2,27), "Fenerbahçe - Trabzonspor": datetime(2022,3,6),
"Alanyaspor - Fenerbahçe": datetime(2022,3,13), "Fenerbahçe - Konyaspor": datetime(2022,3,20),
"Kayserispor - Fenerbahçe": datetime(2022,4,3), "Fenerbahçe - Galatasaray": datetime(2022,4,10),
"Fenerbahçe - Göztepe": datetime(2022,4,17), "Rizespor - Fenerbahçe": datetime(2022,4,24),
"Fenerbahçe - Gaziantep FK": datetime(2022,5,1), "Beşiktaş - Fenerbahçe": datetime(2022,5,8),
"Fenerbahçe - Karagümrük": datetime(2022,5,15), "Yeni Malatya - Fenerbahçe": datetime(2022,5,22) 
}
match_list = list(fenerbahce_fixture)

def responses(input_text):
    user_message = str(input_text).lower()
    
    if re.search(match_time_regex, user_message):
        while fenerbahce_fixture[match_list[0]] < datetime.now():
            fenerbahce_fixture.pop(match_list[0])
            match_list.pop(0)
        return match_list[0] + "  |  " + fenerbahce_fixture[match_list[0]].strftime("%d.%m.%Y - %H:%M")
    if re.search(time_left_regex, user_message):
        while fenerbahce_fixture[match_list[0]] < datetime.now():
            fenerbahce_fixture.pop(match_list[0])
            match_list.pop(0)
        remaining = fenerbahce_fixture[match_list[0]] - datetime.now()
        return get_reamining_time(remaining)
    if re.search(time_left_to_specific_match_regex, user_message):
        team = user_message.split()[0].capitalize()
        specific_match = None
        for match in match_list:
            if team in match:
                specific_match = match
                break
        remaining = fenerbahce_fixture[specific_match] - datetime.now()
        return get_reamining_time(remaining)
    if re.search(fenerbahce_fixture_regex, user_message):
        number_of_matches = int(user_message.split()[1])
        result = ""
        for i in range(number_of_matches):
            result += match_list[i] + " | "+ fenerbahce_fixture[match_list[i]].strftime("%d %B %Y | %A | %H:%M")+"\n"
        return result
    if re.search(get_ticket_regex, user_message):
        teams = user_message.split()[:-2]
        team_name, opponent_name = teams[0].capitalize(), teams[-1].capitalize()
        return find_ticket(team_name, opponent_name)
    if re.search(get_fixture_regex, user_message):
        team_name = user_message.split()[0].capitalize()
        return get_fixture(team_name)

def get_reamining_time(timedelta):
    result = ""
    if timedelta.days != 0:
        result += f"{timedelta.days} gün "
    if int(timedelta.seconds / 60*60) % 24 != 0:
        result += f"{int(timedelta.seconds / 3600) % 24} saat "
    if int(timedelta.seconds / 60) % 60 != 0:
        result += f"{int(timedelta.seconds / 60) % 60} dakika"
    return result

def find_ticket(team_name, opponent_name):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('w3c', True)
    driver = webdriver.Opera(executable_path=r'C:\Users\ergen\OneDrive\Masaüstü\operadriver_win64\operadriver.exe',options=options)
    url = 'https://www.biletwise.com/tr/super-lig-mac-biletleri'
    driver.get(url)
    driver.implicitly_wait(15)
    teams = driver.find_elements(By.CLASS_NAME, 'upcoming_cat')
    for team in teams:
        if team_name in team.find_element(By.TAG_NAME, 'a').text:
            element = team.find_element(By.CLASS_NAME, 'mb-0')
            driver.execute_script("arguments[0].click();", element)
            break
    driver.implicitly_wait(15)
    matches = driver.find_elements(By.CLASS_NAME, 'mb-3')
    index = 2
    for match in matches:
        title = match.find_element(By.CLASS_NAME, 'mb-1').text
        if opponent_name in title:
            date = match.find_element(By.CLASS_NAME, 'mb-0').text
            price = match.find_element(By.XPATH, f'/html/body/div[5]/div[2]/div[5]/div[1]/div[{index}]/div/div/div/div[2]/p').text
            ticket_link = match.find_element(By.XPATH, f'/html/body/div[5]/div[2]/div[5]/div[1]/div[{index}]/div/div/div/div[3]/a').get_attribute('href')
            return title + " | " + date + " | " + price + " | " + ticket_link
        index += 1

def get_fixture(team_name):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('w3c', True)
    driver = webdriver.Opera(executable_path=r'C:\Users\ergen\OneDrive\Masaüstü\operadriver_win64\operadriver.exe',options=options)
    url = 'https://www.sporx.com/turkiye-super-lig-puan-durumu'
    driver.get(url)
    driver.implicitly_wait(15)
    for i in range(1,21):
        team = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/table[1]/tbody/tr[{i}]/td[4]/a')
        if team_name in team.text:
            driver.execute_script("arguments[0].click();", team)
            break
    result = ""
    for i in range(week_count,39): 
        date = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/table/tbody/tr[{i}]/td[1]').text
        team1 = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/table/tbody/tr[{i}]/td[5]/a').text
        team2 = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/table/tbody/tr[{i}]/td[7]/a').text
        result += team1 + " | " + team2 + " | " + date + ".2022" + "\n"
    return result
