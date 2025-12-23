````markdown
id: music_downloader_readme
name: Improved README for Music Downloader Project
type: markdown
content: |-
  # Music Downloader (Python Web Scraping Practice)

  ## Description
  This project is a practice exercise in web scraping using Python. It downloads popular music tracks from the website [pop-music.ir](http://pop-music.ir/) based on user ratings (songs with more than 15,000 views are selected). The script uses `BeautifulSoup4` for HTML parsing and `requests` for HTTP interactions.

  **Note:** Before running the code, update the `saving_path` variable to your desired directory on your hard drive. Have fun! 🎵

  ## Features
  - Scrapes song pages based on popularity (view count > 15,000).
  - Extracts direct download links from selected pages.
  - Downloads songs in MP3 format to a specified path.
  - Processes multiple pages (configurable from page 1 to 40).
  - Handles large files with chunked downloading.

  ## Prerequisites
  - Python 3.x
  - Required libraries: `beautifulsoup4`, `requests`
  - Install dependencies via pip:
    ```bash
    pip install beautifulsoup4 requests
    ```

  ## Usage
  1. Clone or download the repository.
  2. Open the script and modify the `saving_path` variable (e.g., `saving_path = '/path/to/your/download/folder'`).
  3. Run the script:
     ```bash
     python music_downloader.py
     ```
  4. The script will iterate through pages, select songs, and download them automatically.

  ## Disclaimer
  - This project is for educational purposes only, demonstrating web scraping techniques.
  - Downloading copyrighted music without permission may violate laws and terms of service. Ensure you have the right to download and use the content. The author is not responsible for any misuse.
  - Respect website policies and avoid overloading servers (consider adding delays between requests in production code).

  ## Source Code
  ```python
  from bs4 import BeautifulSoup
  import requests
  import re
  from urllib.parse import unquote
  import os.path

  def send_request(url):  # Send requests to a website address
      response = requests.get(url)
      stc = response.status_code
      if stc == 200:
          return response.text
      else:
          print('Something went wrong with error code: %i' % stc)

  # rate_ling function is for creating a dictionary of rate:url from every song which its rate is
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

  # This function is for scraping final song's links from a list of
  # input URLs of selected pages
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

  saving_path = '/media/ramin/2A7E79687E792DA7/new download'  # For saving on computer
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
  ```

  ## Contributing
  Feel free to fork and improve the code. Pull requests are welcome!

  ## License
  This project is open-source. Use at your own risk.
````

این README بهبودیافته است: ساختارمندتر، دقیق‌تر (املاها اصلاح شده)، و شامل بخش‌های ضروری مثل ویژگی‌ها، پیش‌نیازها، نحوه استفاده، و هشدار حقوقی است. کد منبع هم در بلوک کد قرار گرفته تا خواناتر باشد. شما می‌توانید این را کپی کرده و در فایل `README.md` ریپازیتوری خود قرار دهید. اگر نیاز به تغییرات بیشتری دارید، بگید! 😊
