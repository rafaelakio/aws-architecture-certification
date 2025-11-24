"""
IAM (Identity and Access Management) - Exemplo Completo
Conceitos críticos de segurança para certificação AWS
"""

import boto3
import json
from typing import Dict, List
from botocore.exceptions import ClientError

class IAMManager:
    """
    Gerenciador de IAM
    Demonstra conceitos essenciais de segurança AWS
    """
    
    def __init__(self):
        """Inicializa cliente IAM"""
        # IAM é um serviço global (não regional)
        self.iam_client = boto3.client('iam')
        self.iam_resource = boto3.resource('iam')
    
    def create_user(
        self,
        username: str,
        tags: List[Dict[str, str]] = None
    ) -> str:
        """
        Cria usuário IAM
        
        IAM User:
        - Identidade permanente com credenciais de longo prazo
        - Pode ter senha (console) e/ou access keys (API/CLI)
        - Máximo 2 access keys por usuário
        - Deve seguir princípio do menor privilégio
        
        Args:
            username: Nome do usuário
            tags: Tags para organização
        
        Returns:
            user_arn: ARN do usuário criado
        """
        try:
            # Cria usuário
            response = self.iam_client.create_user(
                UserName=username,
                Tags=tags or []
            )
            
            user_arn = response['User']['Arn']
            print(f"Usuário criado: {username}")
            print(f"ARN: {user_arn}")
            
            return user_arn
            
        except ClientError as e:
            print(f"Erro ao criar usuário: {e}")
            raise
    
    def create_access_key(self, username: str) -> Dict[str, str]:
        """
        Cria access key para usuário
        
        Access Key:
        - Credenciais para acesso programático (API/CLI/SDK)
        - Composta por Access Key ID e Secret Access Key
        - Secret só é mostrada uma vez na criação
        - Deve ser rotacionada regularmente (90 dias recomendado)
        
        Args:
            username: Nome do usuário
        
        Returns:
            Dict com AccessKeyId e SecretAccessKey
        """
        try:
            response = self.iam_client.create_access_key(
                UserName=username
            )
            
            access_key = response['AccessKey']
            
            print(f"Access Key criada para {username}")
            print(f"Access Key ID: {access_key['AccessKeyId']}")
            print("⚠️  IMPORTANTE: Guarde o Secret Access Key em local seguro!")
            
            return {
                'AccessKeyId': access_key['AccessKeyId'],
                'SecretAccessKey': access_key['SecretAccessKey']
            }
            
        except ClientError as e:
            print(f"Erro ao criar access key: {e}")
            raise
    
    def create_group(
        self,
        group_name: str,
        path: str = '/'
    ) -> str:
        """
        Cria grupo IAM
        
        IAM Group:
        - Coleção de usuários
        - Facilita gerenciamento de permissões
        - Usuários herdam permissões do grupo
        - Um usuário pode estar em múltiplos grupos
        - Grupos não podem conter outros grupos
        
        Args:
            group_name: Nome do grupo
            path: Caminho organizacional (ex: /developers/)
        
        Returns:
            group_arn: ARN do grupo
        """
        try:
            response = self.iam_client.create_group(
                GroupName=group_name,
                Path=path
            )
            
            group_arn = response['Group']['Arn']
            print(f"Grupo criado: {group_name}")
            print(f"ARN: {group_arn}")
            
            return group_arn
            
        except ClientError as e:
            print(f"Erro ao criar grupo: {e}")
            raise
    
    def add_user_to_group(
        self,
        username: str,
        group_name: str
    ) -> bool:
        """
        Adiciona usuário a um grupo
        
        Args:
            username: Nome do usuário
            group_name: Nome do grupo
        
        Returns:
            bool: True se sucesso
        """
        try:
            self.iam_client.add_user_to_group(
                UserName=username,
                GroupName=group_name
            )
            
            print(f"Usuário {username} adicionado ao grupo {group_name}")
            return True
            
        except ClientError as e:
            print(f"Erro ao adicionar usuário ao grupo: {e}")
            return False
    
    def create_policy(
        self,
        policy_name: str,
        policy_document: Dict,
        description: str = ''
    ) -> str:
        """
        Cria política IAM customizada
        
        IAM Policy:
        - Documento JSON que define permissões
        - Pode ser anexada a users, groups ou roles
        - Tipos: AWS Managed, Customer Managed, Inline
        - Avaliação: Explicit Deny > Explicit Allow > Implicit Deny
        
        Policy Structure:
        - Version: Versão da linguagem de política (2012-10-17)
        - Statement: Lista de declarações
          - Effect: Allow ou Deny
          - Action: Ações permitidas/negadas
          - Resource: Recursos afetados
          - Condition: Condições opcionais
        
        Args:
            policy_name: Nome da política
            policy_document: Documento JSON da política
            description: Descrição da política
        
        Returns:
            policy_arn: ARN da política
        """
        try:
            # Converte dict para JSON string
            policy_json = json.dumps(policy_document)
            
            # Cria política
            response = self.iam_client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=policy_json,
                Description=description
            )
            
            policy_arn = response['Policy']['Arn']
            print(f"Política criada: {policy_name}")
            print(f"ARN: {policy_arn}")
            
            return policy_arn
            
        except ClientError as e:
            print(f"Erro ao criar política: {e}")
            raise
    
    def attach_policy_to_user(
        self,
        username: str,
        policy_arn: str
    ) -> bool:
        """
        Anexa política a um usuário
        
        Args:
            username: Nome do usuário
            policy_arn: ARN da política
        
        Returns:
            bool: True se sucesso
        """
        try:
            self.iam_client.attach_user_policy(
                UserName=username,
                PolicyArn=policy_arn
            )
            
            print(f"Política {policy_arn} anexada ao usuário {username}")
            return True
            
        except ClientError as e:
            print(f"Erro ao anexar política: {e}")
            return False
    
    def attach_policy_to_group(
        self,
        group_name: str,
        policy_arn: str
    ) -> bool:
        """
        Anexa política a um grupo
        
        Args:
            group_name: Nome do grupo
            policy_arn: ARN da política
        
        Returns:
            bool: True se sucesso
        """
        try:
            self.iam_client.attach_group_policy(
                GroupName=group_name,
                PolicyArn=policy_arn
            )
            
            print(f"Política {policy_arn} anexada ao grupo {group_name}")
            return True
            
        except ClientError as e:
            print(f"Erro ao anexar política ao grupo: {e}")
            return False
    
    def create_role(
        self,
        role_name: str,
        assume_role_policy: Dict,
        description: str = '',
        tags: List[Dict[str, str]] = None
    ) -> str:
        """
        Cria role IAM
        
        IAM Role:
        - Identidade com permissões temporárias
        - Pode ser assumida por users, services ou accounts
        - Não tem credenciais permanentes
        - Usa STS (Security Token Service) para credenciais temporárias
        - Casos de uso: EC2, Lambda, Cross-account access
        
        Trust Policy (Assume Role Policy):
        - Define quem pode assumir a role
        - Principal pode ser: AWS service, AWS account, Federated user
        
        Args:
            role_name: Nome da role
            assume_role_policy: Trust policy (quem pode assumir)
            description: Descrição da role
            tags: Tags para organização
        
        Returns:
            role_arn: ARN da role
        """
        try:
            # Converte dict para JSON string
            policy_json = json.dumps(assume_role_policy)
            
            # Cria role
            response = self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=policy_json,
                Description=description,
                Tags=tags or []
            )
            
            role_arn = response['Role']['Arn']
            print(f"Role criada: {role_name}")
            print(f"ARN: {role_arn}")
            
            return role_arn
            
        except ClientError as e:
            print(f"Erro ao criar role: {e}")
            raise
    
    def attach_policy_to_role(
        self,
        role_name: str,
        policy_arn: str
    ) -> bool:
        """
        Anexa política a uma role
        
        Args:
            role_name: Nome da role
            policy_arn: ARN da política
        
        Returns:
            bool: True se sucesso
        """
        try:
            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            
            print(f"Política {policy_arn} anexada à role {role_name}")
            return True
            
        except ClientError as e:
            print(f"Erro ao anexar política à role: {e}")
            return False


# Exemplos de políticas comuns
def get_s3_read_only_policy() -> Dict:
    """
    Política para acesso read-only ao S3
    
    Permite:
    - Listar buckets
    - Listar objetos
    - Baixar objetos
    
    Nega:
    - Upload
    - Deleção
    - Modificação de configurações
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion",
                    "s3:ListBucket",
                    "s3:ListBucketVersions"
                ],
                "Resource": [
                    "arn:aws:s3:::*"
                ]
            }
        ]
    }


def get_ec2_start_stop_policy() -> Dict:
    """
    Política para iniciar/parar instâncias EC2
    
    Permite:
    - Descrever instâncias
    - Iniciar instâncias
    - Parar instâncias
    
    Nega:
    - Criar instâncias
    - Terminar instâncias
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:DescribeInstances",
                    "ec2:DescribeInstanceStatus",
                    "ec2:StartInstances",
                    "ec2:StopInstances"
                ],
                "Resource": "*"
            }
        ]
    }


def get_lambda_execution_role_policy() -> Dict:
    """
    Trust policy para Lambda assumir role
    
    Permite que o serviço Lambda assuma esta role
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }


def get_ec2_instance_role_policy() -> Dict:
    """
    Trust policy para EC2 assumir role
    
    Permite que instâncias EC2 assumam esta role
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }


def get_cross_account_role_policy(trusted_account_id: str) -> Dict:
    """
    Trust policy para acesso cross-account
    
    Permite que outra conta AWS assuma esta role
    
    Args:
        trusted_account_id: ID da conta confiável
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{trusted_account_id}:root"
                },
                "Action": "sts:AssumeRole",
                "Condition": {
                    "StringEquals": {
                        "sts:ExternalId": "unique-external-id-123"
                    }
                }
            }
        ]
    }


def get_policy_with_conditions() -> Dict:
    """
    Política com condições avançadas
    
    Demonstra uso de conditions para controle granular:
    - Restrição por IP
    - Restrição por horário
    - Restrição por MFA
    - Restrição por tags
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": "*",
                "Condition": {
                    # Requer MFA
                    "Bool": {
                        "aws:MultiFactorAuthPresent": "true"
                    },
                    # Apenas de IPs específicos
                    "IpAddress": {
                        "aws:SourceIp": [
                            "203.0.113.0/24",
                            "198.51.100.0/24"
                        ]
                    },
                    # Apenas em horário comercial
                    "DateGreaterThan": {
                        "aws:CurrentTime": "2024-01-01T00:00:00Z"
                    },
                    "DateLessThan": {
                        "aws:CurrentTime": "2024-12-31T23:59:59Z"
                    }
                }
            }
        ]
    }


# Exemplo de uso completo
if __name__ == "__main__":
    iam_manager = IAMManager()
    
    print("\n=== Exemplo 1: Criar Usuário e Access Key ===")
    username = "developer-user"
    iam_manager.create_user(
        username=username,
        tags=[
            {'Key': 'Department', 'Value': 'Engineering'},
            {'Key': 'Environment', 'Value': 'Development'}
        ]
    )
    
    # Cria access key
    credentials = iam_manager.create_access_key(username)
    print(f"Access Key ID: {credentials['AccessKeyId']}")
    
    print("\n=== Exemplo 2: Criar Grupo e Adicionar Usuário ===")
    group_name = "developers"
    iam_manager.create_group(group_name=group_name)
    iam_manager.add_user_to_group(username, group_name)
    
    print("\n=== Exemplo 3: Criar Política Customizada ===")
    policy_name = "S3ReadOnlyPolicy"
    policy_arn = iam_manager.create_policy(
        policy_name=policy_name,
        policy_document=get_s3_read_only_policy(),
        description="Permite acesso read-only ao S3"
    )
    
    print("\n=== Exemplo 4: Anexar Política ao Grupo ===")
    iam_manager.attach_policy_to_group(group_name, policy_arn)
    
    print("\n=== Exemplo 5: Criar Role para Lambda ===")
    role_name = "LambdaExecutionRole"
    role_arn = iam_manager.create_role(
        role_name=role_name,
        assume_role_policy=get_lambda_execution_role_policy(),
        description="Role para execução de funções Lambda",
        tags=[
            {'Key': 'Service', 'Value': 'Lambda'},
            {'Key': 'Environment', 'Value': 'Production'}
        ]
    )
    
    # Anexa política AWS managed para Lambda
    iam_manager.attach_policy_to_role(
        role_name,
        'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    )
    
    print("\n=== Exemplo 6: Criar Role para EC2 ===")
    ec2_role_name = "EC2S3AccessRole"
    ec2_role_arn = iam_manager.create_role(
        role_name=ec2_role_name,
        assume_role_policy=get_ec2_instance_role_policy(),
        description="Role para instâncias EC2 acessarem S3"
    )
    
    # Anexa política S3 read-only
    iam_manager.attach_policy_to_role(ec2_role_name, policy_arn)
    
    print("\n✅ Configuração IAM concluída!")
    print("\n⚠️  IMPORTANTE:")
    print("- Sempre siga o princípio do menor privilégio")
    print("- Habilite MFA para usuários com acesso ao console")
    print("- Rotacione access keys regularmente")
    print("- Use roles ao invés de access keys quando possível")
    print("- Monitore atividades com CloudTrail")
