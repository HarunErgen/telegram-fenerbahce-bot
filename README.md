# Telegram Fenerbahce Bot
Selman the bot provides information about the fixtures of the teams, sends links of the match tickets to the users, and calculates how much time is left for the matches of Fenerbahçe.

Bot is created via telegram library. Commands and messages are handled by the functions of the library. My API key and chat IDs are stored in a separate file named constants.py. I used Selenium to scrape data of team fixtures and match tickets from the websites 'www.biletwise.com' and 'www.sporx.com'. By using the datetime library, I calculated how much time is left for the matches, what week it is in the Süper Lig and when the soonest match of the Fenerbahçe is. I determine the commands of the users through regular expression and provide the required response to the users.  

![2022-01-31_04-49-18 (2)](https://user-images.githubusercontent.com/83069560/151731421-bc69999b-ac33-4ad0-85e9-c76be2944c46.png)

![2022-01-31_04-50-41 (2)](https://user-images.githubusercontent.com/83069560/151731446-c6329fa5-7140-4078-b232-161a58c3aa8d.png)

![2022-01-31_04-51-59 (4)](https://user-images.githubusercontent.com/83069560/151731453-684df154-19e8-42b3-b60f-7a36e6e4f9a8.png)

