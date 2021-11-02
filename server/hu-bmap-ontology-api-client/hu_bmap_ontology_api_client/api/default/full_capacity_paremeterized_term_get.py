from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.full_capacity_term import FullCapacityTerm
from ...types import UNSET, Response, Unset


def _get_kwargs(
    term: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    semantic: Union[Unset, None, List[str]] = UNSET,
    contains: Union[Unset, None, bool] = False,
    case: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/fullCapacityParameterizedTerm/{term}".format(client.base_url, term=term)

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

    json_semantic: Union[Unset, None, List[str]] = UNSET
    if not isinstance(semantic, Unset):
        if semantic is None:
            json_semantic = None
        else:
            json_semantic = semantic

    params: Dict[str, Any] = {
        "sab": json_sab,
        "tty": json_tty,
        "semantic": json_semantic,
        "contains": contains,
        "case": case,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[FullCapacityTerm]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = FullCapacityTerm.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[FullCapacityTerm]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    term: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    semantic: Union[Unset, None, List[str]] = UNSET,
    contains: Union[Unset, None, bool] = False,
    case: Union[Unset, None, bool] = False,
) -> Response[List[FullCapacityTerm]]:
    kwargs = _get_kwargs(
        term=term,
        client=client,
        sab=sab,
        tty=tty,
        semantic=semantic,
        contains=contains,
        case=case,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    term: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    semantic: Union[Unset, None, List[str]] = UNSET,
    contains: Union[Unset, None, bool] = False,
    case: Union[Unset, None, bool] = False,
) -> Optional[List[FullCapacityTerm]]:
    """ """

    return sync_detailed(
        term=term,
        client=client,
        sab=sab,
        tty=tty,
        semantic=semantic,
        contains=contains,
        case=case,
    ).parsed


async def asyncio_detailed(
    term: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    semantic: Union[Unset, None, List[str]] = UNSET,
    contains: Union[Unset, None, bool] = False,
    case: Union[Unset, None, bool] = False,
) -> Response[List[FullCapacityTerm]]:
    kwargs = _get_kwargs(
        term=term,
        client=client,
        sab=sab,
        tty=tty,
        semantic=semantic,
        contains=contains,
        case=case,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    term: str,
    *,
    client: Client,
    sab: Union[Unset, None, List[str]] = UNSET,
    tty: Union[Unset, None, List[str]] = UNSET,
    semantic: Union[Unset, None, List[str]] = UNSET,
    contains: Union[Unset, None, bool] = False,
    case: Union[Unset, None, bool] = False,
) -> Optional[List[FullCapacityTerm]]:
    """ """

    return (
        await asyncio_detailed(
            term=term,
            client=client,
            sab=sab,
            tty=tty,
            semantic=semantic,
            contains=contains,
            case=case,
        )
    ).parsed
