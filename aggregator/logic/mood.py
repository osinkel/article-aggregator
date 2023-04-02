from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging

logger = logging.getLogger()

translator = Translator()

def calculate_mood_level(text: str):
    pass


def translate_text_to_en(text: str) -> str:
    translated_text = ''
    try:
        translated_text = translator.translate(text, dest='en')
        translated_text = translated_text.text
    except Exception as exc: 
        logger.exception(exc)
    return translate_text.text


sentiment = SentimentIntensityAnalyzer()
sent_1 = sentiment.polarity_scores(a)
print("Sentiment of text 1:", sent_1)