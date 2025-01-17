from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.term_resp_obj import TermRespObj
from ...types import UNSET, Response, Unset


def _get_kwargs(
    concept_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    rel: Union[Unset, None, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/concepts/{concept_id}/terms".format(client.base_url, concept_id=concept_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_sab: Union[Unset, None, List[str]] = UNSET
    if not isinstance(sab, Unset):
        if sab is None:
            json_sab = None
        else:
            json_sab = sab

    json_tty: Union[Unset, None, List[str]] = UNSET
    if not isinstance(tty, Unset):
        if tty is None:
            json_tty = None
        else:
            json_tty = tty

    json_rel: Union[Unset, None, List[str]] = UNSET
    if not isinstance(rel, Unset):
        if rel is None:
            json_rel = None
        else:
            json_rel = rel

    params: Dict[str, Any] = {
        "sab": json_sab,
        "tty": json_tty,
        "rel": json_rel,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[TermRespObj]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TermRespObj.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[TermRespObj]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    concept_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    rel: Union[Unset, None, List[str]] = UNSET,
) -> Response[List[TermRespObj]]:
    kwargs = _get_kwargs(
        concept_id=concept_id,
        client=client,
        sab=sab,
        tty=tty,
        rel=rel,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    concept_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    rel: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List[TermRespObj]]:
    """ """

    return sync_detailed(
        concept_id=concept_id,
        client=client,
        sab=sab,
        tty=tty,
        rel=rel,
    ).parsed


async def asyncio_detailed(
    concept_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    rel: Union[Unset, None, List[str]] = UNSET,
) -> Response[List[TermRespObj]]:
    kwargs = _get_kwargs(
        concept_id=concept_id,
        client=client,
        sab=sab,
        tty=tty,
        rel=rel,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    concept_id: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    rel: Union[Unset, None, List[str]] = UNSET,
) -> Optional[List[TermRespObj]]:
    """ """

    return (
        await asyncio_detailed(
            concept_id=concept_id,
            client=client,
            sab=sab,
            tty=tty,
            rel=rel,
        )
    ).parsed
