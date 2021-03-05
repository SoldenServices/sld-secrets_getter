# SLD Secrets Getter


Very thin wrapper for the AWS Secrets Manager library for getting secrets in a standard way.

* Free software: MIT license

## Usage

### Pre-requisites

* AWS credentials
  * This package assumes the [AWS cli environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)
    have been configured for authentication.
    Alternatively, you can provide the values for those variables to the constructor.

### Example

Install the package:

```shell
pip install sld.secrets-getter
```

Running with AWS cli environment variables set:

```python
from secrets_getter import SecretsManagerService

secrets_service = SecretsManagerService()
secrets = secrets_service.get_secrets("NAME_OF_AWS_SECRETS_MANAGER_SECRETS_SET")
```

A `dict` with the key value pairs from the Secrets set is returned.

Providing the AWS cli credentials to the constructor:

```python
from secrets_getter import SecretsManagerService

region = "us-west-2"
key_id = "AWS_ACCESS_KEY_ID"
secret_access_key = "SECRET_ACCESS_KEY"

secrets_service = SecretsManagerService(region=region, access_key_id=key_id, secret_access_key=secret_access_key)
secrets = secrets_service.get_secrets("NAME_OF_AWS_SECRETS_MANAGER_SECRETS_SET")
```


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
