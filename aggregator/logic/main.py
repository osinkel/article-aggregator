import datetime
import logging
import traceback
from typing import Any
import unicodedata
import dateparser
import requests
from lxml import etree
from datetime import datetime
from aggregator.models import Article, Author, Category, Domain, ParsingPattern, Sensitive
from django.db.models.query import QuerySet
import config
from django.core.paginator import Paginator
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import newspaper


logger = logging.getLogger()

months = {
    'июн': 'jun',
    'июл': 'jul',
    'авг': 'aug',
    'сен': 'sep',
    'окт': 'oct',
    'ноя': 'nov',
    'дек': 'dec',
    'янв': 'jan',
    'фев': 'feb',
    'мар': 'mar',
    'апр': 'apr',
    'мая': 'may',
    'май': 'may',
}


def create_etree(url) -> Any | None:
    try:
        response = requests.get(url, timeout=5)
        content = response.content.decode(response.encoding)
        logger.warning(f'tree for {url} successfully parsed!')
    except:
        logger.info(traceback.format_exc())
        return
    try:
        parser = etree.HTMLParser()
        page_tree = etree.fromstring(content, parser)
    except:
        page_tree = etree.fromstring(bytes(content, encoding='utf-8'))
    return page_tree


def is_image(url: str) -> bool:
    return url.endswith(('jpeg', 'jpg', 'png', 'tiff', 'gif'))


def parse_rss(tree: etree,  proterty_for_num_articles: ParsingPattern, properties: QuerySet[ParsingPattern], domain: Domain) -> None:
    common_pattern = proterty_for_num_articles.pattern
    num_articles = len(tree.xpath(common_pattern))
    count = 0
    for article_num in range(1, num_articles+1):
        is_article_exist = False
        article = Article(title=' ', content=' ', description=' ',
                          image=' ', source_url=' ', guid=' ', domain=domain)
        article.save() # Needs to create relationships. You can't add relationship if object not in database
        try:
            for property in properties:
                if property.is_for_parsing:
                    if property.name.name == 'pub_date':
                        date = tree.xpath(
                            f'{common_pattern}[{article_num}]{property.pattern}')[0]
                        continue
                    elif property.name.name == 'category':
                        categories_name = tree.xpath(
                            f'{common_pattern}[{article_num}]{property.pattern}')
                        for category_name in categories_name:
                            last_order = Category.objects.last()
                            try:
                                category = Category.objects.filter(name=category_name.replace('\r\n', '').strip(), order=1 if last_order is None else last_order.order)[0]
                            except IndexError:
                                category = Category(name=category_name.replace('\r\n', '').strip(), order=1 if last_order is None else last_order.order)
                                category.save()
                            article.category.add(category)
                        continue
                    elif property.name.name == 'author':
                        try:
                            author_name = tree.xpath(f'{common_pattern}[{article_num}]{property.pattern}')[
                                0].replace('\r\n', '').strip()
                            author = Author.objects.get_or_create(
                                name=author_name, domain=domain)
                            article.author = author[0]
                        except Exception as exc:
                            logger.warning(f"article {article_num} haven't author")
                            author_name = config.UNKNOWN_AUTHOR_NAME
                            author = Author.objects.get_or_create(name=author_name, domain=domain)
                            article.author = author[0]
                        continue
                    elif property.name.name == 'guid':
                        source_url = tree.xpath(f'{common_pattern}[{article_num}]{property.pattern}')[
                            0].replace('\r\n', '').strip()
                        try:
                            is_article_exist = Article.objects.get(
                                source_url=source_url)
                            logger.warning(is_article_exist)
                        except Article.DoesNotExist:
                            is_article_exist = False
                        if is_article_exist:
                            logger.warning('Article exists!')
                            article.delete()
                            break
                        logger.warning(f"{domain.name} parsed {count}")
                        count+=1
                        article.guid = source_url.rsplit('/', 1)[-1]
                        article.source_url = source_url
                    else:
                        try:
                            data = unicodedata.normalize('NFKD', tree.xpath(
                                f'{common_pattern}[{article_num}]{property.pattern}')[0].replace('\r\n', '').strip())
                            setattr(article, property.name.name, data)
                        except:
                            tree_element = tree.xpath(
                                f'{common_pattern}[{article_num}]{property.pattern}')
                            print(f"error --- {property.pattern} --- {property.name.name} --- {tree_element} --- {article_num}")
                            data = ''
            else:
                if not is_article_exist:
                    date = dateparser.parse(date)
                    article.date = date
                    article.sensitive = calculate_mood_level(get_content_without_tags(article.source_url), domain.language)
                    article.save()
                elif not article.sensitive:
                    article.sensitive = calculate_mood_level(get_content_without_tags(article.source_url), domain.language)
                    article.save()
        except:
            logger.info(traceback.format_exc())
            continue


def parse_page(tree: etree, proterty_for_main_page: ParsingPattern, properties: QuerySet[ParsingPattern], domain: Domain) -> None:
    articles_url = [url if url.startswith(
        'http') else f'https://{domain.name}{url}' for url in tree.xpath(proterty_for_main_page.pattern)]
    count = 0
    print(f"new to parse - {len(articles_url)}")
    for     article_url in articles_url:
        try:
            is_article_exist = Article.objects.get(source_url=article_url)
        except Article.DoesNotExist:
            is_article_exist = False
        # except:
        #     is_article_exist = True
        if not is_article_exist:
            parse_one_article(properties, domain, article_url)
            logger.warning(f'{domain.name} parsed {count}')
            count += 1
        else:
            is_article_exist.sensitive = calculate_mood_level(get_content_without_tags(is_article_exist.source_url), domain.language)
            is_article_exist.save()
    return


def parse_one_article(parse_properties: QuerySet, domain: Domain, article_url: str = None):
    tree = create_etree(article_url)
    if tree is None:
        logger.info(f"Tree of page {article_url} don't be created")
        return
    article = Article(title=' ', content=' ', description=' ',
                      image=' ', source_url=article_url, guid=article_url.rsplit('/', 1)[-1], domain=domain)
    article.save()
    for property in parse_properties:
        if property.is_for_parsing:
            if property.name.name == 'content':
                content = parse_article_content(
                    tree, property.pattern, domain)
                article.content = content
                continue
            if property.name.name == 'category':
                categories_name = tree.xpath(property.pattern)
                for category_name in categories_name:
                    last_order = Category.objects.last()
                    try:
                        category = Category.objects.filter(name=category_name, order=1 if last_order is None else last_order.order)[0]
                    except IndexError:
                        category = Category(name=category_name, order=1 if last_order is None else last_order.order)
                        category.save()
                    article.category.add(category)
                continue
            if property.name.name == 'author':
                author_name = tree.xpath(property.pattern)[0]
                author = Author.objects.get_or_create(
                    name=author_name, domain=domain)
                article.author = author[0]
                continue
            if property.name.name == 'pub_date':
                date = tree.xpath(property.pattern)[0]
                continue
            data = unicodedata.normalize('NFKD', tree.xpath(
                property.pattern)[0].replace('\r\n', '').strip())
            setattr(article, property.name.name, data)
            
    date = dateparser.parse(date)
    article.date = date
    article.sensitive = calculate_mood_level(get_content_without_tags(article.source_url), domain.language)
    article.save()


def parse_article_content(tree: etree, xpath_str: str, domain: Domain, data_attrs: list[str] = ['//text()', '//@href', '//@src']) -> str:
    content = []
    x = 0
    child_num = len(tree.xpath(xpath_str))
    for x in range(child_num):
        xpath_str_i = f'{xpath_str}[{x+1}]'
        text = tree.xpath(' | '.join(
            xpath_str_i + attr for attr in data_attrs))
        content.append(parse_one_paragraph(text, domain))
        x += 1
    return unicodedata.normalize('NFKD', ''.join(content).replace('\r\n', ''))


def parse_one_paragraph(text: str, domain: Domain) -> str:
    result = ''
    for i, item in enumerate(text):
        if not i:
            result = '<p>'
        if not text[i-1].startswith('http') and not item.startswith('http') and not item.startswith('/tags') and not is_image(item):
            result += item
            continue
        if is_image(text[i-1]):
            if not item.startswith('http'):
                item = f'{domain.name}{item}'
            item = f'<figure><img src="{text[i-1]}"/><figcaption></figcaption></figure>'
            result += item
        elif text[i-1].startswith('http'):
            item = f'<a href="{text[i-1]}">{item}</a>'
            result += item
    result += '</p>'
    return result


def do_date_format(date: str, input_format: str, is_english=False) -> datetime:
    # if is_english:
        # date = ' '.join(item[:3] if item.isalpha() and len(
            # item) != 1 else item for item in date.split())
    # else:
        # try:
            # date = ' '.join(months[item[:3]] if item.isalpha() and len(item) != 1 else item for item in date.split())
        # except KeyError as exc:
            # logger.warning(f'Bad domain language - {exc}')
            # date = ' '.join(item[:3] if item.isalpha() and len(item) != 1 else item for item in date.split())
    # date = ' '.join(item[:3] if item.isalpha() and len(item) != 1 else item for item in date.split())
    date = datetime.strptime(date, input_format)
    return date


def get_articles_from_search(request, context):
    if request.htmx:
        search = request.GET.get('q')
        page_num = request.GET.get('page', 1)
        if search:
            articles = Article.objects.filter(title__icontains=search)
        else:
            articles = Article.objects.none()
        page = Paginator(object_list=articles, per_page=5).get_page(page_num)
        context['page'] = page
    return context


def calculate_mood_level(text: str, lang: str):
    translator = Translator()
    if not 'en' in lang:
        text = translator.translate(text, dest='en').text
        
    sentiment = SentimentIntensityAnalyzer()
    return sentiment.polarity_scores(text)['compound']

def get_content_without_tags(url: str):
    article = newspaper.Article(url)
    article.download()
    try:
        article.parse()
    except:
        logger.info(f"Newspaper can't extract text from {url}")
    return article.text.replace('\n', ' ')


def set_sensitive_level_colors(articles: list[Article]):
    sensitives = Sensitive.objects.all()
    for article in articles:
        for sens in sensitives:
            if sens.min<=article.sensitive<=sens.max:
                article.color = sens.color
                break
    return articles
    