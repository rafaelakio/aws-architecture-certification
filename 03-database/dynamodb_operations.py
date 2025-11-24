"""
DynamoDB - Exemplo Completo
Banco de dados NoSQL serverless da AWS
"""

import boto3
from typing import Dict, List, Any
from botocore.exceptions import ClientError
from decimal import Decimal
import json

class DynamoDBManager:
    """
    Gerenciador de operações DynamoDB
    Conceitos essenciais para certificação
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Inicializa cliente DynamoDB
        
        Args:
            region_name: Região AWS
        """
        # Client para operações de baixo nível
        self.dynamodb_client = boto3.client('dynamodb', region_name=region_name)
        
        # Resource para operações de alto nível (mais pythonic)
        self.dynamodb_resource = boto3.resource('dynamodb', region_name=region_name)
        
        self.region = region_name
    
    def create_table(
        self,
        table_name: str,
        partition_key: str,
        partition_key_type: str = 'S',
        sort_key: str = None,
        sort_key_type: str = 'S',
        billing_mode: str = 'PAY_PER_REQUEST'
    ) -> str:
        """
        Cria tabela DynamoDB
        
        DynamoDB Conceitos:
        - Partition Key (Hash Key): Chave primária obrigatória
        - Sort Key (Range Key): Chave de ordenação opcional
        - Composite Key: Partition Key + Sort Key
        - Key Types: S (String), N (Number), B (Binary)
        
        Billing Modes:
        - PAY_PER_REQUEST (On-Demand): Paga por requisição
        - PROVISIONED: Define RCU/WCU (mais barato para uso previsível)
        
        Args:
            table_name: Nome da tabela
            partition_key: Nome da partition key
            partition_key_type: Tipo da partition key (S, N, B)
            sort_key: Nome da sort key (opcional)
            sort_key_type: Tipo da sort key
            billing_mode: Modo de cobrança
        
        Returns:
            table_arn: ARN da tabela criada
        """
        try:
            # Define schema de chaves
            key_schema = [
                {
                    'AttributeName': partition_key,
                    'KeyType': 'HASH'  # Partition key
                }
            ]
            
            # Define definições de atributos
            attribute_definitions = [
                {
                    'AttributeName': partition_key,
                    'AttributeType': partition_key_type
                }
            ]
            
            # Adiciona sort key se fornecida
            if sort_key:
                key_schema.append({
                    'AttributeName': sort_key,
                    'KeyType': 'RANGE'  # Sort key
                })
                attribute_definitions.append({
                    'AttributeName': sort_key,
                    'AttributeType': sort_key_type
                })
            
            # Parâmetros da tabela
            params = {
                'TableName': table_name,
                'KeySchema': key_schema,
                'AttributeDefinitions': attribute_definitions,
                'BillingMode': billing_mode
            }
            
            # Se modo provisionado, define capacidade
            if billing_mode == 'PROVISIONED':
                params['ProvisionedThroughput'] = {
                    'ReadCapacityUnits': 5,  # RCU
                    'WriteCapacityUnits': 5  # WCU
                }
            
            # Cria tabela
            response = self.dynamodb_client.create_table(**params)
            
            table_arn = response['TableDescription']['TableArn']
            print(f"Tabela {table_name} criada com sucesso!")
            print(f"ARN: {table_arn}")
            
            # Aguarda tabela estar ativa
            print("Aguardando tabela ficar ativa...")
            waiter = self.dynamodb_client.get_waiter('table_exists')
            waiter.wait(TableName=table_name)
            
            return table_arn
            
        except ClientError as e:
            print(f"Erro ao criar tabela: {e}")
            raise
    
    def put_item(
        self,
        table_name: str,
        item: Dict[str, Any]
    ) -> bool:
        """
        Insere ou substitui item na tabela
        
        PutItem:
        - Cria novo item ou substitui existente
        - Requer partition key (e sort key se definida)
        - Consome 1 WCU por KB
        
        Args:
            table_name: Nome da tabela
            item: Dicionário com dados do item
        
        Returns:
            bool: True se sucesso
        """
        try:
            table = self.dynamodb_resource.Table(table_name)
            
            # put_item insere ou substitui completamente o item
            table.put_item(Item=item)
            
            print(f"Item inserido na tabela {table_name}")
            return True
            
        except ClientError as e:
            print(f"Erro ao inserir item: {e}")
            return False
    
    def get_item(
        self,
        table_name: str,
        key: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Busca item por chave primária
        
        GetItem:
        - Busca por partition key (e sort key se aplicável)
        - Operação mais eficiente do DynamoDB
        - Eventually consistent por padrão
        - Pode ser strongly consistent (consome 2x RCU)
        - Consome 1 RCU por 4KB (eventually) ou 2 RCU (strongly)
        
        Args:
            table_name: Nome da tabela
            key: Dicionário com partition key (e sort key se aplicável)
        
        Returns:
            Dict com dados do item ou {} se não encontrado
        """
        try:
            table = self.dynamodb_resource.Table(table_name)
            
            # get_item busca por chave primária
            response = table.get_item(
                Key=key,
                # ConsistentRead=True  # Descomente para strongly consistent
            )
            
            # Retorna item se encontrado
            item = response.get('Item', {})
            
            if item:
                print(f"Item encontrado: {item}")
            else:
                print("Item não encontrado")
            
            return item
            
        except ClientError as e:
            print(f"Erro ao buscar item: {e}")
            return {}
    
    def update_item(
        self,
        table_name: str,
        key: Dict[str, Any],
        update_expression: str,
        expression_values: Dict[str, Any]
    ) -> bool:
        """
        Atualiza item existente
        
        UpdateItem:
        - Atualiza atributos específicos (não substitui item inteiro)
        - Cria item se não existir
        - Suporta operações atômicas (incremento, append, etc)
        - Usa UpdateExpression para definir mudanças
        
        Update Expressions:
        - SET: Define ou atualiza atributo
        - REMOVE: Remove atributo
        - ADD: Incrementa número ou adiciona a set
        - DELETE: Remove elemento de set
        
        Args:
            table_name: Nome da tabela
            key: Chave primária do item
            update_expression: Expressão de atualização
            expression_values: Valores para a expressão
        
        Returns:
            bool: True se sucesso
        """
        try:
            table = self.dynamodb_resource.Table(table_name)
            
            # update_item atualiza atributos específicos
            table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues='UPDATED_NEW'  # Retorna valores atualizados
            )
            
            print(f"Item atualizado na tabela {table_name}")
            return True
            
        except ClientError as e:
            print(f"Erro ao atualizar item: {e}")
            return False
    
    def delete_item(
        self,
        table_name: str,
        key: Dict[str, Any]
    ) -> bool:
        """
        Deleta item da tabela
        
        DeleteItem:
        - Remove item completamente
        - Não retorna erro se item não existe
        - Consome 1 WCU por KB
        
        Args:
            table_name: Nome da tabela
            key: Chave primária do item
        
        Returns:
            bool: True se sucesso
        """
        try:
            table = self.dynamodb_resource.Table(table_name)
            
            # delete_item remove o item
            table.delete_item(Key=key)
            
            print(f"Item deletado da tabela {table_name}")
            return True
            
        except ClientError as e:
            print(f"Erro ao deletar item: {e}")
            return False
    
    def query(
        self,
        table_name: str,
        key_condition_expression: str,
        expression_values: Dict[str, Any],
        index_name: str = None
    ) -> List[Dict[str, Any]]:
        """
        Consulta itens usando partition key
        
        Query:
        - Busca por partition key (obrigatório)
        - Pode filtrar por sort key (opcional)
        - Retorna itens ordenados por sort key
        - Mais eficiente que Scan
        - Pode usar índices secundários
        - Consome RCU baseado em dados retornados
        
        Args:
            table_name: Nome da tabela
            key_condition_expression: Condição de busca
            expression_values: Valores para a expressão
            index_name: Nome do índice secundário (opcional)
        
        Returns:
            Lista de itens encontrados
        """
        try:
            table = self.dynamodb_resource.Table(table_name)
            
            params = {
                'KeyConditionExpression': key_condition_expression,
                'ExpressionAttributeValues': expression_values
            }
            
            # Adiciona índice se fornecido
            if index_name:
                params['IndexName'] = index_name
            
            # Executa query
            response = table.query(**params)
            
            items = response.get('Items', [])
            print(f"Query retornou {len(items)} itens")
            
            return items
            
        except ClientError as e:
            print(f"Erro ao executar query: {e}")
            return []
    
    def scan(
        self,
        table_name: str,
        filter_expression: str = None,
        expression_values: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Escaneia toda a tabela
        
        Scan:
        - Lê todos os itens da tabela
        - Muito custoso (consome RCU de toda tabela)
        - Deve ser evitado em produção
        - Use Query quando possível
        - Pode aplicar filtros (mas ainda lê tudo)
        - Suporta parallel scan para performance
        
        Args:
            table_name: Nome da tabela
            filter_expression: Expressão de filtro (opcional)
            expression_values: Valores para a expressão
        
        Returns:
            Lista de itens encontrados
        """
        try:
            table = self.dynamodb_resource.Table(table_name)
            
            params = {}
            
            # Adiciona filtro se fornecido
            if filter_expression and expression_values:
                params['FilterExpression'] = filter_expression
                params['ExpressionAttributeValues'] = expression_values
            
            # Executa scan
            response = table.scan(**params)
            
            items = response.get('Items', [])
            print(f"Scan retornou {len(items)} itens")
            print("⚠️  Scan é custoso! Use Query quando possível.")
            
            return items
            
        except ClientError as e:
            print(f"Erro ao executar scan: {e}")
            return []
    
    def create_global_secondary_index(
        self,
        table_name: str,
        index_name: str,
        partition_key: str,
        partition_key_type: str = 'S',
        sort_key: str = None,
        sort_key_type: str = 'S'
    ) -> bool:
        """
        Cria Global Secondary Index (GSI)
        
        GSI (Global Secondary Index):
        - Índice com partition key e sort key diferentes da tabela
        - Permite queries em atributos não-chave
        - Tem sua própria capacidade (RCU/WCU)
        - Eventually consistent
        - Pode ser criado/deletado após criação da tabela
        - Máximo 20 GSIs por tabela
        
        LSI (Local Secondary Index):
        - Mesma partition key, sort key diferente
        - Compartilha capacidade com tabela
        - Strongly ou eventually consistent
        - Deve ser criado na criação da tabela
        - Máximo 5 LSIs por tabela
        
        Args:
            table_name: Nome da tabela
            index_name: Nome do índice
            partition_key: Partition key do índice
            partition_key_type: Tipo da partition key
            sort_key: Sort key do índice (opcional)
            sort_key_type: Tipo da sort key
        
        Returns:
            bool: True se sucesso
        """
        try:
            # Define schema do índice
            key_schema = [
                {
                    'AttributeName': partition_key,
                    'KeyType': 'HASH'
                }
            ]
            
            # Define atributos
            attribute_definitions = [
                {
                    'AttributeName': partition_key,
                    'AttributeType': partition_key_type
                }
            ]
            
            # Adiciona sort key se fornecida
            if sort_key:
                key_schema.append({
                    'AttributeName': sort_key,
                    'KeyType': 'RANGE'
                })
                attribute_definitions.append({
                    'AttributeName': sort_key,
                    'AttributeType': sort_key_type
                })
            
            # Cria GSI
            self.dynamodb_client.update_table(
                TableName=table_name,
                AttributeDefinitions=attribute_definitions,
                GlobalSecondaryIndexUpdates=[
                    {
                        'Create': {
                            'IndexName': index_name,
                            'KeySchema': key_schema,
                            'Projection': {
                                'ProjectionType': 'ALL'  # ALL, KEYS_ONLY, INCLUDE
                            },
                            'ProvisionedThroughput': {
                                'ReadCapacityUnits': 5,
                                'WriteCapacityUnits': 5
                            }
                        }
                    }
                ]
            )
            
            print(f"GSI {index_name} criado na tabela {table_name}")
            return True
            
        except ClientError as e:
            print(f"Erro ao criar GSI: {e}")
            return False
    
    def enable_streams(
        self,
        table_name: str,
        stream_view_type: str = 'NEW_AND_OLD_IMAGES'
    ) -> str:
        """
        Habilita DynamoDB Streams
        
        DynamoDB Streams:
        - Captura mudanças na tabela (insert, update, delete)
        - Ordenado por chave primária
        - Retenção de 24 horas
        - Pode acionar Lambda functions
        - Casos de uso: Replicação, Auditoria, Analytics
        
        Stream View Types:
        - KEYS_ONLY: Apenas chaves
        - NEW_IMAGE: Novo item completo
        - OLD_IMAGE: Item antigo completo
        - NEW_AND_OLD_IMAGES: Ambos
        
        Args:
            table_name: Nome da tabela
            stream_view_type: Tipo de visualização do stream
        
        Returns:
            stream_arn: ARN do stream
        """
        try:
            response = self.dynamodb_client.update_table(
                TableName=table_name,
                StreamSpecification={
                    'StreamEnabled': True,
                    'StreamViewType': stream_view_type
                }
            )
            
            stream_arn = response['TableDescription']['LatestStreamArn']
            print(f"DynamoDB Streams habilitado para {table_name}")
            print(f"Stream ARN: {stream_arn}")
            
            return stream_arn
            
        except ClientError as e:
            print(f"Erro ao habilitar streams: {e}")
            raise


# Exemplo de uso completo
if __name__ == "__main__":
    dynamodb_manager = DynamoDBManager(region_name='us-east-1')
    
    table_name = "Users"
    
    print("\n=== Exemplo 1: Criar Tabela ===")
    dynamodb_manager.create_table(
        table_name=table_name,
        partition_key='user_id',
        partition_key_type='S',
        sort_key='timestamp',
        sort_key_type='N',
        billing_mode='PAY_PER_REQUEST'
    )
    
    print("\n=== Exemplo 2: Inserir Itens ===")
    # DynamoDB usa Decimal para números
    dynamodb_manager.put_item(
        table_name=table_name,
        item={
            'user_id': 'user123',
            'timestamp': Decimal('1234567890'),
            'name': 'João Silva',
            'email': 'joao@example.com',
            'age': Decimal('30'),
            'active': True
        }
    )
    
    dynamodb_manager.put_item(
        table_name=table_name,
        item={
            'user_id': 'user123',
            'timestamp': Decimal('1234567900'),
            'name': 'João Silva',
            'email': 'joao@example.com',
            'age': Decimal('30'),
            'status': 'updated'
        }
    )
    
    print("\n=== Exemplo 3: Buscar Item ===")
    item = dynamodb_manager.get_item(
        table_name=table_name,
        key={
            'user_id': 'user123',
            'timestamp': Decimal('1234567890')
        }
    )
    
    print("\n=== Exemplo 4: Atualizar Item ===")
    dynamodb_manager.update_item(
        table_name=table_name,
        key={
            'user_id': 'user123',
            'timestamp': Decimal('1234567890')
        },
        update_expression='SET age = :age, #status = :status',
        expression_values={
            ':age': Decimal('31'),
            ':status': 'active'
        }
    )
    
    print("\n=== Exemplo 5: Query (busca eficiente) ===")
    from boto3.dynamodb.conditions import Key
    
    table = dynamodb_manager.dynamodb_resource.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('user_id').eq('user123')
    )
    print(f"Encontrados {len(response['Items'])} itens para user123")
    
    print("\n=== Exemplo 6: Habilitar Streams ===")
    stream_arn = dynamodb_manager.enable_streams(
        table_name=table_name,
        stream_view_type='NEW_AND_OLD_IMAGES'
    )
    
    print("\n✅ Exemplos DynamoDB concluídos!")
    print("\n💡 Dicas para Certificação:")
    print("- Use Query ao invés de Scan sempre que possível")
    print("- GSI permite queries em atributos não-chave")
    print("- DynamoDB Streams para capturar mudanças")
    print("- On-Demand para cargas imprevisíveis")
    print("- Provisioned para cargas previsíveis (mais barato)")
