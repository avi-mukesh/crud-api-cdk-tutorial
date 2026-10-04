from aws_cdk import (
    Stack, # groups AWS resources together
    RemovalPolicy, # controls what happens when you delete the stack
    CfnOutput, # prints values (like table name) after deployment
    aws_dynamodb as dynamodb # CDK module for DynamoDB
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
        
        # prints the table name after deployment so we can verify it exists
        CfnOutput(
            self,
            "TableName",
            value=items_table.table_name,
            description="DynamoDB table name"
        )
