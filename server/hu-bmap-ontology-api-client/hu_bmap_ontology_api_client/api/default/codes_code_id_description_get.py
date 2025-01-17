from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.sab_code_term import SabCodeTerm
from ...types import Response


def _get_kwargs(
    code_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/codes/{code_id}/description".format(client.base_url, code_id=code_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[SabCodeTerm]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SabCodeTerm.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[SabCodeTerm]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    code_id: str,
    *,
    client: Client,
) -> Response[List[SabCodeTerm]]:
    kwargs = _get_kwargs(
        code_id=code_id,
        client=client,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    code_id: str,
    *,
    client: Client,
) -> Optional[List[SabCodeTerm]]:
    """ """

    return sync_detailed(
        code_id=code_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    code_id: str,
    *,
    client: Client,
) -> Response[List[SabCodeTerm]]:
    kwargs = _get_kwargs(
        code_id=code_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    code_id: str,
    *,
    client: Client,
) -> Optional[List[SabCodeTerm]]:
    """ """

    return (
        await asyncio_detailed(
            code_id=code_id,
            client=client,
        )
    ).parsed
