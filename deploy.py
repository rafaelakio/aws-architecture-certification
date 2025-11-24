#!/usr/bin/env python3
"""
Script de Deploy - AWS Architecture Certification
Facilita o deploy dos exemplos práticos
"""

import boto3
import sys
import argparse
from typing import Dict, List
import json
import time

class AWSDeployer:
    """
    Classe para facilitar deploy de recursos AWS
    """
    
    def __init__(self, region: str = 'us-east-1', profile: str = None):
        """
        Inicializa deployer
        
        Args:
            region: Região AWS
            profile: Profile AWS CLI (opcional)
        """
        session_params = {'region_name': region}
        if profile:
            session_params['profile_name'] = profile
        
        self.session = boto3.Session(**session_params)
        self.region = region
        
        # Clientes AWS
        self.cf_client = self.session.client('cloudformation')
        self.ec2_client = self.session.client('ec2')
        self.s3_client = self.session.client('s3')
        
        print(f"✅ AWS Deployer inicializado")
        print(f"   Região: {region}")
        print(f"   Profile: {profile or 'default'}")
    
    def validate_credentials(self) -> bool:
        """
        Valida credenciais AWS
        
        Returns:
            bool: True se credenciais válidas
        """
        try:
            sts = self.session.client('sts')
            identity = sts.get_caller_identity()
            
            print(f"\n✅ Credenciais válidas")
            print(f"   Account ID: {identity['Account']}")
            print(f"   User ARN: {identity['Arn']}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Erro ao validar credenciais: {e}")
            print("\nConfigure suas credenciais AWS:")
            print("  aws configure")
            return False
    
    def deploy_cloudformation_stack(
        self,
        stack_name: str,
        template_file: str,
        parameters: Dict[str, str] = None
    ) -> bool:
        """
        Faz deploy de stack CloudFormation
        
        Args:
            stack_name: Nome da stack
            template_file: Caminho do template
            parameters: Parâmetros do template
        
        Returns:
            bool: True se sucesso
        """
        try:
            print(f"\n📦 Fazendo deploy da stack: {stack_name}")
            
            # Lê template
            with open(template_file, 'r') as f:
                template_body = f.read()
            
            # Prepara parâmetros
            cf_parameters = []
            if parameters:
                cf_parameters = [
                    {'ParameterKey': k, 'ParameterValue': v}
                    for k, v in parameters.items()
                ]
            
            # Verifica se stack existe
            try:
                self.cf_client.describe_stacks(StackName=stack_name)
                stack_exists = True
            except:
                stack_exists = False
            
            # Cria ou atualiza stack
            if stack_exists:
                print(f"   Stack existe, atualizando...")
                self.cf_client.update_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Parameters=cf_parameters,
                    Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM']
                )
                waiter = self.cf_client.get_waiter('stack_update_complete')
            else:
                print(f"   Criando nova stack...")
                self.cf_client.create_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Parameters=cf_parameters,
                    Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM']
                )
                waiter = self.cf_client.get_waiter('stack_create_complete')
            
            # Aguarda conclusão
            print(f"   Aguardando conclusão (isso pode levar alguns minutos)...")
            waiter.wait(StackName=stack_name)
            
            # Obtém outputs
            response = self.cf_client.describe_stacks(StackName=stack_name)
            stack = response['Stacks'][0]
            
            print(f"\n✅ Stack {stack_name} criada com sucesso!")
            
            if 'Outputs' in stack:
                print(f"\n📋 Outputs:")
                for output in stack['Outputs']:
                    print(f"   {output['OutputKey']}: {output['OutputValue']}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Erro ao fazer deploy: {e}")
            return False
    
    def delete_cloudformation_stack(self, stack_name: str) -> bool:
        """
        Deleta stack CloudFormation
        
        Args:
            stack_name: Nome da stack
        
        Returns:
            bool: True se sucesso
        """
        try:
            print(f"\n🗑️  Deletando stack: {stack_name}")
            
            self.cf_client.delete_stack(StackName=stack_name)
            
            print(f"   Aguardando deleção...")
            waiter = self.cf_client.get_waiter('stack_delete_complete')
            waiter.wait(StackName=stack_name)
            
            print(f"\n✅ Stack {stack_name} deletada com sucesso!")
            return True
            
        except Exception as e:
            print(f"\n❌ Erro ao deletar stack: {e}")
            return False
    
    def list_stacks(self) -> List[Dict]:
        """
        Lista todas as stacks CloudFormation
        
        Returns:
            Lista de stacks
        """
        try:
            response = self.cf_client.list_stacks(
                StackStatusFilter=[
                    'CREATE_COMPLETE',
                    'UPDATE_COMPLETE',
                    'ROLLBACK_COMPLETE'
                ]
            )
            
            stacks = response['StackSummaries']
            
            if stacks:
                print(f"\n📚 Stacks CloudFormation:")
                for stack in stacks:
                    print(f"   - {stack['StackName']} ({stack['StackStatus']})")
            else:
                print(f"\n📚 Nenhuma stack encontrada")
            
            return stacks
            
        except Exception as e:
            print(f"\n❌ Erro ao listar stacks: {e}")
            return []
    
    def estimate_costs(self, template_file: str) -> None:
        """
        Estima custos do template (informativo)
        
        Args:
            template_file: Caminho do template
        """
        print(f"\n💰 Estimativa de Custos")
        print(f"   Template: {template_file}")
        print(f"\n   ⚠️  Custos variam baseado em:")
        print(f"   - Região AWS")
        print(f"   - Tipo de instâncias")
        print(f"   - Tráfego de rede")
        print(f"   - Armazenamento")
        print(f"\n   Use AWS Pricing Calculator para estimativa precisa:")
        print(f"   https://calculator.aws/")


def main():
    """
    Função principal
    """
    parser = argparse.ArgumentParser(
        description='Deploy de recursos AWS para certificação'
    )
    
    parser.add_argument(
        'action',
        choices=['deploy', 'delete', 'list', 'validate', 'estimate'],
        help='Ação a executar'
    )
    
    parser.add_argument(
        '--stack-name',
        help='Nome da stack CloudFormation'
    )
    
    parser.add_argument(
        '--template',
        help='Caminho do template CloudFormation'
    )
    
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='Região AWS (default: us-east-1)'
    )
    
    parser.add_argument(
        '--profile',
        help='Profile AWS CLI'
    )
    
    parser.add_argument(
        '--param',
        action='append',
        help='Parâmetro do template (formato: Key=Value)'
    )
    
    args = parser.parse_args()
    
    # Inicializa deployer
    deployer = AWSDeployer(region=args.region, profile=args.profile)
    
    # Executa ação
    if args.action == 'validate':
        if not deployer.validate_credentials():
            sys.exit(1)
    
    elif args.action == 'list':
        deployer.list_stacks()
    
    elif args.action == 'estimate':
        if not args.template:
            print("❌ --template é obrigatório para estimate")
            sys.exit(1)
        deployer.estimate_costs(args.template)
    
    elif args.action == 'deploy':
        if not args.stack_name or not args.template:
            print("❌ --stack-name e --template são obrigatórios para deploy")
            sys.exit(1)
        
        # Valida credenciais
        if not deployer.validate_credentials():
            sys.exit(1)
        
        # Processa parâmetros
        parameters = {}
        if args.param:
            for param in args.param:
                key, value = param.split('=', 1)
                parameters[key] = value
        
        # Faz deploy
        success = deployer.deploy_cloudformation_stack(
            stack_name=args.stack_name,
            template_file=args.template,
            parameters=parameters
        )
        
        if not success:
            sys.exit(1)
    
    elif args.action == 'delete':
        if not args.stack_name:
            print("❌ --stack-name é obrigatório para delete")
            sys.exit(1)
        
        # Confirma deleção
        confirm = input(f"\n⚠️  Tem certeza que deseja deletar {args.stack_name}? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Operação cancelada")
            sys.exit(0)
        
        # Deleta stack
        success = deployer.delete_cloudformation_stack(args.stack_name)
        
        if not success:
            sys.exit(1)
    
    print(f"\n✅ Operação concluída com sucesso!")


if __name__ == "__main__":
    main()
