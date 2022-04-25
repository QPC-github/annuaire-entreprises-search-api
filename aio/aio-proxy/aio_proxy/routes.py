import json
import os

import elasticsearch
import sentry_sdk
from aio_proxy.helper import hide_fields, serialize_error_text
from aio_proxy.helper import serialize_error_text
from aio_proxy.parameters import extract_text_parameters, extract_geo_parameters
from aio_proxy.search.index import Siren
from aio_proxy.search.search_functions import search_text, search_geo
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
    sentry_sdk.init(dsn=DSN_SENTRY, integrations=[AioHttpIntegration()])

# Connect to Elasticsearch
connections.create_connection(
    hosts=[ELASTIC_URL],
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    retry_on_timeout=True,
)

routes = web.RouteTableDef()


@routes.get("/search")
async def search_endpoint(request):
    try:
        terms, page, per_page, filters = extract_text_parameters(request)
        total_results, unite_legale = search_text(
            Siren, terms, page * per_page, per_page, **filters
        )
        unite_legale_filtered = hide_fields(unite_legale)
        res = {
            "unite_legale": unite_legale_filtered,
            "total_results": int(total_results),
            "page": page + 1,
            "per_page": per_page,
        }
        res["total_pages"] = int(res["total_results"] / res["per_page"]) + 1
        return web.json_response(text=json.dumps([res], default=str))
    except (elasticsearch.exceptions.RequestError, ValueError, TypeError) as error:
        raise web.HTTPBadRequest(
            text=serialize_error_text(str(error)), content_type="application/json"
        )
    except BaseException as error:
        raise web.HTTPInternalServerError(
            text=serialize_error_text(str(error)), content_type="application/json"
        )


@routes.get("/near_point")
async def near_point_endpoint(request):
    try:
        lat, lon, radius, page, per_page = extract_geo_parameters(request)
        total_results, unite_legale = search_geo(
            Siren, page * per_page, per_page, lat, lon, radius
        )
        unite_legale_filtered = hide_fields(unite_legale)
        res = {
            "unite_legale": unite_legale_filtered,
            "total_results": int(total_results),
            "page": page + 1,
            "per_page": per_page,
        }
        res["total_pages"] = int(res["total_results"] / res["per_page"]) + 1
        return web.json_response(text=json.dumps([res], default=str))
    except (elasticsearch.exceptions.RequestError, ValueError, TypeError) as error:
        raise web.HTTPBadRequest(
            text=serialize_error_text(str(error)), content_type="application/json"
        )
    except BaseException as error:
        raise web.HTTPInternalServerError(
            text=serialize_error_text(str(error)), content_type="application/json"
        )


@routes.get("/colors")
async def color_endpoint(request):
    return web.json_response(
        {
            "CURRENT_COLOR": os.getenv("CURRENT_COLOR"),
            "NEXT_COLOR": os.getenv("NEXT_COLOR"),
        },
        status=200,
    )
