##### Reqs:
##### pip install pip install beautifulsoup4
##### pip install pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
#from selenium import webdriver
#from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
# Global variables
#validID = 1
#hasVideos = 1
#validLink = 1
commentsWritten = 0

def scraper(mode, channelID, numVideos, link):
    # Variables
    validID = 1
    hasVideos = 1
    validLink = 1
    videoLinks = []
    # Setup driver options
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    #options.add_argument('--headless=new')
    # Channel Mode
    if (mode == "channel"):
        # Get video links
        channelUrl = get_channel_page(channelID)
        # Create driver
        service = Service(r"C:\\Users\\hakhyun\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
        # Scrape channel page for links to videos
        videoLinks, validID, hasVideos = scrape_channel_page(channelUrl, numVideos, driver, validID, hasVideos)
        # Exit driver
        driver.quit()

    # Video Mode
    else:
        # Get single link
        videoLinks.append(link)
    # Both Modes
    for video in videoLinks:
        # Create driver
        service = Service(r"C:\\Users\\hakhyun\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
        # Scrape video for comments
        validLink = scrape_video_comments(video, driver, validLink)
        
        # Exit driver
        driver.quit()
        print("i am getting out of scrape_video_comments")

    return validID, hasVideos, validLink

# Input: channel id
# Output: url to the channel page
def get_channel_page(channelID):
    if(channelID.startswith("@")):
        url = "https://www.youtube.com/" + channelID + "/videos"
    else: 
        url = "https://www.youtube.com/@" + channelID + "/videos"
    print("[DEBUG] Channel URL: " + url)
    return url

# Input: url to channel page, number of videos to scrape, driver
# Output: array of video urls
def scrape_channel_page(channelURL, numVideos, driver, validID, hasVideos):
    # Setup variables
    videoLinks = []
    linksScraped = 0
    #global validLink
    # Get to channel page with Selenium
    driver.get(channelURL)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    # Start soup
    if(html and soup):
        # Get title tag for debugging
        for title in soup.find_all('title'):
            print("[DEBUG] Title: " + title.text)
            if (title.text == "404 Not Found"):
                #validLink = 1
                validID = 0
                #hasVideos = 1
                print("[ERROR] Invalid channel ID")
                return videoLinks, validID, hasVideos
        print("[DEBUG] Valid channel ID")
        # Print all followable links on the main channel page
        for a in soup.find_all('a', href=True):
            if (linksScraped == numVideos):
                break
            if (a['href'].startswith("/watch") and "https://www.youtube.com" + a['href'] not in videoLinks):
                videoLinks.append("https://www.youtube.com" + a['href'])
                linksScraped += 1
                print("[DEBUG] ADDED: " + a['href'])
        # Determine if channel has no videos on it
        if (linksScraped == 0):
            hasVideos = 0
            #validID = 1
            #validLink = 1
            print("[ERROR] Channel has no videos")
    else:
        print("Soup failed.")
    # Return the video links
    return videoLinks , validID, hasVideos

def scrape_video_comments(url, driver, validLink):
    # Variables
    #global validID
    #global validLink
    #global hasVideos
    scrollNum = 0
    timesToScroll = 10
    comments = []
    # Scrape the video for comments
    #with driver:
    wait = WebDriverWait(driver,1)
    print("[DEBUG] URL: " + url)
    driver.get(url)
    print("[DEBUG] Title: " + driver.title)
    # Determine if video link is invalid
    if (driver.title == "- YouTube"):
        #validID = 1
        #hasVideos = 1
        validLink = 0
        print("[ERROR] Invalid video link")
        return validLink
    # Scroll and get comments
    for scrollNum in range(timesToScroll):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(1)   # time to wait between scrolls
    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
        comments.append(comment.text)
    print("[DEBUG] Comments Found: ", len(comments))
    # Write comments to rawComments.txt
    #with open(r"D:\\Code\\Python\\Software_Engineering_Project\\rawComments.txt", "a", encoding="utf-8") as f:
    with open(r"C:\\Users\\hakhyun\\youtube_analyzer\\flash\\rawComments.txt", "a", encoding="utf-8") as f:
        for comment in comments:
            print(comment)
            f.write(comment)
            f.write("ENDOFCOMMENT ")
    print("done writing comments")
    return validLink

# For stand-alone testing
#scraper("channel", "@LofiGirl", 1, "") # Valid channel case, single video
#scraper("channel", "@LofiGirl", 2, "") # Valid channel case, mutliple videos
#scraper("video", "", 0, "https://www.youtube.com/watch?v=n61ULEU7CO0") # Valid video case
#scraper("channel", "abwongbaeouwgbaeiugbwaegbwegw", 2, "") # Invalid channel id
#scraper("channel", "@aaaaaaaaaaaaaaaaaaaa", 1, "") # Invalid channel case, no videos on channel case
#scraper("video", "", 0, "https://www.youtube.com/watch?v=cDiabnosezb") # Invalid url