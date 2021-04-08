import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt

text = ''

with open("./data/all_unclassified_data_shuffled.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for index, row in enumerate(csv_reader):
        text += row['body']

wordcloud = WordCloud(
    background_color='black',
    width=1280,
    height=800,
).generate(text)

plt.axis('off')
plt.imshow(wordcloud, interpolation='bilinear')
plt.show()