"""
SQS e SNS - Exemplo Completo
Serviços de mensageria e notificação da AWS
"""

import boto3
import json
from typing import List, Dict
from botocore.exceptions import ClientError
import time

class MessagingManager:
    """
    Gerenciador de SQS e SNS
    Demonstra padrões de mensageria para certificação
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Inicializa clientes SQS e SNS
        
        Args:
            region_name: Região AWS
        """
        self.sqs_client = boto3.client('sqs', region_name=region_name)
        self.sns_client = boto3.client('sns', region_name=region_name)
        self.region = region_name
    
    # ========== SQS Operations ==========
    
    def create_sqs_queue(
        self,
        queue_name: str,
        is_fifo: bool = False,
        visibility_timeout: int = 30,
        message_retention: int = 345600  # 4 dias
    ) -> str:
        """
        Cria fila SQS
        
        SQS Conceitos:
        - Standard Queue: At-least-once delivery, ordem não garantida
        - FIFO Queue: Exactly-once, ordem garantida, .fifo no nome
        - Visibility Timeout: Tempo que mensagem fica invisível após leitura
        - Message Retention: Tempo que mensagem fica na fila (1 min - 14 dias)
        - Dead Letter Queue: Fila para mensagens que falharam múltiplas vezes
        
        Args:
            queue_name: Nome da fila
            is_fifo: Se True, cria fila FIFO
            visibility_timeout: Timeout de visibilidade (segundos)
            message_retention: Retenção de mensagens (segundos)
        
        Returns:
            queue_url: URL da fila criada
        """
        try:
            # FIFO queues devem terminar com .fifo
            if is_fifo and not queue_name.endswith('.fifo'):
                queue_name += '.fifo'
            
            # Atributos da fila
            attributes = {
                'VisibilityTimeout': str(visibility_timeout),
                'MessageRetentionPeriod': str(message_retention),
                'ReceiveMessageWaitTimeSeconds': '20'  # Long polling
            }
            
            # Atributos específicos de FIFO
            if is_fifo:
                attributes['FifoQueue'] = 'true'
                # Content-based deduplication evita duplicatas
                attributes['ContentBasedDeduplication'] = 'true'
            
            # Cria fila
            response = self.sqs_client.create_queue(
                QueueName=queue_name,
                Attributes=attributes
            )
            
            queue_url = response['QueueUrl']
            print(f"Fila SQS criada: {queue_name}")
            print(f"URL: {queue_url}")
            
            return queue_url
            
        except ClientError as e:
            print(f"Erro ao criar fila: {e}")
            raise
    
    def send_message(
        self,
        queue_url: str,
        message_body: str,
        message_attributes: Dict = None,
        message_group_id: str = None,
        message_deduplication_id: str = None
    ) -> str:
        """
        Envia mensagem para fila SQS
        
        Args:
            queue_url: URL da fila
            message_body: Corpo da mensagem (string ou JSON)
            message_attributes: Atributos customizados
            message_group_id: ID do grupo (obrigatório para FIFO)
            message_deduplication_id: ID de deduplicação (FIFO)
        
        Returns:
            message_id: ID da mensagem enviada
        """
        try:
            params = {
                'QueueUrl': queue_url,
                'MessageBody': message_body
            }
            
            # Adiciona atributos se fornecidos
            if message_attributes:
                params['MessageAttributes'] = message_attributes
            
            # Parâmetros FIFO
            if message_group_id:
                params['MessageGroupId'] = message_group_id
            
            if message_deduplication_id:
                params['MessageDeduplicationId'] = message_deduplication_id
            
            # Envia mensagem
            response = self.sqs_client.send_message(**params)
            
            message_id = response['MessageId']
            print(f"Mensagem enviada: {message_id}")
            
            return message_id
            
        except ClientError as e:
            print(f"Erro ao enviar mensagem: {e}")
            raise
    
    def receive_messages(
        self,
        queue_url: str,
        max_messages: int = 1,
        wait_time: int = 20
    ) -> List[Dict]:
        """
        Recebe mensagens da fila SQS
        
        Long Polling vs Short Polling:
        - Long Polling (wait_time > 0): Aguarda até mensagem chegar
        - Short Polling (wait_time = 0): Retorna imediatamente
        - Long polling reduz custos e latência
        
        Args:
            queue_url: URL da fila
            max_messages: Número máximo de mensagens (1-10)
            wait_time: Tempo de espera para long polling
        
        Returns:
            Lista de mensagens recebidas
        """
        try:
            # Recebe mensagens
            # Long polling é mais eficiente
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,
                MessageAttributeNames=['All'],
                AttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            
            if messages:
                print(f"Recebidas {len(messages)} mensagens")
                for msg in messages:
                    print(f"  - ID: {msg['MessageId']}")
                    print(f"    Body: {msg['Body'][:100]}...")
            else:
                print("Nenhuma mensagem na fila")
            
            return messages
            
        except ClientError as e:
            print(f"Erro ao receber mensagens: {e}")
            return []
    
    def delete_message(
        self,
        queue_url: str,
        receipt_handle: str
    ) -> bool:
        """
        Deleta mensagem da fila após processamento
        
        IMPORTANTE: Sempre delete mensagens após processar
        Caso contrário, voltarão para fila após visibility timeout
        
        Args:
            queue_url: URL da fila
            receipt_handle: Handle da mensagem (obtido no receive)
        
        Returns:
            bool: True se sucesso
        """
        try:
            self.sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            
            print("Mensagem deletada com sucesso")
            return True
            
        except ClientError as e:
            print(f"Erro ao deletar mensagem: {e}")
            return False
    
    # ========== SNS Operations ==========
    
    def create_sns_topic(
        self,
        topic_name: str,
        is_fifo: bool = False
    ) -> str:
        """
        Cria tópico SNS
        
        SNS Conceitos:
        - Pub/Sub: Um publisher, múltiplos subscribers
        - Fan-out: Distribuir mensagem para múltiplos destinos
        - Protocols: Email, SMS, HTTP/HTTPS, Lambda, SQS
        - Standard: At-least-once, ordem não garantida
        - FIFO: Exactly-once, ordem garantida
        
        Args:
            topic_name: Nome do tópico
            is_fifo: Se True, cria tópico FIFO
        
        Returns:
            topic_arn: ARN do tópico criado
        """
        try:
            # FIFO topics devem terminar com .fifo
            if is_fifo and not topic_name.endswith('.fifo'):
                topic_name += '.fifo'
            
            # Atributos do tópico
            attributes = {}
            if is_fifo:
                attributes['FifoTopic'] = 'true'
                attributes['ContentBasedDeduplication'] = 'true'
            
            # Cria tópico
            response = self.sns_client.create_topic(
                Name=topic_name,
                Attributes=attributes
            )
            
            topic_arn = response['TopicArn']
            print(f"Tópico SNS criado: {topic_name}")
            print(f"ARN: {topic_arn}")
            
            return topic_arn
            
        except ClientError as e:
            print(f"Erro ao criar tópico: {e}")
            raise
    
    def subscribe_to_topic(
        self,
        topic_arn: str,
        protocol: str,
        endpoint: str
    ) -> str:
        """
        Inscreve endpoint em tópico SNS
        
        Protocols:
        - email: Envia email (requer confirmação)
        - sms: Envia SMS
        - http/https: POST para URL
        - lambda: Invoca função Lambda
        - sqs: Envia para fila SQS
        - application: Push notification mobile
        
        Args:
            topic_arn: ARN do tópico
            protocol: Protocolo (email, sms, http, lambda, sqs)
            endpoint: Destino (email, phone, URL, ARN)
        
        Returns:
            subscription_arn: ARN da inscrição
        """
        try:
            response = self.sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol=protocol,
                Endpoint=endpoint
            )
            
            subscription_arn = response['SubscriptionArn']
            print(f"Inscrição criada: {protocol} -> {endpoint}")
            
            if protocol == 'email':
                print("⚠️  Verifique seu email para confirmar inscrição")
            
            return subscription_arn
            
        except ClientError as e:
            print(f"Erro ao criar inscrição: {e}")
            raise
    
    def publish_to_topic(
        self,
        topic_arn: str,
        message: str,
        subject: str = None,
        message_attributes: Dict = None
    ) -> str:
        """
        Publica mensagem em tópico SNS
        
        Args:
            topic_arn: ARN do tópico
            message: Mensagem a publicar
            subject: Assunto (para email)
            message_attributes: Atributos customizados
        
        Returns:
            message_id: ID da mensagem publicada
        """
        try:
            params = {
                'TopicArn': topic_arn,
                'Message': message
            }
            
            if subject:
                params['Subject'] = subject
            
            if message_attributes:
                params['MessageAttributes'] = message_attributes
            
            # Publica mensagem
            response = self.sns_client.publish(**params)
            
            message_id = response['MessageId']
            print(f"Mensagem publicada: {message_id}")
            
            return message_id
            
        except ClientError as e:
            print(f"Erro ao publicar mensagem: {e}")
            raise
    
    # ========== Fan-Out Pattern ==========
    
    def create_fanout_architecture(
        self,
        topic_name: str,
        queue_names: List[str]
    ) -> Dict:
        """
        Cria arquitetura Fan-Out (SNS -> múltiplas SQS)
        
        Fan-Out Pattern:
        - Uma mensagem SNS é distribuída para múltiplas filas SQS
        - Cada fila processa independentemente
        - Útil para processamento paralelo
        
        Casos de uso:
        - Processar pedido: notificar estoque, pagamento, envio
        - Upload de imagem: gerar thumbnails, extrair metadados, scan vírus
        - Evento de usuário: analytics, notificação, auditoria
        
        Args:
            topic_name: Nome do tópico SNS
            queue_names: Lista de nomes de filas SQS
        
        Returns:
            Dict com ARNs criados
        """
        try:
            print("\n=== Criando Arquitetura Fan-Out ===")
            
            # Cria tópico SNS
            topic_arn = self.create_sns_topic(topic_name)
            
            queue_arns = []
            
            # Cria filas e inscreve no tópico
            for queue_name in queue_names:
                # Cria fila
                queue_url = self.create_sqs_queue(queue_name)
                
                # Obtém ARN da fila
                attrs = self.sqs_client.get_queue_attributes(
                    QueueUrl=queue_url,
                    AttributeNames=['QueueArn']
                )
                queue_arn = attrs['Attributes']['QueueArn']
                queue_arns.append(queue_arn)
                
                # Configura política de acesso da fila
                # Permite SNS enviar mensagens
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Principal": {"Service": "sns.amazonaws.com"},
                        "Action": "sqs:SendMessage",
                        "Resource": queue_arn,
                        "Condition": {
                            "ArnEquals": {
                                "aws:SourceArn": topic_arn
                            }
                        }
                    }]
                }
                
                self.sqs_client.set_queue_attributes(
                    QueueUrl=queue_url,
                    Attributes={
                        'Policy': json.dumps(policy)
                    }
                )
                
                # Inscreve fila no tópico
                self.subscribe_to_topic(
                    topic_arn=topic_arn,
                    protocol='sqs',
                    endpoint=queue_arn
                )
            
            print("\n✅ Arquitetura Fan-Out criada com sucesso!")
            
            return {
                'topic_arn': topic_arn,
                'queue_arns': queue_arns
            }
            
        except ClientError as e:
            print(f"Erro ao criar fan-out: {e}")
            raise


# Exemplo de uso completo
if __name__ == "__main__":
    messaging = MessagingManager(region_name='us-east-1')
    
    print("\n=== Exemplo 1: SQS Standard Queue ===")
    
    # Cria fila standard
    queue_url = messaging.create_sqs_queue(
        queue_name='orders-queue',
        is_fifo=False
    )
    
    # Envia mensagens
    for i in range(3):
        messaging.send_message(
            queue_url=queue_url,
            message_body=json.dumps({
                'order_id': f'ORD-{i+1}',
                'customer': f'Customer {i+1}',
                'amount': 100.00 * (i+1)
            })
        )
    
    # Recebe e processa mensagens
    messages = messaging.receive_messages(queue_url, max_messages=10)
    
    for message in messages:
        # Processa mensagem
        body = json.loads(message['Body'])
        print(f"Processando pedido: {body['order_id']}")
        
        # Deleta após processar
        messaging.delete_message(queue_url, message['ReceiptHandle'])
    
    print("\n=== Exemplo 2: SQS FIFO Queue ===")
    
    # Cria fila FIFO
    fifo_queue_url = messaging.create_sqs_queue(
        queue_name='transactions-queue',
        is_fifo=True
    )
    
    # Envia mensagens FIFO
    for i in range(3):
        messaging.send_message(
            queue_url=fifo_queue_url,
            message_body=f'Transaction {i+1}',
            message_group_id='group1',  # Obrigatório para FIFO
            message_deduplication_id=f'txn-{i+1}'  # Evita duplicatas
        )
    
    print("\n=== Exemplo 3: SNS Topic ===")
    
    # Cria tópico
    topic_arn = messaging.create_sns_topic('notifications-topic')
    
    # Inscreve email (requer confirmação)
    # messaging.subscribe_to_topic(
    #     topic_arn=topic_arn,
    #     protocol='email',
    #     endpoint='your-email@example.com'
    # )
    
    # Publica mensagem
    messaging.publish_to_topic(
        topic_arn=topic_arn,
        message='Sistema de pedidos está operacional',
        subject='Status do Sistema'
    )
    
    print("\n=== Exemplo 4: Fan-Out Pattern ===")
    
    # Cria arquitetura fan-out
    fanout = messaging.create_fanout_architecture(
        topic_name='order-events',
        queue_names=[
            'inventory-queue',
            'payment-queue',
            'shipping-queue'
        ]
    )
    
    # Publica evento que será distribuído para todas as filas
    messaging.publish_to_topic(
        topic_arn=fanout['topic_arn'],
        message=json.dumps({
            'event': 'order_created',
            'order_id': 'ORD-12345',
            'timestamp': time.time()
        })
    )
    
    print("\n✅ Exemplos concluídos!")
    print("\n💡 Conceitos importantes:")
    print("- SQS Standard: At-least-once, ordem não garantida")
    print("- SQS FIFO: Exactly-once, ordem garantida")
    print("- SNS: Pub/Sub para múltiplos subscribers")
    print("- Fan-Out: SNS -> múltiplas SQS para processamento paralelo")
    print("- Long Polling: Reduz custos e latência")
    print("- Dead Letter Queue: Para mensagens que falharam")
