import json
import os

import boto3
from botocore.exceptions import ClientError
from .exceptions import (
    AwsSdkPrerequisiteError,
    SecretStringNotFound,
    ResourceNotFoundException,
)


class SecretsManagerService:
    """Service to work with AWS SDK for Secrets Manager entries

    https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html#envvars-list

    """

    aws_region_env_var = "AWS_DEFAULT_REGION"
    aws_access_key_id_var = "AWS_ACCESS_KEY_ID"
    aws_secret_access_key_var = "AWS_SECRET_ACCESS_KEY"
    aws_service_name = "secretsmanager"

    def __init__(self, region=None, access_key_id=None, secret_access_key=None):
        self.region = None
        self.access_key_id = None
        self.secret_access_key = None
        self.session = None
        self.client = None
        self._set_request_values(region, access_key_id, secret_access_key)
        self.get_session()
        self.get_client()

    def get_secrets(self, secret_name: str) -> dict:
        """Get deserialized SecretSting from AWS Secrets Manager for the given secret_name.

        :param secret_name: The SecretId for the entry in Secrets Manager
        :returns dict loaded from SecretString json
        """
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )

        except ClientError as e:
            if e.response["Error"]["Code"] == "DecryptionFailureException":
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InternalServiceErrorException":
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "ResourceNotFoundException":
                raise ResourceNotFoundException(
                    exception=e, secret_name=secret_name, region=self.region
                )

        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
            else:
                raise SecretStringNotFound(secret_name)

            return json.loads(secret)

    def _set_request_values(self, region, access_key_id, secret_access_key):
        self.region = (
            region if region is not None else os.getenv(self.aws_region_env_var)
        )
        self.access_key_id = (
            access_key_id
            if access_key_id is not None
            else os.getenv(self.aws_access_key_id_var)
        )
        self.secret_access_key = (
            secret_access_key
            if secret_access_key is not None
            else os.getenv(self.aws_secret_access_key_var)
        )

        if self.region is None:
            raise AwsSdkPrerequisiteError("AWS region not found.")
        if self.access_key_id is None:
            raise AwsSdkPrerequisiteError("AWS access key id not found.")
        if self.secret_access_key is None:
            raise AwsSdkPrerequisiteError("AWS secret access key not found.")

    def get_session(self):
        if self.session is None:
            self.session = boto3.session.Session()

    def get_client(self):
        if self.client is None:
            self.client = self.session.client(
                service_name=self.aws_service_name, region_name=self.region
            )
