"""
Analyzing Text
The goal is to find related concepts by doing text mining. 
Keywords are extracted from the text and then try to visualize the result.
"""

"""
Step 1: Getting the Data
"""
import requests

url = 'https://en.wikipedia.org/wiki/Data_science'
text = requests.get(url).content.decode('utf-8')
print(text[:1000])

"""
Step 2: Transforming the Data
"""
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    script = False
    res = ""
    def handle_starttag(self, tag, attrs):
        if tag.lower() in ["script","style"]:
            self.script = True
    def handle_endtag(self, tag):
        if tag.lower() in ["script","style"]:
            self.script = False
    def handle_data(self, data):
        if str.strip(data)=="" or self.script:
            return
        self.res += ' '+data.replace('[ edit ]','')

parser = MyHTMLParser()
parser.feed(text)
text = parser.res
print(text[:1000])

"""
Step 3: Getting Insights
"""
import sys
!{sys.executable} -m pip install nlp_rake

# The Rake object is customized with parameters, set the minimum length of a keyword to 5 characters, minimum frequency of a keyword in the document to 3, and maximum number of words in a keyword - to 2. 
import nlp_rake
extractor = nlp_rake.Rake(max_words=2,min_freq=3,min_chars=5)
res = extractor.apply(text)
res # Shows a list terms together with associated degree of importance.

"""
Step 4: Visualizing the Result
"""
# The matplotlib library in Python to plot simple distribution of the keywords with their relevance.
import matplotlib.pyplot as plt

def plot(pair_list):
    k,v = zip(*pair_list)
    plt.bar(range(len(k)),v)
    plt.xticks(range(len(k)),k,rotation='vertical')
    plt.show()

plot(res)

# Another way to visualize word frequencies is using Word Cloud.
!{sys.executable} -m pip install wordcloud

# The WordCloud object takes in either original text, or pre-computed list of words with their frequencies, and returns and image, which can then be displayed using matplotlib.
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wc = WordCloud(background_color='white',width=800,height=600)
plt.figure(figsize=(15,7))
plt.imshow(wc.generate_from_frequencies({ k:v for k,v in res }))

# Passing in the original text to WordCloud.
plt.figure(figsize=(15,7))
plt.imshow(wc.generate(text))

# Using the original text the word cloud has more words, but it also contains a lot of unrelated words. The RAKE algorithm does a better job at selecting good keywords from text. This example illustrates the importance of data pre-processing and cleaning, because a clear picture will help make better decisions.
