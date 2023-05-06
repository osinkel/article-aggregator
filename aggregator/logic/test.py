from googletrans import Translator
from newspaper import Article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def calculate_mood_level(text: str, lang: str):
    translator = Translator()
    if not 'en' in lang:
        text = translator.translate(text, dest='en').text
        
    sentiment = SentimentIntensityAnalyzer()
    return sentiment.polarity_scores(text)


url = "https://aif.ru/money/v_centrobanke_otvetili_na_27_samyh_populyarnyh_voprosov_o_cifrovom_ruble"
article = Article(url)
article.download()
article.parse()
text = article.text.replace('\n', ' ')
translator = Translator()
text = translator.translate(text, dest='en').text
print(text)
sentiment = SentimentIntensityAnalyzer()
print(sentiment.polarity_scores(text))  

