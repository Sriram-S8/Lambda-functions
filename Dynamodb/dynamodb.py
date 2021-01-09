import json
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    print(json.dumps(event))
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Series')

        if not table:
            raise Exception('Table not present')

        movies = table.scan()

        if movies == {}:
            raise Exception('Empty table')

        series_id = event['pathParameters']['series']

        dynamodb_response = table.query(KeyConditionExpression=Key('SID').eq(series_id))
        print(dynamodb_response)

        if dynamodb_response['Items'] == []:
            raise Exception('SID is not present')

    except Exception as e:
        return {
            'statusCode': 200,
            'body': str(e)
        }

    return {
        'statusCode': 200,
        'body': json.dumps(dynamodb_response['Items'][0], default=str)
    }

