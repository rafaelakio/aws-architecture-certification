"""
EC2 Management - Exemplo Completo
Demonstra operações comuns com EC2 cobradas na certificação
"""

import boto3
import time
from typing import List, Dict
from botocore.exceptions import ClientError

class EC2Manager:
    """
    Classe para gerenciar instâncias EC2
    Demonstra padrões comuns de uso do serviço
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Inicializa o cliente EC2
        
        Args:
            region_name: Região AWS onde os recursos serão criados
        """
        # Cria cliente boto3 para EC2
        # boto3 é o SDK oficial da AWS para Python
        self.ec2_client = boto3.client('ec2', region_name=region_name)
        
        # Resource é uma abstração de alto nível sobre o client
        # Facilita operações orientadas a objetos
        self.ec2_resource = boto3.resource('ec2', region_name=region_name)
        
        self.region = region_name
    
    def create_instance(
        self,
        ami_id: str,
        instance_type: str = 't2.micro',
        key_name: str = None,
        security_group_ids: List[str] = None,
        subnet_id: str = None,
        user_data: str = None,
        tags: Dict[str, str] = None
    ) -> str:
        """
        Cria uma instância EC2 com configurações especificadas
        
        Args:
            ami_id: ID da Amazon Machine Image (ex: ami-0c55b159cbfafe1f0)
            instance_type: Tipo da instância (ex: t2.micro, m5.large)
            key_name: Nome do key pair para acesso SSH
            security_group_ids: Lista de IDs dos security groups
            subnet_id: ID da subnet onde a instância será criada
            user_data: Script de inicialização (bash ou cloud-init)
            tags: Dicionário de tags para organização
            
        Returns:
            instance_id: ID da instância criada
        """
        try:
            # Prepara os parâmetros para criação da instância
            # MinCount e MaxCount definem quantas instâncias criar
            params = {
                'ImageId': ami_id,  # AMI é o template do sistema operacional
                'InstanceType': instance_type,  # Define CPU, memória e rede
                'MinCount': 1,  # Mínimo de instâncias a criar
                'MaxCount': 1,  # Máximo de instâncias a criar
            }
            
            # Adiciona key pair se fornecido
            # Key pair é necessário para acesso SSH em instâncias Linux
            if key_name:
                params['KeyName'] = key_name
            
            # Adiciona security groups se fornecidos
            # Security Groups funcionam como firewall virtual
            if security_group_ids:
                params['SecurityGroupIds'] = security_group_ids
            
            # Adiciona subnet se fornecida
            # Subnet define em qual AZ e VPC a instância será criada
            if subnet_id:
                params['SubnetId'] = subnet_id
            
            # User Data permite executar scripts na inicialização
            # Útil para configuração automática (bootstrap)
            if user_data:
                params['UserData'] = user_data
            
            # Cria a instância
            response = self.ec2_client.run_instances(**params)
            
            # Extrai o ID da instância criada
            instance_id = response['Instances'][0]['InstanceId']
            
            # Aguarda a instância estar em estado 'running'
            # Importante: a instância pode levar alguns minutos para iniciar
            print(f"Aguardando instância {instance_id} iniciar...")
            waiter = self.ec2_client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[instance_id])
            
            # Adiciona tags se fornecidas
            # Tags são essenciais para organização e billing
            if tags:
                self.ec2_client.create_tags(
                    Resources=[instance_id],
                    Tags=[{'Key': k, 'Value': v} for k, v in tags.items()]
                )
            
            print(f"Instância {instance_id} criada com sucesso!")
            return instance_id
            
        except ClientError as e:
            print(f"Erro ao criar instância: {e}")
            raise
    
    def stop_instance(self, instance_id: str) -> bool:
        """
        Para uma instância EC2
        
        Importante: Instâncias paradas não geram custo de computação,
        mas volumes EBS anexados continuam gerando custo
        
        Args:
            instance_id: ID da instância a ser parada
            
        Returns:
            bool: True se operação foi bem sucedida
        """
        try:
            # Stop mantém os dados e configurações
            # A instância pode ser reiniciada posteriormente
            response = self.ec2_client.stop_instances(
                InstanceIds=[instance_id]
            )
            
            print(f"Parando instância {instance_id}...")
            
            # Aguarda a instância estar completamente parada
            waiter = self.ec2_client.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=[instance_id])
            
            print(f"Instância {instance_id} parada com sucesso!")
            return True
            
        except ClientError as e:
            print(f"Erro ao parar instância: {e}")
            return False
    
    def start_instance(self, instance_id: str) -> bool:
        """
        Inicia uma instância EC2 que estava parada
        
        Args:
            instance_id: ID da instância a ser iniciada
            
        Returns:
            bool: True se operação foi bem sucedida
        """
        try:
            # Start reinicia uma instância previamente parada
            response = self.ec2_client.start_instances(
                InstanceIds=[instance_id]
            )
            
            print(f"Iniciando instância {instance_id}...")
            
            # Aguarda a instância estar em execução
            waiter = self.ec2_client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[instance_id])
            
            print(f"Instância {instance_id} iniciada com sucesso!")
            return True
            
        except ClientError as e:
            print(f"Erro ao iniciar instância: {e}")
            return False
    
    def terminate_instance(self, instance_id: str) -> bool:
        """
        Termina (deleta) uma instância EC2
        
        ATENÇÃO: Esta operação é irreversível!
        Todos os dados em volumes EBS sem proteção serão perdidos
        
        Args:
            instance_id: ID da instância a ser terminada
            
        Returns:
            bool: True se operação foi bem sucedida
        """
        try:
            # Terminate deleta permanentemente a instância
            # Volumes EBS com DeleteOnTermination=True também serão deletados
            response = self.ec2_client.terminate_instances(
                InstanceIds=[instance_id]
            )
            
            print(f"Terminando instância {instance_id}...")
            
            # Aguarda a instância ser completamente terminada
            waiter = self.ec2_client.get_waiter('instance_terminated')
            waiter.wait(InstanceIds=[instance_id])
            
            print(f"Instância {instance_id} terminada com sucesso!")
            return True
            
        except ClientError as e:
            print(f"Erro ao terminar instância: {e}")
            return False
    
    def get_instance_info(self, instance_id: str) -> Dict:
        """
        Obtém informações detalhadas sobre uma instância
        
        Args:
            instance_id: ID da instância
            
        Returns:
            Dict com informações da instância
        """
        try:
            # describe_instances retorna informações detalhadas
            response = self.ec2_client.describe_instances(
                InstanceIds=[instance_id]
            )
            
            # Extrai informações da primeira instância
            instance = response['Reservations'][0]['Instances'][0]
            
            # Monta dicionário com informações relevantes
            info = {
                'InstanceId': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],  # running, stopped, terminated, etc
                'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                'SubnetId': instance.get('SubnetId', 'N/A'),
                'VpcId': instance.get('VpcId', 'N/A'),
                'LaunchTime': instance['LaunchTime'],
                'Tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            }
            
            return info
            
        except ClientError as e:
            print(f"Erro ao obter informações da instância: {e}")
            return {}
    
    def list_instances(self, filters: List[Dict] = None) -> List[Dict]:
        """
        Lista todas as instâncias com filtros opcionais
        
        Args:
            filters: Lista de filtros (ex: [{'Name': 'instance-state-name', 'Values': ['running']}])
            
        Returns:
            Lista de dicionários com informações das instâncias
        """
        try:
            # Prepara parâmetros da consulta
            params = {}
            if filters:
                params['Filters'] = filters
            
            # Obtém todas as instâncias
            response = self.ec2_client.describe_instances(**params)
            
            instances = []
            # Itera sobre todas as reservations e instâncias
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name'],
                        'PublicIp': instance.get('PublicIpAddress', 'N/A'),
                        'PrivateIp': instance.get('PrivateIpAddress', 'N/A'),
                        'LaunchTime': instance['LaunchTime']
                    })
            
            return instances
            
        except ClientError as e:
            print(f"Erro ao listar instâncias: {e}")
            return []


# Exemplo de uso
if __name__ == "__main__":
    # Inicializa o gerenciador
    ec2_manager = EC2Manager(region_name='us-east-1')
    
    # Exemplo 1: Criar uma instância simples
    print("\n=== Exemplo 1: Criar Instância ===")
    instance_id = ec2_manager.create_instance(
        ami_id='ami-0c55b159cbfafe1f0',  # Amazon Linux 2 AMI
        instance_type='t2.micro',  # Free tier eligible
        tags={
            'Name': 'Exemplo-Certificacao',
            'Environment': 'Development',
            'Purpose': 'Learning'
        }
    )
    
    # Exemplo 2: Obter informações da instância
    print("\n=== Exemplo 2: Informações da Instância ===")
    info = ec2_manager.get_instance_info(instance_id)
    for key, value in info.items():
        print(f"{key}: {value}")
    
    # Exemplo 3: Listar todas as instâncias em execução
    print("\n=== Exemplo 3: Listar Instâncias Running ===")
    running_instances = ec2_manager.list_instances(
        filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    for instance in running_instances:
        print(f"ID: {instance['InstanceId']}, Type: {instance['InstanceType']}, State: {instance['State']}")
    
    # Exemplo 4: Parar a instância
    print("\n=== Exemplo 4: Parar Instância ===")
    ec2_manager.stop_instance(instance_id)
    
    # Exemplo 5: Iniciar a instância novamente
    print("\n=== Exemplo 5: Iniciar Instância ===")
    ec2_manager.start_instance(instance_id)
    
    # CUIDADO: Descomente apenas se quiser deletar a instância
    # print("\n=== Exemplo 6: Terminar Instância ===")
    # ec2_manager.terminate_instance(instance_id)
