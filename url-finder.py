from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import unquote
import os.path


def send_request(url):  # send requests to a website address
    response = requests.get(url)
    stc = response.status_code
    if stc == 200:
        return response.text
    else:
        print('something went wrong with error code: %i' % stc)


# rate_ling function is for creating a dictionary of rate:url from every song which it's rate is
# more than the specified limit as popularity based on user's comments
def nominated_page_links(text, rt_pattern, dlp_pattern, rt_limit):
    soup = BeautifulSoup(text, 'html.parser')
    all_posts = soup.findAll('article', class_='post')
    ratings_list = re.findall(rt_pattern, str(all_posts))
    links_list = re.findall(dlp_pattern, str(all_posts))
    nominated_links = []
    for i in range(len(ratings_list)):
        numeric_rating_list = int(''.join(ratings_list[i].split(',')))
        if numeric_rating_list > rt_limit:
            nominated_links.append(links_list[i])
    return nominated_links


# this function is for scrape final song's links from a list of
# input url of selected pages
def download_link_finder(dl_lst):
    link_pattern = r'<a download="" href="(.*)" title=.*>\s*.*\s*</a>'
    final_link_list = []
    for link in dl_lst:
        res = send_request(link)
        soup = BeautifulSoup(res, 'html.parser')
        result = soup.find('p', class_='downloader')
        final_link = re.findall(link_pattern, str(result.a))
        final_link_list.append(final_link[0])
    return final_link_list


def download_songs(list_of_songs_url, save_path):
    for link in list_of_songs_url:
        res = requests.get(link, stream=True)
        splitted = link.split('/')
        song_name = unquote(str(splitted[-1]))
        final_saving_path = os.path.join(save_path, song_name)
        print('Downloading %s is in progress...' % song_name)
        with open(final_saving_path, 'wb') as mp3:
            for chunk in res.iter_content(chunk_size=1024*1024):
                if chunk:
                    mp3.write(chunk)
        print('Download completed!')


saving_path = '/media/ramin/2A7E79687E792DA7/new download'  # for saving on computer
first_page_no = 1
last_page_no = 40
dl_pages_list = []
rating_limit = 15000
rating_pattern = r'\s<span class="view">(.*)بازدید</span>\s'
download_page_pattern = r'<div class="morelink"><a href="(.*?)">.*</a>'
while first_page_no <= last_page_no:
    website_url = "http://pop-music.ir/category/single-music/page/"+str(first_page_no)
    response_text = send_request(website_url)
    new_lst = nominated_page_links(response_text, rating_pattern, download_page_pattern, rating_limit)
    dl_pages_list = dl_pages_list + new_lst
    print('There is/are %i song(s) available in page %i.' % (len(new_lst), first_page_no))
    first_page_no += 1
print('There are a total number of %i songs ready for download!' % len(dl_pages_list))
songs_list = download_link_finder(dl_pages_list)
download_songs(songs_list, saving_path)
