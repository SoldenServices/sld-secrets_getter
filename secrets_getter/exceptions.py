class AwsSdkPrerequisiteError(Exception):
    _template = (
        "A setting required for working with the AWS API was not found. \n"
        "The region, access key ID, and secret access key are all required to call the AWS CLI. \n"
        "{msg}"
    )

    def __init__(self, msg):
        message = self._template.format(msg=msg)
        super().__init__(message)


class SecretStringNotFound(Exception):
    _template = "The SecretString was not found in the response from AWS for secret name '{secret_name}'"

    def __init__(self, secret_name):
        message = self._template.format(secret_name=secret_name)
        super().__init__(message)


class ResourceNotFoundException(Exception):
    _template = "{exception} could not find a secrets manager entry for {secret_name} in {region}."

    def __init__(self, exception, secret_name, region):
        message = self._template.format(
            exception=exception, secret_name=secret_name, region=region
        )
        super().__init__(message)
