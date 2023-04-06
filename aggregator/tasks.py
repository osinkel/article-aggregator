from aggregator.logic.main import create_etree, parse_page, parse_rss
from aggregator.models import Domain
import logging
# from celery import shared_task
from article_aggregator.celery import app

logger = logging.getLogger()

# shared_task
@app.task
def parse(domain_name_to_parse: str) -> None:
    print(f"************************** {domain_name_to_parse}")
    domain = Domain.objects.get(name=domain_name_to_parse)
    logger.warning(f'start parsing of {domain_name_to_parse}')
    tree = create_etree(domain.source_url)
    print(domain_name_to_parse, 1)
    properties = domain.parsingpattern_set.all()
    print(domain_name_to_parse, 2)
    proterty_for_main_page = properties.get(is_main=True)
    print(domain_name_to_parse, 3)
    properties = properties.filter(is_main=False)
    print(domain_name_to_parse, 4)
    if domain.is_rss:
        print(domain_name_to_parse, 5)
        parse_rss(tree, proterty_for_main_page, properties, domain)
    else:
        print(domain_name_to_parse, 6)
        parse_page(tree, proterty_for_main_page, properties, domain)
    print(domain_name_to_parse, 7)


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0)

# app.conf.beat_schedule = {
#     "run-me-every-ten-seconds": {
#     "task": "tasks.parse",
#     "schedule": 10.0,
#     }
# }
