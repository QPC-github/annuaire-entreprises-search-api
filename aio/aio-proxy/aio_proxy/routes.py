import os

import sentry_sdk
from aio_proxy.response.build_response import api_response
from aio_proxy.search.geo_search import geo_search
from aio_proxy.search.parameters import extract_geo_parameters, extract_text_parameters
from aio_proxy.search.text_search import text_search
from aiohttp import web
from dotenv import load_dotenv
from elasticsearch_dsl import connections
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

load_dotenv()

# Get env variables
ENV = os.getenv("ENV")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_URL = os.getenv("ELASTIC_URL")
DSN_SENTRY = os.getenv("DSN_SENTRY")

# Connect to Sentry in production
if ENV == "prod":
    sentry_sdk.init(
        dsn=DSN_SENTRY,
        integrations=[AioHttpIntegration(transaction_style="method_and_path_pattern")],
        # Log 10% of transactions for performance monitoring
        traces_sample_rate=0.1,
    )

# Connect to Elasticsearch
connections.create_connection(
    hosts=[ELASTIC_URL],
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    retry_on_timeout=True,
)

routes = web.RouteTableDef()


@routes.get("/search")
async def search_text_endpoint(request):
    return api_response(
        request, extract_function=extract_text_parameters, search_function=text_search
    )


@routes.get("/near_point")
async def near_point_endpoint(request):
    return api_response(
        request, extract_function=extract_geo_parameters, search_function=geo_search
    )
