from bs4 import BeautifulSoup # import BeautifulSoup
import requests # import requests
import json # import json

# create request to archive page
blog_archive_url = 'https://enlear.academy/archive/2022/01'
response = requests.get(blog_archive_url)
# parse the resposne using HTML parser on BeautifulSoup
parsedHtml = BeautifulSoup(response.text, 'html.parser')

# get list of all divs having the classes "streamItem streamItem--postPreview js-streamItem" to get each story.
stories = parsedHtml.find_all('div', class_='streamItem streamItem--postPreview js-streamItem')

formatted_stories = []

for story in stories:
    # get the title of the story
    story_title = story.find('h3').text if story.find('h3') else 'N/A'
    # get the subtitle of the story
    story_subtitle = story.find('h4').text if story.find('h4') else 'N/A'

    # get the number of claps
    clap_button = story.find('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents')
    claps = 0
    if (clap_button):
        # if clap button has a DOM reference, obtain its text
        claps = clap_button.text
    
    # get reference to the card header containing author info
    author_header = story.find('div', class_='postMetaInline u-floatLeft u-sm-maxWidthFullWidth')
    # access the reading time span element and get its title attribute
    reading_time = author_header.find('span', class_='readingTime')['title']

    # get read more ref
    read_more_ref = story.find('a', class_='button button--smaller button--chromeless u-baseColor--buttonNormal')
    url = read_more_ref['href'] if read_more_ref else 'N/A'

    # add an object to formatted_stories
    formatted_stories.append({
        'title': story_title,
        'subtitle': story_subtitle,
        'claps': claps,
        'reading_time': reading_time,
        'url': url
    })

file = open('stories.json', 'w')
file.write(json.dumps(formatted_stories))