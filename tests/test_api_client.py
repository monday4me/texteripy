import pytest
from texteripy.client import Texterify
from unittest.mock import MagicMock, AsyncMock

# Mock Texterify._make_request
Texterify._make_request = AsyncMock()


@pytest.mark.asyncio
async def test_get_keys():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": [{"id": "1", "name": "key1"}]}
    result = await texterify.get_keys("project_id")
    assert result == {"data": [{"id": "1", "name": "key1"}]}
    texterify._make_request.assert_called_once_with("projects/project_id/keys", "GET", None, False)


@pytest.mark.asyncio
async def test_create_key():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": {"attributes": {"id": "1", "name": "key1"}}}
    result = await texterify.create_key("project_id", "key1", "description")
    assert result == {"data": {"attributes": {"id": "1", "name": "key1"}}}
    texterify._make_request.assert_called_once_with("projects/project_id/keys", "POST", {
        "name": "key1",
        "description": "description"
    }, False)


@pytest.mark.asyncio
async def test_update_key():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": {"attributes": {"id": "1", "name": "key1_updated"}}}
    result = await texterify.update_key("project_id", "1", "key1_updated", "description_updated")
    assert result == {"data": {"attributes": {"id": "1", "name": "key1_updated"}}}
    texterify._make_request.assert_called_once_with("projects/project_id/keys/1", "PUT", {
        "name": "key1_updated",
        "description": "description_updated"
    }, False)


@pytest.mark.asyncio
async def test_delete_keys():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": {"message": "keys deleted"}}
    result = await texterify.delete_keys("project_id", ["1", "2"])
    assert result == {"data": {"message": "keys deleted"}}
    texterify._make_request.assert_called_once_with("projects/project_id/keys", "DELETE", {
        "keys": ["1", "2"]
    }, False)


@pytest.mark.asyncio
async def test_get_projects():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": [{"id": "1", "name": "project1"}]}
    result = await texterify.get_projects()
    assert result == {"data": [{"id": "1", "name": "project1"}]}
    texterify._make_request.assert_called_once_with("projects", "GET", None, False)


@pytest.mark.asyncio
async def test_get_project():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": {"id": "1", "name": "project1"}}
    result = await texterify.get_project("1")
    assert result == {"data": {"id": "1", "name": "project1"}}
    texterify._make_request.assert_called_once_with("projects/1", "GET", None, False)


@pytest.mark.asyncio
async def test_create_project():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": {"id": "1", "name": "project1"}}
    result = await texterify.create_project("project1", "description")
    assert result == {"data": {"id": "1", "name": "project1"}}
    texterify._make_request.assert_called_once_with("projects", "POST", {
        "project": {
            "name": "project1",
            "description": "description"
        }
    }, False)


@pytest.mark.asyncio
async def test_update_project():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": {"id": "1", "name": "project1_updated"}}
    result = await texterify.update_project("project1_updated", "description_updated")
    assert result == {"data": {"id": "1", "name": "project1_updated"}}
    texterify._make_request.assert_called_once_with("projects", "PUT", {
        "project": {
            "name": "project1_updated",
            "description": "description_updated"
        }
    }, False)


@pytest.mark.asyncio
async def test_export_project():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    aiohttp_response = MagicMock()
    aiohttp_response.status = 200
    texterify._make_request.return_value = aiohttp_response
    result = await texterify.export_project("1", "export_config_id", {})
    assert result == aiohttp_response
    texterify._make_request.assert_called_once_with("projects/1/exports/export_config_id", "GET", {}, True)


@pytest.mark.asyncio
async def test_import_project():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": {"message": "file imported"}}
    result = await texterify.import_project("1", "language_id", "tests/export")
    assert result == {"data": {"message": "file imported"}}
    texterify._make_request.assert_called_once_with("projects/1/import", "POST", {
        "language_id": "language_id",
        "file": "ZmlsZSBjb250ZW50"
    }, False)


@pytest.mark.asyncio
async def test_create_translation():
    texterify = Texterify("test@example.com", "test_secret")
    texterify._make_request.reset_mock()
    texterify._make_request.return_value = {"data": {"id": "1", "content": "translation"}}
    result = await texterify.create_translation("project_id", "1", "translation")
    assert result == {"data": {"id": "1", "content": "translation"}}
    texterify._make_request.assert_called_once_with("projects/project_id/translations", "POST", {
        "language_id": None,
        "key_id": "1",
        "translation": {
            "content": "translation"
        }
    }, False)
