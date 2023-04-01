import aiohttp
import json
import urllib.parse
from typing import Any, Dict, Optional
import logging
import base64

logger = logging.getLogger(__name__)


class Texterify:
    """
    Texterify is an asynchronous API client for interacting with the Texterify localization platform.
    The class provides methods to manage projects, keys, and translations using the Texterify API.

    Usage:
        texterify = Texterify(auth_email="your_email", auth_secret="your_secret")
    """

    def __init__(self, auth_email: str, auth_secret: str):
        """
        Initialize the Texterify API client with the provided authentication credentials.

        :param auth_email: The email address used for authenticating with the Texterify API.
        :param auth_secret: The secret used for authenticating with the Texterify API.
        """
        self.auth_email = auth_email
        self.auth_secret = auth_secret

        self.request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        api_base_url = 'https://app.texterify.com/api'
        self.api_version = 'v1'

        self.api_base_url = f"{api_base_url}/{self.api_version}/"

        self.request_headers["Auth-Email"] = self.auth_email
        self.request_headers["Auth-Secret"] = self.auth_secret

    async def _make_request(self, url: str, method: str, params: Optional[Dict[str, Any]],
                            is_file_download: Optional[bool]) -> Any:
        """
        Make an HTTP request to the Texterify API.

        :param url: The endpoint URL of the request.
        :param method: The HTTP method of the request.
        :param params: The query parameters or payload for the request.
        :param is_file_download: Whether the request is for a file download.
        :return: The response data or the response object in case of a file download.
        """
        full_url = f"{self.api_base_url}{url}"
        try:
            if method == "GET" and params:
                params = [(k, str(v).lower() if isinstance(v, bool) else v) for k, v in params.items()]
                full_url += f"?{urllib.parse.urlencode(params)}"

            options = {
                "headers": self.request_headers
            }

            if method != "GET":
                options["data"] = json.dumps(params)
            else:
                options["params"] = params

            async with aiohttp.ClientSession() as session:
                async with session.request(method, full_url, **options) as response:
                    if response.status != 200 and response.status != 400:
                        if response.status == 404:
                            logger.error("The resource could not be found. Maybe your auth credentials are wrong or you"
                                         " don't have the permission to access this resource.")
                        else:
                            logger.error(f"Invalid response status received: {response.status}")
                        raise Exception(f"Invalid response status received: {response.status}\n")
                    return await response.json() if not is_file_download else response

        except Exception as error:
            logger.error("Error:", error)
            raise error

    async def _get_request(self, url: str, query_params: Optional[Dict[str, Any]] = None,
                           is_file_download: Optional[bool] = False) -> Any:
        """
        Make a GET request to the Texterify API.

        :param url: The endpoint URL of the request.
        :param query_params: The query parameters for the request.
        :param is_file_download: Whether the request is for a file download.
        :return: The response data or the response object in case of a file download.
        """
        return await self._make_request(url, "GET", query_params, is_file_download)

    async def _post_request(self, url: str, body: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a POST request to the Texterify API.

        :param url: The endpoint URL of the request.
        :param body: The payload for the request.
        :return: The response data.
        """
        return await self._make_request(url, "POST", body, False)

    async def _put_request(self, url: str, body: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a PUT request to the Texterify API.

        :param url: The endpoint URL of the request.
        :param body: The payload for the request.
        :return: The response data.
        """
        return await self._make_request(url, "PUT", body, False)

    async def _delete_request(self, url: str, body: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a DELETE request to the Texterify API.

        :param url: The endpoint URL of the request.
        :param body: The payload for the request.
        :return: The response data.
        """
        return await self._make_request(url, "DELETE", body, False)

    async def get_keys(self, project_id: str, page: int = 1, per_page: int = 10, case_sensitive: bool = False,
        only_html_enabled: bool = False, only_untranslated: bool = False, only_with_overwrites: bool = False
    ) -> Any:
        """
        Retrieve keys for a given project.

        :param project_id: The ID of the project.
        :return: A list of keys for the project.
        """
        return await self._get_request(f"projects/{project_id}/keys", {
            "page": page,
            "per_page": per_page,
            "case_sensitive": case_sensitive,
            "only_html_enabled": only_html_enabled,
            "only_untranslated": only_untranslated,
            "only_with_overwrites": only_with_overwrites,
        })

    async def create_key(self, project_id: str, name: str, description: str,
                         default_language_translation: Optional[str] = None) -> Any:
        """
        Create a new key for a given project.

        :param project_id: The ID of the project.
        :param name: The name of the new key.
        :param description: The description of the new key.
        :param default_language_translation: The optional default language translation for the new key.
        :return: The created key.
        """
        new_key = await self._post_request(f"projects/{project_id}/keys", {
            "name": name,
            "description": description
        })

        if not new_key.get("error") and new_key.get("data") and default_language_translation:
            new_translation_response = await self.create_translation(
                project_id=project_id,
                key_id=new_key["data"]["attributes"]["id"],
                content=default_language_translation
            )

            if new_translation_response.get("error") == "NO_DEFAULT_LANGUAGE_SPECIFIED":
                logger.error("You need to define a default language if you want to add translations for"
                             " your default language directly when creating a new key.")

        return new_key

    async def update_key(self, project_id: str, key_id: str, name: str, description: str) -> Any:
        """
        Update an existing key for a given project.

        :param project_id: The ID of the project.
        :param key_id: The ID of the key.
        :param name: The new name for the key.
        :param description: The new description for the key.
        :return: The updated key.
        """
        return await self._put_request(f"projects/{project_id}/keys/{key_id}", {
            "name": name,
            "description": description
        })

    async def delete_keys(self, project_id: str, keys: Any) -> Any:
        """
        Delete keys for a given project.

        :param project_id: The ID of the project.
        :param keys: A list of key IDs to delete.
        :return: The response data.
        """
        return await self._delete_request(f"projects/{project_id}/keys", {
            "keys": keys
        })

    async def get_projects(self) -> Any:
        """
        Retrieve a list of projects.

        :return: A list of projects.
        """
        return await self._get_request("projects")

    async def get_project(self, project_id: str) -> Any:
        """
        Retrieve the details of a specific project.

        :param project_id: The ID of the project.
        :return: The project details.
        """
        return await self._get_request(f"projects/{project_id}")

    async def create_project(self, name: str, description: str) -> Any:
        """
        Create a new project.

        :param name: The name of the new project.
        :param description: The description of the new project.
        :return: The created project.
        """
        return await self._post_request("projects", {
            "project": {
                "name": name,
                "description": description
            }
        })

    async def update_project(self, name: str, description: str) -> Any:
        """
        Update an existing project.

        :param name: The new name for the project.
        :param description: The new description for the project.
        :return: The updated project.
        """
        return await self._put_request("projects", {
            "project": {
                "name": name,
                "description": description
            }
        })

    async def export_project(self, project_id: str, export_config_id: str, options: Dict[str, Any]) -> Any:
        """
        Export a project with the specified export configuration.

        :param project_id: The ID of the project.
        :param export_config_id: The ID of the export configuration.
        :param options: Additional export options.
        :return: The exported project.
        """
        return await self._get_request(f"projects/{project_id}/exports/{export_config_id}", options, True)

    async def import_project(self, project_id: str, language_id: str, file_path: str) -> Any:
        """
        Import a file into a project for a specific language.

        :param project_id: The ID of the project.
        :param language_id: The ID of the language.
        :param file_path: Path to the file to be imported.
        :return: The response data.
        """
        with open(file_path, "rb") as file:
            file_bytes = file.read()

        file_base64 = base64.b64encode(file_bytes).decode()

        return await self._post_request(f"projects/{project_id}/import", {
            "language_id": language_id,
            "file": file_base64
        })

    async def create_translation(self, project_id: str, key_id: str, content: str,
                                 language_id: Optional[str] = None) -> Any:
        """
        Create a new translation for a given project and key.

        :param project_id: The ID of the project.
        :param key_id: The ID of the key.
        :param content: The content of the translation.
        :param language_id: The optional language ID for the translation.
        :return: The created translation.
        """
        return await self._post_request(f"projects/{project_id}/translations", {
            "language_id": language_id,
            "key_id": key_id,
            "translation": {
                "content": content
            }
        })

    async def get_languages(self, project_id: str, page: int = 1, per_page: int = 10, search: str | Any = None) -> Any:
        return await self._get_request(f"projects/{project_id}/languages", {
            "page": page,
            "per_page": per_page,
            "search": search if search else ""
        })
