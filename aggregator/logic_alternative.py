from newspaper import Article as NewsPaper, build as build_main_page
import nltk
from aggregator.models import Domain, Article
import logging

logger = logging.getLogger()


nltk.download('punkt')

def parse_domain(domain_name: str) -> NewsPaper:
    try:
        domain = Domain.objects.get(name=domain_name)
    except Domain.DoesNotExist:
        logger.warning(f"Domain '{domain_name}' is not found in db. Add such domain to database!")
        return

    logger.warning(f'start parsing of {domain_name}')
    domain_paper = build_main_page("https://devby.io/")
    for article in domain_paper.articles:
        parse_one_article(article.url)
    return 


def parse_one_article(article_url: str):
    parsed_article = NewsPaper(article_url)
    parsed_article.download()
    parsed_article.parse()
    parsed_article.nlp()
    print(f"authors - {parsed_article.authors}")
    print(f"publish_date - {parsed_article.publish_date}")
    print(f"keywords - {parsed_article.keywords}")
    article = Article(title=' ', content=' ', description=' ',
                      image=' ', source_url=article_url, guid=article_url.rsplit('/', 1)[-1])
    article.save()

if __name__ == '__main__':
    parse_domain("https://devby.io/news")