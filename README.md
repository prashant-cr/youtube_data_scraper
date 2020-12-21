# youtube_data_scraper
The Project is basically scraping the data from the youtube using the youtube free apis.

# steps to setup
1. Install requirements.txt file in your virtual environments.
2. Run youtube_scraper.py file to start scraping.

# what this scraper scrapes from youtube
1. According to your key word on scraper file it will scrape the all channels info.
2. It will scrape channel link, channel name, subscribers, total views. email addresses, description.

# important points
1. This project is basically uses the youtube apis. YouTube Apis do have the limitation on per day api counts.
2. After reaching YouTube API limitation count it will give 403 error So make sure to have 
   page count less than 70 in code.
3. You can change the configurations according to your need like keyword, page count in code.
