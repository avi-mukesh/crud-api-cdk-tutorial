import boto3
import os
import json
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    http_method = event['httpMethod']
    path = event.get('resource', '')
    
    try:
        if http_method == 'GET' and path == '/items':
            return get_all_items()
        elif http_method == 'GET' and path == '/items/{id}':
            item_id = event['pathParameters']['id']
            return get_item(item_id)
        elif http_method == 'POST' and path == '/items':
            body = json.loads(event['body'])
            return create_item(body)
        elif http_method == 'PUT' and path == '/items/{id}':
            item_id = event['pathParameters']['id']
            body = json.loads(event['body'])
            return update_item(item_id, body)
        elif http_method == 'DELETE' and path == '/items/{id}':
            item_id = event['pathParameters']['id']
            return delete_item(item_id)
        return api_response(400, {'error':'Unsupported route'})
    except Exception as e:
        return api_response(500, {'error': str(e)})
            

def get_all_items():
    result = table.scan()
    return api_response(200, result['Items'])

def get_item(item_id):
    result = table.get_item(Key={'id': item_id})
    if "Item" not in result:
        return api_response(404, {'error': f'Item {item_id} not found'})
    return api_response(200, result['Item'])

def create_item(body):
    item = {
        "id": str(uuid.uuid4()),
        "name": body.get("name", ""),
        "description": body.get("description", "")
    }
    table.put_item(Item=item)
    return api_response(201, item)

def update_item(item_id, body):
    result = table.update_item(
        Key={"id": item_id},
        UpdateExpression="SET #n = :n, description = :d",
        ExpressionAttributeNames={"#n": "name"},
        ExpressionAttributeValues={
            ":n": body.get("name", ""),
            ":d": body.get("description", "")
        },
        ReturnValues="ALL_NEW"
    )
    return api_response(200, result['Attributes'])
    
    
def delete_item(item_id):
    table.delete_item(Key={"id": item_id})
    return api_response(200, {"message": f"Deleted {item_id}"})

def api_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body, default=str)
    }