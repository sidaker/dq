import json
import os

import boto3
from aws_lambda_powertools import Logger
from botocore.config import Config


logger = Logger()


class StepFunc:
    """Helper class for StepFunction methods"""

    def __init__(self, profile=None):
        """__init__"""
        if profile:
            self.session = boto3.Session(profile_name=profile)
        else:
            self.session = boto3.session.Session()

        self._region = os.environ.get("AWS_REGION")
        config = Config(retries={"max_attempts": 10, "mode": "standard"})
        self._sf = self.session.client(
            service_name="stepfunctions",
            region_name=self._region,
            config=config,
        )

    def start_execution(self, sf_arn: str, payload: dict, name: str = None) -> str:
        """Get Step Function execution async"""
        try:
            logger.info(f"Invoking Step Function: {sf_arn}")
            args = {"name": name} if name else {}
            resp = self._sf.start_execution(
                stateMachineArn=sf_arn,
                input=json.dumps(payload),
                **args,
            )
            logger.info(f'Exeuction ARN is: {resp["executionArn"]}')
            return resp["executionArn"]
        except self._sf.exceptions.InvalidArn:
            raise ValueError(f"Invalid ARN for Step Function: {sf_arn}")
        except self._sf.exceptions.StateMachineDoesNotExist:
            raise ValueError(f"Did not find Step Function ARN: {sf_arn}")
        except Exception as err:
            logger.error(err)
            raise
