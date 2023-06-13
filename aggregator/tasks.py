from aggregator.logic.main import create_etree, parse_page, parse_rss
from aggregator.models import Domain
import logging
from article_aggregator.celery import app

logger = logging.getLogger()

# shared_task

@app.task()
def aggregate_articles() -> None:
    domains = Domain.objects.all()
    logger.warning(f"Domains to parse: {domains}")
    for domain in domains:
        parse_article_source(domain.name)


def parse_article_source(domain_name_to_parse: str) -> None:
    domain = Domain.objects.get(name=domain_name_to_parse)
    logger.warning(f'start parsing of {domain_name_to_parse}')
    tree = create_etree(domain.source_url)
    if tree is None:
        return
    properties = domain.parsingpattern_set.all()
    proterty_for_main_page = properties.get(is_main=True)
    properties = properties.filter(is_main=False)
    if domain.is_rss:
        parse_rss(tree, proterty_for_main_page, properties, domain)
    else:
        parse_page(tree, proterty_for_main_page, properties, domain)


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0)

# app.conf.beat_schedule = {
#     "run-me-every-ten-seconds": {
#     "task": "tasks.parse",
#     "schedule": 10.0,
#     }
# }
