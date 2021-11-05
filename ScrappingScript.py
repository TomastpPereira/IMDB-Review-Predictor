from requests import get
from bs4 import BeautifulSoup
import pandas as pd

pages = ['https://www.imdb.com/title/tt0903747/episodes?season=1', 'https://www.imdb.com/title/tt0903747/episodes?season=2', 'https://www.imdb.com/title/tt0903747/episodes?season=3', 'https://www.imdb.com/title/tt0903747/episodes?season=4', 'https://www.imdb.com/title/tt0903747/episodes?season=5']
titles = []
releaseDates = []
reviewLinks = []
seasons = []
seasonTrack = 0   # For tracking what season an episode belongs to

for page in pages:
    seasonTrack += 1
    url = page
    response = get(url)
    # print(response.text[:500])

    html_soup = BeautifulSoup(response.text, 'html.parser')

    ep_containers_odd = html_soup.find_all('div', class_='list_item odd')
    ep_containers_even = html_soup.find_all('div', class_='list_item even')

    episode_containers = []
    for i in range(max(len(ep_containers_even), len(ep_containers_odd))):
        if i < len(ep_containers_odd):
            episode_containers.append(ep_containers_odd[i])
        if i < len(ep_containers_even):
            episode_containers.append(ep_containers_even[i])

    for container in episode_containers:
        title = container.strong.a.text
        titles.append(title)

        seasons.append(seasonTrack)

        releaseDate = container.find('div', class_='airdate').text
        releaseDate = releaseDate.strip()
        releaseDates.append(releaseDate)

        episode_code_raw = container.strong.a['href']
        episode_code = episode_code_raw[7: 16]
        episode_reviews = 'https://www.imdb.com/title/{0}/reviews?ref_=tt_urv'
        episode_reviews_adjusted = episode_reviews.replace('{0}', str(episode_code))
        reviewLinks.append(episode_reviews_adjusted)

    test_df = pd.DataFrame({'Name': titles, 'Season': seasons, 'Reviews Link': reviewLinks, 'Date': releaseDates})
print(test_df.info())
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(test_df)
test_df.to_csv('data.csv')