from aws_cdk import (
    Stack, # groups AWS resources together
    RemovalPolicy, # controls what happens when you delete the stack
    CfnOutput, # prints values (like table name) after deployment
    Duration,  # for setting timeouts for how long the lambda runs for
    aws_dynamodb as dynamodb, # CDK module for DynamoDB
    aws_lambda as _lambda
)
from constructs import Construct

class CrudApiStack(Stack):
    """This stack defines all the AWS resources for our CRUD API."""
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines the stack
 
        items_table = dynamodb.Table(
            self,
            "ItemsTable",
            partition_key=dynamodb.Attribute( # single field primary key
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST, # better for learning
            removal_policy=RemovalPolicy.DESTROY # delete the table when we destroy the stack (default is to keep it alive)
        )
        
        api_handler = _lambda.Function(
            self,
            "ApiHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,  # Python version to use
            handler="index.handler",   # <fileName>.<functionName>
            code=_lambda.Code.from_asset("lambda"),  # zips the lambda/ folder and uploads it
            architecture=_lambda.Architecture.ARM_64, # Graviton - cheaper and faster
            environment={
                "TABLE_NAME": items_table.table_name
            },
            timeout=Duration.seconds(10),  # default is 3s which is too short
            memory_size=128
        )
        
        # prints the table name after deployment so we can verify it exists
        CfnOutput(
            self,
            "TableName",
            value=items_table.table_name,
            description="DynamoDB table name"
        )
