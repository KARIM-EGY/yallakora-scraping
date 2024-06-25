import csv
from bs4 import BeautifulSoup
import requests

date = input('write the date to get the matches of the date (MM/DD/YYYY) : ')
URL = (f'https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}')
# requesting the data from the website
page = requests.get(URL).content
match_table = []  # creating list of the output


def main(source):
    soup = BeautifulSoup(source, "lxml")
    championship_title = soup.find_all('div', {'class': 'matchCard'})  # selecting the match info

    def get_match_info(championship_name):
        champions_title = championship_name.contents[1].find('h2').text.strip()  # get the championship name
        teams = championship_name.contents[3].find_all('div', {'class': 'teamsData'})  # selecting all the teams
        matches_count = int(len(teams))  # estimate the number matches by dividing numbers of teams over 2

        for i in range(matches_count):
            # get the teams
            team1 = teams[i].find('div', {'class': 'teamA'}).text.strip()
            team2 = teams[i].find('div', {'class': 'teamB'}).text.strip()
            # get the scores
            score = teams[i].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            #  but this will return the number of goals of each team separate, so it should be combined
            total_score = f'{score[0].text.strip()}-{score[1].text.strip()}'  # combining the score
            # get the time of the match beginning
            match_time = teams[i].find('span', {'class': 'time'}).text.strip()
            # add the data to the list of the match table
            match_table.append({'البطولة ': champions_title,
                                'الذهاب': team1,
                                'العوده': team2,
                                'النتيجه': total_score,
                                ' ضربة البداية': match_time})

    for i in range(len(championship_title)):
        get_match_info(championship_title[i])

    keys = match_table[0].keys()

    with open(r'C:\Users\Reda\Desktop\KP\jupyter\yallakora.csv', 'w' , encoding='utf-8') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(match_table)
        print('file created')


main(page)
print(match_table)
