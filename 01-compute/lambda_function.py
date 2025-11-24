"""
AWS Lambda - Exemplo Completo
Demonstra conceitos importantes de Lambda para certificação
"""

import boto3
import json
import os
from datetime import datetime
from typing import Dict, Any

# Cliente S3 global (reutilizado entre invocações - boa prática)
# Conexões são mantidas entre cold starts
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler principal da função Lambda
    
    Esta é a função que a AWS Lambda invoca quando a função é executada.
    
    Args:
        event: Dicionário contendo dados do evento que acionou a função
               Estrutura varia conforme o trigger (S3, API Gateway, etc)
        context: Objeto com informações sobre a execução e ambiente
                 Contém: request_id, function_name, memory_limit, etc
    
    Returns:
        Dict com statusCode e body (formato esperado pelo API Gateway)
    """
    
    # Log do evento recebido (visível no CloudWatch Logs)
    print(f"Evento recebido: {json.dumps(event)}")
    
    # Informações do contexto de execução
    # Úteis para debugging e monitoramento
    print(f"Request ID: {context.request_id}")
    print(f"Function Name: {context.function_name}")
    print(f"Memory Limit: {context.memory_limit_in_mb} MB")
    print(f"Time Remaining: {context.get_remaining_time_in_millis()} ms")
    
    try:
        # Processa o evento baseado na fonte
        if 'Records' in event:
            # Evento vindo do S3
            return process_s3_event(event, context)
        elif 'httpMethod' in event:
            # Evento vindo do API Gateway
            return process_api_gateway_event(event, context)
        elif 'source' in event and event['source'] == 'aws.events':
            # Evento vindo do EventBridge/CloudWatch Events
            return process_eventbridge_event(event, context)
        else:
            # Evento genérico
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Evento processado com sucesso',
                    'timestamp': datetime.now().isoformat()
                })
            }
    
    except Exception as e:
        # Tratamento de erros
        # Erros não tratados causam retry automático (dependendo da configuração)
        print(f"Erro ao processar evento: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Erro ao processar requisição'
            })
        }


def process_s3_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Processa eventos do S3
    
    Trigger comum: quando um arquivo é criado/modificado em um bucket
    
    Args:
        event: Evento do S3 contendo informações sobre o objeto
        context: Contexto da execução Lambda
    
    Returns:
        Dict com resultado do processamento
    """
    # Itera sobre todos os registros (pode haver múltiplos)
    for record in event['Records']:
        # Extrai informações do evento S3
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        event_name = record['eventName']
        
        print(f"Processando arquivo: s3://{bucket_name}/{object_key}")
        print(f"Tipo de evento: {event_name}")
        
        # Exemplo: Ler o conteúdo do arquivo
        try:
            # get_object retorna o objeto do S3
            response = s3_client.get_object(
                Bucket=bucket_name,
                Key=object_key
            )
            
            # Lê o conteúdo do arquivo
            # Body é um StreamingBody que precisa ser lido
            content = response['Body'].read().decode('utf-8')
            
            print(f"Conteúdo do arquivo (primeiros 100 chars): {content[:100]}")
            
            # Exemplo: Processar e salvar resultado em outro bucket
            processed_content = content.upper()  # Processamento simples
            
            # Salva resultado processado
            output_key = f"processed/{object_key}"
            s3_client.put_object(
                Bucket=bucket_name,
                Key=output_key,
                Body=processed_content.encode('utf-8'),
                ContentType='text/plain'
            )
            
            print(f"Arquivo processado salvo em: s3://{bucket_name}/{output_key}")
            
        except Exception as e:
            print(f"Erro ao processar arquivo S3: {str(e)}")
            raise
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Arquivos S3 processados com sucesso',
            'files_processed': len(event['Records'])
        })
    }


def process_api_gateway_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Processa eventos do API Gateway
    
    Usado quando Lambda é backend de uma API REST
    
    Args:
        event: Evento do API Gateway com httpMethod, path, body, etc
        context: Contexto da execução Lambda
    
    Returns:
        Dict com statusCode, headers e body (formato API Gateway)
    """
    # Extrai informações da requisição HTTP
    http_method = event['httpMethod']
    path = event['path']
    query_params = event.get('queryStringParameters', {})
    headers = event.get('headers', {})
    
    # Body pode vir como string JSON
    body = event.get('body', '{}')
    if isinstance(body, str):
        body = json.loads(body) if body else {}
    
    print(f"Requisição: {http_method} {path}")
    print(f"Query Params: {query_params}")
    print(f"Body: {body}")
    
    # Roteamento baseado no método HTTP
    if http_method == 'GET':
        # Exemplo: Buscar dados
        response_data = {
            'message': 'GET request processado',
            'path': path,
            'params': query_params
        }
        
    elif http_method == 'POST':
        # Exemplo: Criar recurso
        response_data = {
            'message': 'Recurso criado com sucesso',
            'data': body,
            'id': context.request_id
        }
        
    elif http_method == 'PUT':
        # Exemplo: Atualizar recurso
        response_data = {
            'message': 'Recurso atualizado com sucesso',
            'data': body
        }
        
    elif http_method == 'DELETE':
        # Exemplo: Deletar recurso
        response_data = {
            'message': 'Recurso deletado com sucesso'
        }
        
    else:
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # CORS
            },
            'body': json.dumps({
                'error': 'Método não permitido'
            })
        }
    
    # Resposta no formato esperado pelo API Gateway
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # CORS - importante para APIs públicas
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization'
        },
        'body': json.dumps(response_data)
    }


def process_eventbridge_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Processa eventos do EventBridge (CloudWatch Events)
    
    Usado para execuções agendadas (cron) ou eventos customizados
    
    Args:
        event: Evento do EventBridge
        context: Contexto da execução Lambda
    
    Returns:
        Dict com resultado do processamento
    """
    # Extrai informações do evento
    detail_type = event.get('detail-type', 'Unknown')
    source = event.get('source', 'Unknown')
    detail = event.get('detail', {})
    
    print(f"EventBridge Event - Type: {detail_type}, Source: {source}")
    print(f"Detail: {json.dumps(detail)}")
    
    # Exemplo: Executar tarefa agendada
    if detail_type == 'Scheduled Event':
        print("Executando tarefa agendada...")
        
        # Exemplo: Limpar arquivos antigos do S3
        # Exemplo: Gerar relatório diário
        # Exemplo: Backup de dados
        
        result = {
            'message': 'Tarefa agendada executada com sucesso',
            'execution_time': datetime.now().isoformat()
        }
    else:
        result = {
            'message': 'Evento EventBridge processado',
            'detail_type': detail_type
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }


def write_to_dynamodb(table_name: str, item: Dict[str, Any]) -> bool:
    """
    Escreve item no DynamoDB
    
    Exemplo de integração Lambda + DynamoDB (padrão comum)
    
    Args:
        table_name: Nome da tabela DynamoDB
        item: Dicionário com dados a serem salvos
    
    Returns:
        bool: True se sucesso
    """
    try:
        table = dynamodb.Table(table_name)
        
        # put_item insere ou substitui item
        table.put_item(Item=item)
        
        print(f"Item salvo no DynamoDB: {item}")
        return True
        
    except Exception as e:
        print(f"Erro ao salvar no DynamoDB: {str(e)}")
        return False


def send_sns_notification(topic_arn: str, message: str, subject: str = None) -> bool:
    """
    Envia notificação via SNS
    
    Exemplo de integração Lambda + SNS (padrão comum)
    
    Args:
        topic_arn: ARN do tópico SNS
        message: Mensagem a ser enviada
        subject: Assunto (opcional)
    
    Returns:
        bool: True se sucesso
    """
    try:
        sns_client = boto3.client('sns')
        
        params = {
            'TopicArn': topic_arn,
            'Message': message
        }
        
        if subject:
            params['Subject'] = subject
        
        # Publica mensagem no tópico
        response = sns_client.publish(**params)
        
        print(f"Notificação SNS enviada: {response['MessageId']}")
        return True
        
    except Exception as e:
        print(f"Erro ao enviar notificação SNS: {str(e)}")
        return False


# Exemplo de função Lambda com timeout handling
def long_running_task(context: Any) -> Dict[str, Any]:
    """
    Exemplo de tarefa de longa duração com controle de timeout
    
    Lambda tem limite de 15 minutos de execução
    É importante monitorar o tempo restante
    
    Args:
        context: Contexto da execução Lambda
    
    Returns:
        Dict com resultado
    """
    # Reserva 10 segundos para finalização
    safety_margin = 10000  # 10 segundos em milissegundos
    
    items_processed = 0
    
    while True:
        # Verifica tempo restante
        time_remaining = context.get_remaining_time_in_millis()
        
        if time_remaining < safety_margin:
            print(f"Tempo limite próximo. Parando processamento.")
            print(f"Items processados: {items_processed}")
            break
        
        # Processa item
        # ... seu código aqui ...
        items_processed += 1
        
        # Simula processamento
        import time
        time.sleep(0.1)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'items_processed': items_processed,
            'completed': time_remaining >= safety_margin
        })
    }


# Variáveis de ambiente (configuradas no console Lambda)
# Boa prática: usar variáveis de ambiente para configuração
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'default-table')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

print(f"Lambda inicializada - Environment: {ENVIRONMENT}")
