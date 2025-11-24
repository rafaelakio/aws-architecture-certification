"""
S3 (Simple Storage Service) - Exemplo Completo
Demonstra operações essenciais do S3 para certificação AWS
"""

import boto3
import json
from typing import List, Dict, Optional
from botocore.exceptions import ClientError
import os
from datetime import datetime, timedelta

class S3Manager:
    """
    Gerenciador de operações S3
    Cobre os principais conceitos cobrados na certificação
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Inicializa cliente S3
        
        Args:
            region_name: Região AWS
        """
        # Cliente S3 para operações de baixo nível
        self.s3_client = boto3.client('s3', region_name=region_name)
        
        # Resource S3 para operações de alto nível (orientado a objetos)
        self.s3_resource = boto3.resource('s3', region_name=region_name)
        
        self.region = region_name
    
    def create_bucket(
        self,
        bucket_name: str,
        enable_versioning: bool = False,
        enable_encryption: bool = True,
        block_public_access: bool = True
    ) -> bool:
        """
        Cria um bucket S3 com configurações de segurança
        
        Conceitos importantes:
        - Bucket names são globalmente únicos
        - Buckets são regionais mas nomes são globais
        - Versioning permite recuperar versões anteriores
        - Encryption protege dados em repouso
        - Block Public Access previne exposição acidental
        
        Args:
            bucket_name: Nome único do bucket (DNS-compliant)
            enable_versioning: Habilita versionamento de objetos
            enable_encryption: Habilita criptografia padrão (SSE-S3)
            block_public_access: Bloqueia acesso público
        
        Returns:
            bool: True se sucesso
        """
        try:
            # Cria o bucket
            # LocationConstraint é necessário para regiões diferentes de us-east-1
            if self.region == 'us-east-1':
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': self.region
                    }
                )
            
            print(f"Bucket {bucket_name} criado com sucesso!")
            
            # Habilita versionamento se solicitado
            # Versioning protege contra deleções acidentais
            # Permite recuperar versões anteriores de objetos
            if enable_versioning:
                self.s3_client.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
                print(f"Versionamento habilitado para {bucket_name}")
            
            # Habilita criptografia padrão
            # SSE-S3: Server-Side Encryption com chaves gerenciadas pela AWS
            # Alternativas: SSE-KMS (mais controle), SSE-C (cliente gerencia chaves)
            if enable_encryption:
                self.s3_client.put_bucket_encryption(
                    Bucket=bucket_name,
                    ServerSideEncryptionConfiguration={
                        'Rules': [{
                            'ApplyServerSideEncryptionByDefault': {
                                'SSEAlgorithm': 'AES256'  # SSE-S3
                            },
                            'BucketKeyEnabled': True  # Reduz custos de KMS
                        }]
                    }
                )
                print(f"Criptografia habilitada para {bucket_name}")
            
            # Bloqueia acesso público
            # Importante: previne exposição acidental de dados sensíveis
            if block_public_access:
                self.s3_client.put_public_access_block(
                    Bucket=bucket_name,
                    PublicAccessBlockConfiguration={
                        'BlockPublicAcls': True,
                        'IgnorePublicAcls': True,
                        'BlockPublicPolicy': True,
                        'RestrictPublicBuckets': True
                    }
                )
                print(f"Acesso público bloqueado para {bucket_name}")
            
            return True
            
        except ClientError as e:
            print(f"Erro ao criar bucket: {e}")
            return False
    
    def upload_file(
        self,
        file_path: str,
        bucket_name: str,
        object_key: str = None,
        metadata: Dict[str, str] = None,
        storage_class: str = 'STANDARD'
    ) -> bool:
        """
        Faz upload de arquivo para S3
        
        Storage Classes (importante para certificação):
        - STANDARD: Acesso frequente, alta durabilidade
        - INTELLIGENT_TIERING: Move automaticamente entre tiers
        - STANDARD_IA: Acesso infrequente, menor custo
        - ONEZONE_IA: Uma AZ apenas, mais barato
        - GLACIER: Arquivamento, retrieval em minutos/horas
        - GLACIER_DEEP_ARCHIVE: Arquivamento longo prazo, retrieval em 12h
        
        Args:
            file_path: Caminho local do arquivo
            bucket_name: Nome do bucket destino
            object_key: Chave do objeto no S3 (se None, usa nome do arquivo)
            metadata: Metadados customizados
            storage_class: Classe de armazenamento
        
        Returns:
            bool: True se sucesso
        """
        try:
            # Se object_key não fornecido, usa nome do arquivo
            if object_key is None:
                object_key = os.path.basename(file_path)
            
            # Prepara parâmetros extras
            extra_args = {
                'StorageClass': storage_class
            }
            
            # Adiciona metadados se fornecidos
            # Metadados são úteis para classificação e busca
            if metadata:
                extra_args['Metadata'] = metadata
            
            # Upload do arquivo
            # upload_file é um método de alto nível que:
            # - Faz multipart upload automaticamente para arquivos grandes
            # - Gerencia retries automaticamente
            # - É mais eficiente que put_object para arquivos grandes
            self.s3_client.upload_file(
                Filename=file_path,
                Bucket=bucket_name,
                Key=object_key,
                ExtraArgs=extra_args
            )
            
            print(f"Arquivo {file_path} enviado para s3://{bucket_name}/{object_key}")
            print(f"Storage Class: {storage_class}")
            
            return True
            
        except ClientError as e:
            print(f"Erro ao fazer upload: {e}")
            return False
    
    def download_file(
        self,
        bucket_name: str,
        object_key: str,
        local_path: str
    ) -> bool:
        """
        Baixa arquivo do S3
        
        Args:
            bucket_name: Nome do bucket
            object_key: Chave do objeto
            local_path: Caminho local para salvar
        
        Returns:
            bool: True se sucesso
        """
        try:
            # download_file é método de alto nível
            # Gerencia multipart download automaticamente
            self.s3_client.download_file(
                Bucket=bucket_name,
                Key=object_key,
                Filename=local_path
            )
            
            print(f"Arquivo s3://{bucket_name}/{object_key} baixado para {local_path}")
            return True
            
        except ClientError as e:
            print(f"Erro ao baixar arquivo: {e}")
            return False
    
    def list_objects(
        self,
        bucket_name: str,
        prefix: str = '',
        max_keys: int = 1000
    ) -> List[Dict]:
        """
        Lista objetos em um bucket
        
        Args:
            bucket_name: Nome do bucket
            prefix: Prefixo para filtrar objetos (como "pasta/")
            max_keys: Número máximo de objetos a retornar
        
        Returns:
            Lista de dicionários com informações dos objetos
        """
        try:
            # list_objects_v2 é a versão recomendada (v1 é legacy)
            response = self.s3_client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            objects = []
            
            # Verifica se há objetos
            if 'Contents' in response:
                for obj in response['Contents']:
                    objects.append({
                        'Key': obj['Key'],
                        'Size': obj['Size'],  # Tamanho em bytes
                        'LastModified': obj['LastModified'],
                        'StorageClass': obj.get('StorageClass', 'STANDARD'),
                        'ETag': obj['ETag']  # Hash MD5 do objeto
                    })
            
            print(f"Encontrados {len(objects)} objetos em {bucket_name}")
            return objects
            
        except ClientError as e:
            print(f"Erro ao listar objetos: {e}")
            return []
    
    def delete_object(
        self,
        bucket_name: str,
        object_key: str,
        version_id: str = None
    ) -> bool:
        """
        Deleta objeto do S3
        
        Importante: Se versioning está habilitado, cria delete marker
        Para deletar permanentemente, precisa especificar version_id
        
        Args:
            bucket_name: Nome do bucket
            object_key: Chave do objeto
            version_id: ID da versão (para buckets com versioning)
        
        Returns:
            bool: True se sucesso
        """
        try:
            params = {
                'Bucket': bucket_name,
                'Key': object_key
            }
            
            # Se version_id fornecido, deleta versão específica
            if version_id:
                params['VersionId'] = version_id
            
            self.s3_client.delete_object(**params)
            
            print(f"Objeto s3://{bucket_name}/{object_key} deletado")
            return True
            
        except ClientError as e:
            print(f"Erro ao deletar objeto: {e}")
            return False
    
    def generate_presigned_url(
        self,
        bucket_name: str,
        object_key: str,
        expiration: int = 3600,
        http_method: str = 'get_object'
    ) -> Optional[str]:
        """
        Gera URL pré-assinada para acesso temporário
        
        Conceito importante: Permite acesso temporário sem credenciais AWS
        Casos de uso:
        - Download temporário de arquivos privados
        - Upload direto do cliente para S3
        - Compartilhamento seguro de arquivos
        
        Args:
            bucket_name: Nome do bucket
            object_key: Chave do objeto
            expiration: Tempo de expiração em segundos (máx 7 dias)
            http_method: Método HTTP (get_object, put_object, etc)
        
        Returns:
            URL pré-assinada ou None se erro
        """
        try:
            # generate_presigned_url cria URL temporária
            # URL contém credenciais temporárias na query string
            url = self.s3_client.generate_presigned_url(
                ClientMethod=http_method,
                Params={
                    'Bucket': bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration
            )
            
            print(f"URL pré-assinada gerada (expira em {expiration}s)")
            return url
            
        except ClientError as e:
            print(f"Erro ao gerar URL pré-assinada: {e}")
            return None
    
    def enable_lifecycle_policy(
        self,
        bucket_name: str
    ) -> bool:
        """
        Configura política de lifecycle para otimizar custos
        
        Lifecycle Policies (importante para certificação):
        - Transição automática entre storage classes
        - Deleção automática de objetos antigos
        - Limpeza de uploads incompletos
        - Gerenciamento de versões antigas
        
        Args:
            bucket_name: Nome do bucket
        
        Returns:
            bool: True se sucesso
        """
        try:
            # Define regras de lifecycle
            lifecycle_config = {
                'Rules': [
                    {
                        'Id': 'Move-to-IA-after-30-days',
                        'Status': 'Enabled',
                        'Filter': {'Prefix': ''},  # Aplica a todos objetos
                        'Transitions': [
                            {
                                # Move para STANDARD_IA após 30 dias
                                'Days': 30,
                                'StorageClass': 'STANDARD_IA'
                            },
                            {
                                # Move para GLACIER após 90 dias
                                'Days': 90,
                                'StorageClass': 'GLACIER'
                            }
                        ]
                    },
                    {
                        'Id': 'Delete-old-versions',
                        'Status': 'Enabled',
                        'Filter': {'Prefix': ''},
                        'NoncurrentVersionExpiration': {
                            # Deleta versões antigas após 90 dias
                            'NoncurrentDays': 90
                        }
                    },
                    {
                        'Id': 'Clean-incomplete-uploads',
                        'Status': 'Enabled',
                        'Filter': {'Prefix': ''},
                        'AbortIncompleteMultipartUpload': {
                            # Remove uploads incompletos após 7 dias
                            'DaysAfterInitiation': 7
                        }
                    }
                ]
            }
            
            # Aplica configuração de lifecycle
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration=lifecycle_config
            )
            
            print(f"Lifecycle policy configurada para {bucket_name}")
            return True
            
        except ClientError as e:
            print(f"Erro ao configurar lifecycle: {e}")
            return False
    
    def enable_replication(
        self,
        source_bucket: str,
        destination_bucket: str,
        iam_role_arn: str
    ) -> bool:
        """
        Configura replicação entre buckets (CRR ou SRR)
        
        Tipos de replicação:
        - CRR (Cross-Region Replication): Entre regiões diferentes
        - SRR (Same-Region Replication): Mesma região
        
        Requisitos:
        - Versioning habilitado em ambos buckets
        - IAM role com permissões adequadas
        
        Casos de uso:
        - Disaster Recovery
        - Compliance (dados em múltiplas regiões)
        - Redução de latência
        
        Args:
            source_bucket: Bucket origem
            destination_bucket: Bucket destino
            iam_role_arn: ARN da role IAM para replicação
        
        Returns:
            bool: True se sucesso
        """
        try:
            # Configuração de replicação
            replication_config = {
                'Role': iam_role_arn,
                'Rules': [
                    {
                        'ID': 'ReplicateAll',
                        'Status': 'Enabled',
                        'Priority': 1,
                        'Filter': {'Prefix': ''},  # Replica todos objetos
                        'Destination': {
                            'Bucket': f'arn:aws:s3:::{destination_bucket}',
                            'ReplicationTime': {
                                'Status': 'Enabled',
                                'Time': {
                                    'Minutes': 15  # S3 RTC (Replication Time Control)
                                }
                            },
                            'Metrics': {
                                'Status': 'Enabled',
                                'EventThreshold': {
                                    'Minutes': 15
                                }
                            }
                        },
                        'DeleteMarkerReplication': {
                            'Status': 'Enabled'  # Replica delete markers
                        }
                    }
                ]
            }
            
            # Aplica configuração de replicação
            self.s3_client.put_bucket_replication(
                Bucket=source_bucket,
                ReplicationConfiguration=replication_config
            )
            
            print(f"Replicação configurada: {source_bucket} -> {destination_bucket}")
            return True
            
        except ClientError as e:
            print(f"Erro ao configurar replicação: {e}")
            return False


# Exemplo de uso
if __name__ == "__main__":
    # Inicializa gerenciador
    s3_manager = S3Manager(region_name='us-east-1')
    
    # Nome do bucket (deve ser único globalmente)
    bucket_name = f"exemplo-certificacao-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Exemplo 1: Criar bucket com segurança
    print("\n=== Exemplo 1: Criar Bucket ===")
    s3_manager.create_bucket(
        bucket_name=bucket_name,
        enable_versioning=True,
        enable_encryption=True,
        block_public_access=True
    )
    
    # Exemplo 2: Upload de arquivo
    print("\n=== Exemplo 2: Upload de Arquivo ===")
    # Cria arquivo de exemplo
    with open('exemplo.txt', 'w') as f:
        f.write('Conteúdo de exemplo para certificação AWS')
    
    s3_manager.upload_file(
        file_path='exemplo.txt',
        bucket_name=bucket_name,
        object_key='documentos/exemplo.txt',
        metadata={'author': 'AWS Student', 'category': 'certification'},
        storage_class='STANDARD'
    )
    
    # Exemplo 3: Listar objetos
    print("\n=== Exemplo 3: Listar Objetos ===")
    objects = s3_manager.list_objects(bucket_name)
    for obj in objects:
        print(f"- {obj['Key']} ({obj['Size']} bytes)")
    
    # Exemplo 4: Gerar URL pré-assinada
    print("\n=== Exemplo 4: URL Pré-assinada ===")
    url = s3_manager.generate_presigned_url(
        bucket_name=bucket_name,
        object_key='documentos/exemplo.txt',
        expiration=3600  # 1 hora
    )
    print(f"URL: {url}")
    
    # Exemplo 5: Configurar Lifecycle
    print("\n=== Exemplo 5: Lifecycle Policy ===")
    s3_manager.enable_lifecycle_policy(bucket_name)
    
    print("\n✅ Exemplos concluídos!")
    print(f"Bucket criado: {bucket_name}")
    print("Lembre-se de deletar o bucket após os testes para evitar custos!")
