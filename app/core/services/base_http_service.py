from typing import Any, Dict, Optional

import aiohttp


class BaseHTTPClient:
    """
    Base class for API clients. Handles making requests to external REST APIs.
    Inherit from this class when creating a client for an API.
    """

    @staticmethod
    async def __request(
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        proxy: Optional[str] = None,
    ) -> str | Any:
        # Determine if we should send as JSON or form data
        content_type = headers.get("Content-Type", "") if headers else ""
        if "application/x-www-form-urlencoded" in content_type:
            request_kwargs = {
                "method": method.upper(),
                "url": url,
                "headers": headers,
                "cookies": cookies,
                "data": data,
                "params": params,
                "proxy": proxy
            }
        else:
            request_kwargs = {
                "method": method.upper(),
                "url": url,
                "headers": headers,
                "cookies": cookies,
                "json": data,
                "params": params,
                "proxy": proxy
            }
        async with aiohttp.ClientSession() as session:
            async with session.request(**request_kwargs) as response:
                response.raise_for_status()
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return await response.json()
                return await response.text()



    async def get(
        self,
        endpoint,
        cookies: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        raise_errors=False,
    ) -> Optional[Dict[str, Any]]:
        """
        Make an asynchronous GET request to an external API.

        Parameters:
            endpoint: The endpoint to send the request to.
            headers: The headers of the request.
            params: The query parameters of the request.
            raise_errors: Whether to raise errors or to silence them and return None.

        Returns:
            The response of the request.
        """
        return await self.__request(
            "GET",
            endpoint,
            headers=headers,
            cookies=cookies,
            params=params,
        )

    async def post(
        self,
        endpoint,
        data: Dict[str, Any],
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Make an asynchronous POST request to an external API.

        Parameters:
            endpoint: The endpoint to send the request to.
            data: The data of the request.
            headers: The headers of the request.
            params: The query parameters of the request.

        Returns:
            The response of the request.
        """
        return await self.__request(
            "POST",
            endpoint,
            data=data,
            cookies=cookies,
            headers=headers,
            params=params,
        )

    async def delete(
        self,
        endpoint: str,
        body: Dict[str, Any],
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        raise_errors=False
    ) -> Optional[Dict[str, Any]]:
        """
        Make an asynchronous DELETE request to an external API.

        Parameters:
            endpoint: The endpoint to send the request to.
            body: The body of the request.
            headers: The headers of the request.
            params: The query parameters of the request.
            raise_errors: Whether to raise errors or to silence them and return None.

        Returns:
            The response of the request.
        """
        return await self.__request(
            "DELETE",
            endpoint,
            data=body,
            headers=headers,
            params=params,
        )

    async def put(
        self,
        endpoint,
        body: Dict[str, Any],
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        raise_errors=False,
    ) -> Optional[Dict[str, Any]]:
        """
        Make an asynchronous PUT request to an external API.

        Parameters:
            endpoint: The endpoint to send the request to.
            body: The body of the request.
            headers: The headers of the request.
            params: The query parameters of the request.
            raise_errors: Whether to raise errors or to silence them and return None.

        Returns:
            The response of the request.
        """
        return await self.__request(
            "PUT",
            endpoint,
            data=body,
            headers=headers,
            params=params,
        )