import json
import boto3
from botocore.exceptions import ClientError

# Inizializza la risorsa DynamoDB e specifica la tabella "Users"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def create_user(event, context):
    try:
        # Verifica che 'body' esista e sia un JSON valido
        if 'body' not in event:
            return {
                'statusCode': 400,  # Restituisce un codice di errore 400 se il body è mancante
                'body': json.dumps({'error': 'Missing body in request'})  # Messaggio di errore
            }
        
        # Decodifica il body JSON della richiesta
        body = json.loads(event['body'])
        
        # Verifica che 'id' e 'name' siano presenti nel body
        if 'id' not in body or 'name' not in body:
            return {
                'statusCode': 400,  # Restituisce un codice di errore 400 se 'id' o 'name' sono mancanti
                'body': json.dumps({'error': 'Missing id or name in request body'})  # Messaggio di errore
            }

        # Estrae l'id e il nome dell'utente dal body della richiesta
        user_id = body['id']
        user_name = body['name']

        # Inserisce l'utente nella tabella DynamoDB
        table.put_item(Item={'id': user_id, 'name': user_name})

        return {
            'statusCode': 200,  # Restituisce un codice 200 per successo
            'body': json.dumps({'message': 'User created successfully'})  # Messaggio di conferma
        }
    except Exception as e:
        # Gestisce eventuali eccezioni generiche e restituisce un errore
        return {
            'statusCode': 400,  # Restituisce un codice 400 in caso di errore generico
            'body': json.dumps({'error': str(e)})  # Include il messaggio di errore
        }

def get_user_by_id(event, context):
    try:
        # Verifica che 'pathParameters' esista e contenga 'id'
        if 'pathParameters' not in event or 'id' not in event['pathParameters']:
            return {
                'statusCode': 400,  # Restituisce un codice di errore 400 se il parametro 'id' è mancante
                'body': json.dumps({'error': 'Missing id in path parameters'})  # Messaggio di errore
            }
        
        # Estrae l'id dell'utente dai parametri di percorso
        user_id = event['pathParameters']['id']

        # Recupera l'utente dalla tabella DynamoDB utilizzando l'id
        response = table.get_item(Key={'id': user_id})

        # Verifica se l'utente esiste nella tabella
        if 'Item' in response:
            return {
                'statusCode': 200,  # Restituisce un codice 200 per successo
                'body': json.dumps(response['Item'])  # Restituisce i dati dell'utente
            }
        else:
            return {
                'statusCode': 404,  # Restituisce un codice 404 se l'utente non è trovato
                'body': json.dumps({'error': 'User not found'})  # Messaggio di errore se l'utente non esiste
            }
    except ClientError as e:
        # Gestisce errori specifici del client AWS (es. permessi, risorse mancanti)
        return {
            'statusCode': 500,  # Restituisce un codice 500 per errori del server
            'body': json.dumps({'error': str(e)})  # Include il messaggio di errore specifico del client AWS
        }
    except Exception as e:
        # Gestisce qualsiasi altra eccezione generica
        return {
            'statusCode': 500,  # Restituisce un codice 500 in caso di errore generico
            'body': json.dumps({'error': str(e)})  # Include il messaggio di errore
        }
