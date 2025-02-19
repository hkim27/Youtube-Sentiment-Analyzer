# YouTube Sentiment Analyzer

## Overview
The **YouTube Sentiment Analyzer** is a tool designed to analyze the sentiment of comments on YouTube videos. It processes text data to determine whether the general tone of comments is **positive, negative, or neutral**, providing insights into audience reactions.

## Features
- Fetches YouTube comments using the YouTube Data API
- Performs sentiment analysis using **NLTK** and other NLP techniques
- Supports visualization of sentiment distribution
- Flask-based web application for user interaction

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- **Python 3.10+**
- **pip** (Python package manager)
- **Git**

Also, make sure you pip install:
- **pip install flask**
- **pip install beautifulsoup4**
- **pip install selenium**
- **pip install ntlk**
- **pip install lxml**
- **pip install wordcloud**
- **pip install scipy**
- **pip install matplotlib**
- **pip install vadersentiment**
- **Add --user if you get permission related error**

### Clone the Repository
```sh
git clone https://github.com/hkim27/Youtube-Sentiment-Analyzer.git
cd Youtube-Sentiment-Analyzer/flash
```

### Set Up a Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### Install Dependencies
```sh
pip install flask
pip install beautifulsoup4
pip install selenium
pip install ntlk
pip install lxml
pip install wordcloud
pip install scipy
pip install matplotlib
pip install vadersentiment
```
**Add --user if you get permission related error**

## Usage

### Running the Flask Application
```sh
python -m flask run
```
The application will start locally at `http://127.0.0.1:5000/`.

### Fetching and Analyzing YouTube Comments
1. Select the Search by Channel tab or Search by Video Tab
2. In order to search by channel, input the channel name and then select the number of videos to analyze
3. In order to search by video, input the video url.
4. Select at least one data visualization format.
5. Click **Submit** to fetch comments.
6. View the **sentiment analysis results**.

## Roadmap
- [ ] Improve sentiment analysis accuracy with deep learning models
- [ ] Add real-time comment analysis
- [ ] Enhance visualization with interactive charts

## Contributing
Contributions are welcome! Please follow these steps:
1. **Fork** the repository
2. Create a **new branch**: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature-branch`
5. Open a **Pull Request**

## Contact
For any inquiries, feel free to reach out:
- GitHub: [hkim27](https://github.com/hkim27)
- Email: hakhyunkimchi@gmail.com 

