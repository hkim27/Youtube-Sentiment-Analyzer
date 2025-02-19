##pip install flask
from flask import Flask, render_template, request, url_for, flash, redirect
from .youtubeScraper import scraper 
from .sentimentAnalyzer import sentimentAnalyzerMain
from .data_visualizer import graph_data
from .data_visualizer import export_data
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '75874bc47a9ca89148118e3947adf6a3570f13132fa98cd4'

# Global var used for scraper
mode = ""
channelName = ""
numVideos = 0
link = ""

# Global var list used for data visualizer
options = [0] * 8  # Shortened initialization

# Function to reset options to 0
def reset_options():
    for i in range(len(options)):
        options[i] = 0

@app.route('/')
# loads home screen
def home():
    return render_template('landingpage.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # var that holds which tab the user has clicked on (search by channel or search by vid)
        selectedValue = request.form['group']
        
        # if user has clicked on the channel tab
        if selectedValue == 'c':
            mode = "channel"
            # get channel name
            channelName = request.form['cName']
            # get num videos
            numVideosInput = request.form['nVideos']
            numVideos = int(numVideosInput) if numVideosInput else 0
            link = ""
            # give error message if channel name is not inputted
            if not channelName:
                flash("Channel Name is required!")
                return redirect(url_for('home'))

        # if user has clicked on the video tab
        else:
            mode = "video"
            channelName = ""
            numVideos = 0
            link = request.form['vURL']
            # give error message if link is not inputted
            if not link:
                flash("A video URL is required!")
                return redirect(url_for('home'))

        # check which data format(s) user has chosen
        if request.form.get("pieGraph"):
            options[0] = 1
        if request.form.get("histogram"):
            options[1] = 1
        if request.form.get("lineChart"):
            options[2] = 1
        if request.form.get("wordcloud"):
            options[3] = 1
        if request.form.get("circleChart"):
            options[4] = 1
        if request.form.get("density"):
            options[5] = 1
        if request.form.get("scatterplot"):
            options[6] = 1
        if request.form.get("boxplot"):
            options[7] = 1

        # Ensure at least one data format is selected
        if all(opt == 0 for opt in options):
            flash("You must select at least one data visualization format!")
            return redirect(url_for('home'))

        # Call scraper
        validID, hasVideos, validLink = scraper(mode, channelName, numVideos, link)
        print("I am getting here")

        # Handle errors based on the scraper results
        if validID == 0:
            reset_options()
            flash("Channel name is not valid!")
            return redirect(url_for('home'))
        
        if hasVideos == 0:
            reset_options()
            flash("The channel does not have any videos!")
            return redirect(url_for('home'))

        if validLink == 0:
            reset_options()
            flash("The link is invalid!")
            return redirect(url_for('home'))

        # Call sentiment analyzer
        sentimentAnalyzerMain("rawComments.txt")
        
        # Call visualizer
        graph_data(options, "analysisResults.txt", "static/resultpageimgs/")
        
        # Delete the temporary files
        try:
            os.remove("rawComments.txt")
            os.remove("analysisResults.txt")
        except OSError as e:
            print(f"Error deleting files: {e}")

        return render_template('resultPage.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        selectedValue = request.form['action']
        
        if selectedValue == "Download":
            # Call export_data function to create the zip file
            export_data(options, "flash/", "static/resultpageimgs/")
            
            # Reset options
            reset_options()

            # Safely remove text files if they exist
            for file in ["analysisResults.txt", "rawComments.txt"]:
                file_path = os.path.join("flash", file)
                if os.path.exists(file_path):
                    os.remove(file_path)

            return redirect(url_for('home'))
        
        if selectedValue == "Home":
            # Reset options
            reset_options()

            # Safely remove text files if they exist
            for file in ["analysisResults.txt", "rawComments.txt"]:
                file_path = os.path.join("flash", file)
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
