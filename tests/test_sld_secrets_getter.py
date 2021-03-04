"""Tests for `secrets_getter` package."""

import pytest
from botocore.stub import Stubber

from secrets_getter import SecretsManagerService
from secrets_getter.exceptions import (
    AwsSdkPrerequisiteError,
    SecretStringNotFound,
    ResourceNotFoundException,
)


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv(SecretsManagerService.aws_region_env_var, "us-none-1")
    monkeypatch.setenv(SecretsManagerService.aws_access_key_id_var, "123abc")
    monkeypatch.setenv(SecretsManagerService.aws_secret_access_key_var, "blah")


def test_get_secrets(monkeypatch, mock_env_vars):
    def mock_secrets_response(_):
        return {"blah": "blah"}

    secrets_manager_service = SecretsManagerService()
    monkeypatch.setattr(secrets_manager_service, "get_secrets", mock_secrets_response)
    mock_response = secrets_manager_service.get_secrets("something")
    assert mock_response.get("blah") == "blah"


def test_get_secrets_loads_dict_from_json_response(mock_env_vars, monkeypatch):
    def mock_get_secret_value_request(SecretId):
        response = {"SecretString": '{"key_1": "value_1", "key_2": "value_2"}'}
        return response

    secrets_manager_service = SecretsManagerService()
    monkeypatch.setattr(
        secrets_manager_service.client,
        "get_secret_value",
        mock_get_secret_value_request,
    )
    mock_response = secrets_manager_service.get_secrets("something")
    assert mock_response.get("key_1") == "value_1"


def test_get_secrets_raises_exception_when_secret_string_not_found(mock_env_vars):
    secrets_manager_service = SecretsManagerService()
    stubber = Stubber(secrets_manager_service.client)
    stubber.add_client_error(
        method="get_secret_value", service_error_code="ResourceNotFoundException"
    )
    stubber.activate()

    with pytest.raises(ResourceNotFoundException):
        _ = secrets_manager_service.get_secrets("missing_secret")


def test_get_secrets_raises_exception_for_resource_not_found(monkeypatch, mock_env_vars):
    def mock_get_secret_value_request(SecretId):
        response = {
            "MayNotMakeSense": '{"only_if_secret_name_exists": "but_secret_string_is_empty"}'
        }
        return response

    secrets_manager_service = SecretsManagerService()
    monkeypatch.setattr(
        secrets_manager_service.client,
        "get_secret_value",
        mock_get_secret_value_request,
    )
    with pytest.raises(SecretStringNotFound):
        _ = secrets_manager_service.get_secrets("empty_secrets")


def test_secrets_manager_service_constructor_with_env_vars(monkeypatch):
    secret_access_key = "blah"
    access_key_id = "123abc"
    region = "us-none-1"
    monkeypatch.setenv(SecretsManagerService.aws_region_env_var, region)
    monkeypatch.setenv(SecretsManagerService.aws_access_key_id_var, access_key_id)
    monkeypatch.setenv(SecretsManagerService.aws_secret_access_key_var, secret_access_key)
    secrets_manager_service = SecretsManagerService()
    assert secrets_manager_service.region == "us-none-1"
    assert secrets_manager_service.secret_access_key == secret_access_key
    assert secrets_manager_service.access_key_id == access_key_id


def test_secrets_manager_service_constructor_given_aws_vars(monkeypatch):
    secret_access_key = "blah"
    access_key_id = "123abc"
    region = "us-none-1"
    secrets_manager_service = SecretsManagerService(
        region=region, access_key_id=access_key_id, secret_access_key=secret_access_key
    )
    assert secrets_manager_service.region == "us-none-1"
    assert secrets_manager_service.secret_access_key == secret_access_key
    assert secrets_manager_service.access_key_id == access_key_id


def test_secrets_manager_service_raises_exception_when_missing_aws_prerequisite(monkeypatch, ):
    monkeypatch.delenv(SecretsManagerService.aws_region_env_var, raising=False)
    monkeypatch.delenv(SecretsManagerService.aws_access_key_id_var, raising=False)
    monkeypatch.delenv(SecretsManagerService.aws_secret_access_key_var, raising=False)
    with pytest.raises(AwsSdkPrerequisiteError):
        _ = SecretsManagerService()


def test_secrets_manager_service_constructor_session_not_none(mock_env_vars):
    secrets_manager_service = SecretsManagerService()
    assert secrets_manager_service.session is not None


def test_secrets_manager_service_constructor_client_not_none(mock_env_vars):
    secrets_manager_service = SecretsManagerService()
    assert secrets_manager_service.client is not None
