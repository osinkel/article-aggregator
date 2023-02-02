from aggregator.logic import create_etree, parse_page, parse_rss
from aggregator.models import Domain
import logging
# from celery import shared_task
from article_aggregator.celery import app

logger = logging.getLogger()

# shared_task
@app.task
def parse(domain_name_to_parse: str = 'devby.io') -> None:
    domain = Domain.objects.get(name=domain_name_to_parse)
    logger.warning(f'start parsing of {domain_name_to_parse}')
    tree = create_etree(domain.source_url)
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
