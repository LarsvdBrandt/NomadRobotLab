#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from fastapi import Depends, APIRouter, Body, HTTPException

from nomad.graph.graph_reader import (
    MongoReader,
    ConfigError,
    GeneralReader,
    UserReader,
    Token,
)
from .auth import create_user_dependency
from .entries import EntriesArchive
from ..models import User
from nomad.app.v1.models.graph import GraphRequest, GraphResponse

router = APIRouter()
default_tag = 'graph'


def normalise_response(response):
    if GeneralReader.__CACHE__ in response:
        del response[GeneralReader.__CACHE__]

    return reorder_children(response)


def relocate_children(request):
    if not isinstance(request, dict) or not request:
        return
    request.update(request.pop('m_children', {}))
    for child in request.values():
        relocate_children(child)


def reorder_children(query):
    if not isinstance(query, dict):
        return query
    return {
        k: reorder_children(v)
        for k, v in sorted(query.items(), key=lambda item: item[0])
    }


@router.post(
    '/raw_query',
    tags=[default_tag],
    summary='Query the database with a graph style without verification.',
    description='Query the database with a graph style without verification.',
)
async def raw_query(
    query=Body(...), user: User = Depends(create_user_dependency(required=True))
):
    relocate_children(query)
    with MongoReader(query, user=user) as reader:
        return normalise_response(reader.read())


@router.post(
    '/query',
    tags=[default_tag],
    summary='Query the database with a graph style.',
    description='Query the database with a graph style.',
    response_model=GraphResponse,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def basic_query(
    query: GraphRequest = Body(...),
    user: User = Depends(create_user_dependency(required=True)),
):
    try:
        query_dict = query.dict(
            exclude_none=True, exclude_unset=True, exclude_defaults=True
        )
        relocate_children(query_dict)
        with MongoReader(query_dict, user=user) as reader:
            response: dict = reader.read()
    except ConfigError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(422, detail=str(e))

    return normalise_response(response)


@router.post(
    '/archive/query',
    tags=[default_tag],
    summary='Search entries and access their archives',
)
async def archive_query(
    data: EntriesArchive, user: User = Depends(create_user_dependency())
):
    graph_dict: dict = {Token.SEARCH: {'m_request': {'query': {}}}}
    root_request: dict = graph_dict[Token.SEARCH]['m_request']['query']

    if data.pagination:
        root_request['pagination'] = data.pagination
    if data.query:
        root_request['query'] = data.query
    if data.owner:
        root_request['owner'] = data.owner

    if data.required is None:
        graph_dict[Token.SEARCH]['m_request']['directive'] = 'plain'
    else:
        graph_dict[Token.SEARCH]['*'] = {Token.ENTRIES: {Token.ARCHIVE: data.required}}

    if not root_request:
        del graph_dict[Token.SEARCH]['m_request']['query']

    with UserReader(graph_dict, user=user) as reader:
        response: dict = reader.read(user.user_id)

    return normalise_response(response)
