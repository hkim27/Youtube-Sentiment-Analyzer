import matplotlib.pyplot as plt
import numpy as np
import os
import re
from scipy.stats import gaussian_kde
import string
from wordcloud import WordCloud, STOPWORDS
from zipfile import ZipFile

# Regex patterns to parse the analysis results file
WORD_FREQ_LINE =  re.compile("^\w+ \d+$")
NUM_COMMENTS_LINE =  re.compile("^Number of Comments: \d+$")
POSITIVE_SENT_LINE = re.compile("^Positive Sentiment:") 
NEUTRAL_SENT_LINE = re.compile("^Neutral Sentiment:")
NEGATIVE_SENT_LINE = re.compile("^Negative Sentiment:")
OVERALL_SENT_LINE = re.compile("^Overall Sentiment:")

SENTIMENT_TYPES = ["Positive", "Neutral", "Negative"]

# Controls how big the figures are in inches
FIG_WIDTH = 12
FIG_HEIGHT = (FIG_WIDTH / 16) * 9

ALPHA_VALUE = 0.75 # Controls the transparency of each plot

text_kwargs = dict(ha='center', va='center', fontsize=48, color='tab:gray')

#TESTING = False # Used to enable the plots to be shown to the screen. Disable for system integration.

# Gets the data from the analysisResults.txt file
def get_data(data_file: str):
    words_dict = {}   # Stores the words and their frequencies
    pos_sent = []     # Stores the Positive sentiment values
    neutral_sent = [] # Stores the Neutral sentiment values
    neg_sent = []     # Stores the Negative sentiment values
    overall_sent = {} # Stores the Overall sentiment types

    # Reads the data from the anaylsis results data_file file
    with open(data_file) as file:
        for line in file:
            # Gets the words and their frequencies
            if (bool(re.search(WORD_FREQ_LINE, line))):
                line_list = line.split()

                if (not(line_list[0] == "'s" or line_list[0].isspace() or line_list[0] in string.punctuation)):
                    words_dict[line_list[0].capitalize()] = int(line_list[1])

            # Gets the positive sentiment values
            elif (bool(re.search(POSITIVE_SENT_LINE, line))):
                pos_sent = re.findall("\d.\d+", line)
                for i in range(len(pos_sent)):
                    pos_sent[i] = float(pos_sent[i])*100

            # Gets the neutral sentiment valuesv
            elif (bool(re.search(NEUTRAL_SENT_LINE, line))):
                neutral_sent = re.findall("\d.\d+", line)
                for i in range(len(neutral_sent)):
                    neutral_sent[i] = float(neutral_sent[i])*100

            # Gets the negative sentiment values
            elif (bool(re.search(NEGATIVE_SENT_LINE, line))):
                neg_sent = re.findall("\d.\d+", line)
                for i in range(len(neg_sent)):
                    neg_sent[i] = float(neg_sent[i])*100

            # Gets the overall sentiment types
            elif (bool(re.search(OVERALL_SENT_LINE, line))):
                pos = re.findall(SENTIMENT_TYPES[0], line)
                neutral = re.findall(SENTIMENT_TYPES[1], line) 
                neg = re.findall(SENTIMENT_TYPES[2], line)

                overall_sent[SENTIMENT_TYPES[0]] = len(pos)
                overall_sent[SENTIMENT_TYPES[1]] = len(neutral)
                overall_sent[SENTIMENT_TYPES[2]] = len(neg)

        #if (TESTING):
            #print(f"Word Dictionary     = {words_dict}")
            #print(f"Posivitve Sentiment = {pos_sent}")
            #print(f"Neurtal Sentiment   = {neutral_sent}")
            #print(f"Negative Sentiment  = {neg_sent}")
            #print(f"Overall Sentiment   = {overall_sent}") 

    return words_dict, pos_sent, neutral_sent, neg_sent, overall_sent


# Generates the selected plots of the data 
def graph_data(option: list[int], analysis_file: str, png_path: str) -> None:
    # Removes old plot PNGs so that they are not zipped if not selected
    #for file in os.listdir(png_path):
    #    os.remove(f"{png_path}{file}")

    # Gets the data from the analysis file
    words_dict, pos_sent, neutral_sent, neg_sent, overall_sent = get_data(analysis_file)

    # Number of comments
    comment_num_list = [i+1 for i in range(len(neutral_sent))]

    # Extracted words and their frequencies
    words = list(words_dict.keys())
    freqs = list(words_dict.values())

    # Stores the number of positive, neutral, and negative sentiments of the comments
    sent_values = list(overall_sent.values())

    # Pie Chart
    if (option[0]):
        #print("Creating Pie Chart....... ", end='')

        fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
        ax.pie(sent_values, labels=SENTIMENT_TYPES, autopct='%1.1f%%', pctdistance=0.5, colors=['green', 'blue', 'red'], wedgeprops={"alpha":ALPHA_VALUE})
        plt.title("Overall Sentiment Pie Chart")
        plt.savefig(fname=f"{png_path}pie_chart.png", format='png', bbox_inches='tight')
        
        #print("Done")
    else:
        plt.figure(figsize=(FIG_WIDTH/2, FIG_HEIGHT/2))
        plt.title("Overall Sentiment Pie Chart")
        plt.axis(False)
        plt.text(0.5, 0.5, 'Not Selected',  **text_kwargs)
        plt.savefig(fname=f"{png_path}pie_chart.png", format='png', bbox_inches='tight')


    # Histogram
    if (option[1]):
        #print("Creating Histogram....... ", end='')

        num_bins = 10
        pos_counts, pos_bins = np.histogram(pos_sent, bins=num_bins, range=(0.0, 100.0))
        neutral_counts, neutral_bins = np.histogram(neutral_sent, bins=num_bins, range=(0.0, 100.0))
        neg_counts, neg_bins = np.histogram(neg_sent, bins=num_bins, range=(0.0, 100.0))

        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

        # Positve Sentiment
        plt.hist(pos_bins[:-1], pos_bins, weights=pos_counts, color='green', alpha=ALPHA_VALUE, label='Positive')

        # Neutral Sentiment
        plt.hist(neutral_bins[:-1], neutral_bins, weights=neutral_counts, color='blue', alpha=ALPHA_VALUE, label='Neutral')

        # Negative Sentiment
        plt.hist(neg_bins[:-1], neg_bins, weights=neg_counts, color='red', alpha=ALPHA_VALUE, label='Negative')

        plt.title("Overall Sentiment Histogram")
        plt.xlabel("Percentage of Sentiment Type Per Comment")
        plt.ylabel("Frequency")
        plt.legend()
        plt.draw()
        plt.savefig(fname=f"{png_path}histogram.png", format='png', bbox_inches='tight')

        #print("Done")
    else:
        plt.figure(figsize=(FIG_WIDTH/2, FIG_HEIGHT/2))
        plt.title("Overall Sentiment Histogram")
        plt.axis(False)
        plt.text(0.5, 0.5, 'Not Selected',  **text_kwargs)
        plt.savefig(fname=f"{png_path}histogram.png", format='png', bbox_inches='tight')


    # Line Chart
    if (option[2]):
        #print("Creating Line Chart...... ", end='')

        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        plt.plot(comment_num_list, pos_sent, color='green', label='Positive', alpha=ALPHA_VALUE)
        plt.plot(comment_num_list, neutral_sent, color='blue', label='Neutral', alpha=ALPHA_VALUE)
        plt.plot(comment_num_list, neg_sent, color='red', label='Negative', alpha=ALPHA_VALUE)
        plt.grid(True)
        plt.title("Overall Sentiment Line Chart")
        plt.xlabel("Comment Number")
        plt.ylabel("Percentage of Sentiment")
        plt.legend()
        plt.draw()
        plt.savefig(fname=f"{png_path}line_chart.png", format='png', bbox_inches='tight')

        #print("Done")
    else:
        plt.figure(figsize=(FIG_WIDTH/2, FIG_HEIGHT/2))
        plt.title("Overall Sentiment Line Chart")
        plt.axis(False)
        plt.text(0.5, 0.5, 'Not Selected',  **text_kwargs)
        plt.savefig(fname=f"{png_path}line_chart.png", format='png', bbox_inches='tight')
    

    # Word Cloud
    if (option[3]):
        #print("Creating Word Cloud...... ", end='')

        word_str = ""

        for i in range(len(words)):
            for j in range(freqs[i]):
                word_str += f"{words[i]} "
        
        wordcloud = WordCloud(background_color="black", 
                              width=1920, height=1080, 
                              stopwords=STOPWORDS,
                              colormap='tab10',
                              collocations=False).generate(word_str)

        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        plt.imshow(wordcloud)
        #plt.title("Word Cloud")
        plt.axis('off')
        plt.draw()
        plt.savefig(fname=f"{png_path}word_cloud.png", format='png', facecolor='k', bbox_inches='tight')

        #print("Done")
    else:
        plt.figure(figsize=(FIG_WIDTH/2, FIG_HEIGHT/2))
        plt.title("Word Cloud")
        plt.axis(False)
        plt.text(0.5, 0.5, 'Not Selected',  **text_kwargs)
        plt.savefig(fname=f"{png_path}word_cloud.png", format='png', bbox_inches='tight')


    # Circle Chart
    if (option[4]):
        #print("Creating Circle Chart.... ", end='')
        
        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        plt.scatter(0, 0, s=0)
        plt.scatter(1, sent_values[0], s=sent_values[0]*100, color='green', alpha=ALPHA_VALUE)
        plt.scatter(2, sent_values[1], s=sent_values[1]*100, color='blue', alpha=ALPHA_VALUE)
        plt.scatter(3, sent_values[2], s=sent_values[2]*100, color='red', alpha=ALPHA_VALUE)
        plt.scatter(4, max(sent_values)*1.35, s=0)
        plt.title("Overall Sentiment Circle Chart")
        plt.xlabel("Sentiment Type")
        plt.xticks([0, 1, 2, 3, 4], labels=['','Positive', 'Neutral', 'Negative', ''])
        plt.ylabel("Frequency")
        plt.draw()
        plt.savefig(fname=f"{png_path}circle_chart.png", format='png', bbox_inches='tight')

        #print("Done")
    else:
        plt.figure(figsize=(FIG_WIDTH/2, FIG_HEIGHT/2))
        plt.title("Overall Sentiment Circle Chart")
        plt.axis(False)
        plt.text(0.5, 0.5, 'Not Selected',  **text_kwargs)
        plt.savefig(fname=f"{png_path}circle_chart.png", format='png', bbox_inches='tight')


    # Density Chart
    if (option[5]):
        #print("Creating Density Chart... ", end='')

        # Postive Sentiment Density
        pos_density = gaussian_kde(pos_sent)
        pos_density.covariance_factor = lambda: 0.5
        pos_density._compute_covariance()

        # Neutral Sentiment Density
        neutral_density = gaussian_kde(neutral_sent)
        neutral_density.covariance_factor = lambda: 0.5
        neutral_density._compute_covariance()
        
        # Negative Sentiment Density
        neg_density = gaussian_kde(neg_sent)
        neg_density.covariance_factor = lambda: 0.5
        neg_density._compute_covariance()

        line = np.linspace(0, len(comment_num_list), len(comment_num_list)*2)

        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        plt.plot(line, pos_density(line), color='green', label='Positive', alpha=ALPHA_VALUE)
        plt.plot(line, neutral_density(line), color='blue', label='Neutral', alpha=ALPHA_VALUE)
        plt.plot(line, neg_density(line), color='red', label='Negative', alpha=ALPHA_VALUE)
        plt.title("Overall Sentiment Density Plot")
        plt.xlabel("Number of Comments")
        plt.ylabel("Density")
        plt.legend(loc=1)
        plt.draw()
        plt.savefig(fname=f"{png_path}density_plot.png", format='png', bbox_inches='tight')

        #print("Done")
    else:
        plt.figure(figsize=(FIG_WIDTH/2, FIG_HEIGHT/2))
        plt.title("Overall Sentiment Density Plot")
        plt.axis(False)
        plt.text(0.5, 0.5, 'Not Selected',  **text_kwargs)
        plt.savefig(fname=f"{png_path}density_plot.png", format='png', bbox_inches='tight')


    # Scatter Plot
    if (option[6]):
        #print("Creating Scatter Plot.... ", end='')

        plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
        plt.scatter(comment_num_list, pos_sent, color='green', label='Positive', alpha=ALPHA_VALUE)
        plt.scatter(comment_num_list, neutral_sent, color='blue', label='Neutral', alpha=ALPHA_VALUE)
        plt.scatter(comment_num_list, neg_sent, color='red', label='Negative', alpha=ALPHA_VALUE)
        plt.grid(True)
        plt.title("Overall Sentiment Scatter Plot")
        plt.xlabel("Comment Number")
        plt.ylabel("Percentage of Sentiment")
        plt.legend()
        plt.draw()
        plt.savefig(fname=f"{png_path}scatter_plot.png", format='png', bbox_inches='tight')

        #print("Done")
    else:
        plt.figure(figsize=(FIG_WIDTH/2, FIG_HEIGHT/2))
        plt.title("Overall Sentiment Scatter Plot")
        plt.axis(False)
        plt.text(0.5, 0.5, 'Not Selected',  **text_kwargs)
        plt.savefig(fname=f"{png_path}scatter_plot.png", format='png', bbox_inches='tight')


    # Box Plot
    if (option[7]):
        #print("Creating Box Plot........ ", end='')

        fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
        bp = ax.boxplot([pos_sent, neutral_sent, neg_sent], patch_artist=True)

        colors = ['#00ff00', '#0000ff', '#ff0000']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(ALPHA_VALUE)

        plt.title("Overall Sentiment Box Plot")
        ax.set_xticklabels(['Positive', 'Neutral', 'Negative'])
        plt.xlabel("Sentiment Type")
        plt.ylabel("Percentage of Sentiment")
        plt.draw()
        plt.savefig(fname=f"{png_path}box_plot.png", format='png', bbox_inches='tight')

        #print("Done")
    else:
        plt.figure(figsize=(FIG_WIDTH/2, FIG_HEIGHT/2))
        plt.title("Overall Sentiment Box Plot")
        plt.axis(False)
        plt.text(0.5, 0.5, 'Not Selected',  **text_kwargs)
        plt.savefig(fname=f"{png_path}box_plot.png", format='png', bbox_inches='tight')

    #if (TESTING):
    #    print("\nShowing plots to screen...")
    #    plt.pause(0.001) # Shows the plots in separate windows for testing
 

# Exports the plots into a convenient zip file that the user can download
def export_data(options: list[int], export_path: str, png_path: str) -> None:
    zip_file = f"{export_path}Data_Plots.zip"
    with ZipFile(zip_file, mode='w') as archive:
        for file in sorted(os.listdir(png_path)):
            zip_file = False

            # Determines whether to zip the plot PNG depending on if the user selected to generate the plot
            if (options[0] and file == "pie_chart.png"):
                print("0")
                zip_file = True

            elif (options[1] and file == "histogram.png"):
                print("1")
                zip_file = True

            elif (options[2] and file == "line_chart.png"):
                print("2")
                zip_file = True

            elif (options[3] and file == "word_cloud.png"):
                print("3")
                zip_file = True
            
            elif (options[4] and file == "circle_chart.png"):
                print("4")
                zip_file = True
            
            elif (options[5] and file == "density_plot.png"):
                print("5")
                zip_file = True

            elif (options[6] and file == "scatter_plot.png"):
                print("6")
                zip_file = True

            elif (options[7] and file == "box_plot.png"):
                print("7")
                zip_file = True

            # Save the plot PNG to the zip file if it was selected 
            if (zip_file):
                archive.write(f"{png_path}{file}", os.path.basename(f"{png_path}{file}"))
    #print("Saved plots to 'Data_Plots.zip'")


#def main() -> None:
#    ANALYSIS_FILE = "../SentimentAnalyzer/analyisResults.txt"
#    PLOTS_DIR = "./Plots/"
#
#    # This will store the state of the plots the user selected to generate. 1 == Enabled, 0 == not selected
#    options = [ 1, # Pie Chart
#                1, # Histogram
#                1, # Line Chart
#                1, # Word Cloud
#                1, # Circle Chart
#                1, # Density Chart
#                1, # Scatter Plot
#                1  # Box Plot
#            ]
#
#    #print("Graphing results of sentiment analysis...\n")
#    graph_data(options, ANALYSIS_FILE, PLOTS_DIR)
#
#    #if (TESTING):
#    #    input("\nPress 'Enter' to close all plots...\n")
#    #    plt.close('all')
#    
#    export_data(options, "./", PLOTS_DIR)
#
#if __name__ == '__main__':
#    main()
    