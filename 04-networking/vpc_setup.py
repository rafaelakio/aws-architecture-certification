"""
VPC (Virtual Private Cloud) - Exemplo Completo
Conceitos essenciais de networking para certificação AWS
"""

import boto3
from typing import Dict, List, Optional
from botocore.exceptions import ClientError

class VPCManager:
    """
    Gerenciador de VPC e componentes de rede
    Cobre conceitos críticos para certificação
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Inicializa cliente EC2 (VPC é parte do EC2)
        
        Args:
            region_name: Região AWS
        """
        self.ec2_client = boto3.client('ec2', region_name=region_name)
        self.ec2_resource = boto3.resource('ec2', region_name=region_name)
        self.region = region_name
    
    def create_vpc(
        self,
        cidr_block: str = '10.0.0.0/16',
        enable_dns_hostnames: bool = True,
        enable_dns_support: bool = True,
        tags: Dict[str, str] = None
    ) -> str:
        """
        Cria uma VPC (Virtual Private Cloud)
        
        VPC Conceitos importantes:
        - CIDR Block: Range de IPs privados (RFC 1918)
        - Ranges comuns: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
        - DNS Hostnames: Permite nomes DNS para instâncias
        - DNS Support: Habilita resolução DNS na VPC
        
        Args:
            cidr_block: Bloco CIDR da VPC (ex: 10.0.0.0/16 = 65,536 IPs)
            enable_dns_hostnames: Habilita DNS hostnames
            enable_dns_support: Habilita suporte DNS
            tags: Tags para organização
        
        Returns:
            vpc_id: ID da VPC criada
        """
        try:
            # Cria a VPC
            # CIDR block define o range de IPs disponíveis
            # /16 = 65,536 IPs, /24 = 256 IPs, /28 = 16 IPs
            response = self.ec2_client.create_vpc(
                CidrBlock=cidr_block,
                # Tenancy: default (compartilhado) ou dedicated (hardware dedicado)
                InstanceTenancy='default'
            )
            
            vpc_id = response['Vpc']['VpcId']
            print(f"VPC criada: {vpc_id} com CIDR {cidr_block}")
            
            # Aguarda VPC estar disponível
            waiter = self.ec2_client.get_waiter('vpc_available')
            waiter.wait(VpcIds=[vpc_id])
            
            # Habilita DNS hostnames
            # Necessário para instâncias terem nomes DNS públicos
            if enable_dns_hostnames:
                self.ec2_client.modify_vpc_attribute(
                    VpcId=vpc_id,
                    EnableDnsHostnames={'Value': True}
                )
                print(f"DNS Hostnames habilitado para {vpc_id}")
            
            # Habilita DNS support
            # Permite resolução DNS dentro da VPC
            if enable_dns_support:
                self.ec2_client.modify_vpc_attribute(
                    VpcId=vpc_id,
                    EnableDnsSupport={'Value': True}
                )
                print(f"DNS Support habilitado para {vpc_id}")
            
            # Adiciona tags
            if tags:
                self.ec2_client.create_tags(
                    Resources=[vpc_id],
                    Tags=[{'Key': k, 'Value': v} for k, v in tags.items()]
                )
            
            return vpc_id
            
        except ClientError as e:
            print(f"Erro ao criar VPC: {e}")
            raise
    
    def create_subnet(
        self,
        vpc_id: str,
        cidr_block: str,
        availability_zone: str,
        is_public: bool = False,
        tags: Dict[str, str] = None
    ) -> str:
        """
        Cria uma subnet dentro da VPC
        
        Subnet Conceitos:
        - Subnet é um range de IPs dentro da VPC
        - Cada subnet está em uma única AZ (Availability Zone)
        - Public Subnet: Tem rota para Internet Gateway
        - Private Subnet: Não tem rota direta para internet
        - AWS reserva 5 IPs em cada subnet (primeiro 4 e último)
        
        Args:
            vpc_id: ID da VPC
            cidr_block: CIDR da subnet (deve estar dentro do CIDR da VPC)
            availability_zone: AZ onde criar a subnet (ex: us-east-1a)
            is_public: Se True, configura como subnet pública
            tags: Tags para organização
        
        Returns:
            subnet_id: ID da subnet criada
        """
        try:
            # Cria a subnet
            response = self.ec2_client.create_subnet(
                VpcId=vpc_id,
                CidrBlock=cidr_block,
                AvailabilityZone=availability_zone
            )
            
            subnet_id = response['Subnet']['SubnetId']
            print(f"Subnet criada: {subnet_id} em {availability_zone}")
            
            # Se subnet pública, habilita auto-assign de IP público
            # Instâncias lançadas nesta subnet receberão IP público automaticamente
            if is_public:
                self.ec2_client.modify_subnet_attribute(
                    SubnetId=subnet_id,
                    MapPublicIpOnLaunch={'Value': True}
                )
                print(f"Auto-assign IP público habilitado para {subnet_id}")
            
            # Adiciona tags
            if tags:
                self.ec2_client.create_tags(
                    Resources=[subnet_id],
                    Tags=[{'Key': k, 'Value': v} for k, v in tags.items()]
                )
            
            return subnet_id
            
        except ClientError as e:
            print(f"Erro ao criar subnet: {e}")
            raise
    
    def create_internet_gateway(
        self,
        vpc_id: str,
        tags: Dict[str, str] = None
    ) -> str:
        """
        Cria e anexa Internet Gateway à VPC
        
        Internet Gateway (IGW):
        - Permite comunicação entre VPC e internet
        - Necessário para subnets públicas
        - Horizontally scaled, redundante e highly available
        - Não causa gargalo de rede
        - Realiza NAT para instâncias com IP público
        
        Args:
            vpc_id: ID da VPC
            tags: Tags para organização
        
        Returns:
            igw_id: ID do Internet Gateway
        """
        try:
            # Cria Internet Gateway
            response = self.ec2_client.create_internet_gateway()
            igw_id = response['InternetGateway']['InternetGatewayId']
            print(f"Internet Gateway criado: {igw_id}")
            
            # Anexa IGW à VPC
            # Uma VPC pode ter apenas um IGW
            self.ec2_client.attach_internet_gateway(
                InternetGatewayId=igw_id,
                VpcId=vpc_id
            )
            print(f"Internet Gateway {igw_id} anexado à VPC {vpc_id}")
            
            # Adiciona tags
            if tags:
                self.ec2_client.create_tags(
                    Resources=[igw_id],
                    Tags=[{'Key': k, 'Value': v} for k, v in tags.items()]
                )
            
            return igw_id
            
        except ClientError as e:
            print(f"Erro ao criar Internet Gateway: {e}")
            raise
    
    def create_nat_gateway(
        self,
        subnet_id: str,
        tags: Dict[str, str] = None
    ) -> str:
        """
        Cria NAT Gateway para subnets privadas
        
        NAT Gateway:
        - Permite instâncias em subnets privadas acessarem internet
        - Não permite conexões iniciadas da internet
        - Managed service (AWS gerencia disponibilidade)
        - Criado em subnet pública
        - Requer Elastic IP
        - Alternativa: NAT Instance (EC2, você gerencia)
        
        Args:
            subnet_id: ID da subnet pública onde criar o NAT Gateway
            tags: Tags para organização
        
        Returns:
            nat_gateway_id: ID do NAT Gateway
        """
        try:
            # Aloca Elastic IP para o NAT Gateway
            # EIP é necessário para o NAT Gateway ter IP público fixo
            eip_response = self.ec2_client.allocate_address(
                Domain='vpc'  # EIP para VPC (não EC2-Classic)
            )
            allocation_id = eip_response['AllocationId']
            eip = eip_response['PublicIp']
            print(f"Elastic IP alocado: {eip}")
            
            # Cria NAT Gateway
            response = self.ec2_client.create_nat_gateway(
                SubnetId=subnet_id,
                AllocationId=allocation_id
            )
            
            nat_gateway_id = response['NatGateway']['NatGatewayId']
            print(f"NAT Gateway criado: {nat_gateway_id}")
            
            # Aguarda NAT Gateway estar disponível
            # Pode levar alguns minutos
            print("Aguardando NAT Gateway ficar disponível...")
            waiter = self.ec2_client.get_waiter('nat_gateway_available')
            waiter.wait(NatGatewayIds=[nat_gateway_id])
            
            # Adiciona tags
            if tags:
                self.ec2_client.create_tags(
                    Resources=[nat_gateway_id],
                    Tags=[{'Key': k, 'Value': v} for k, v in tags.items()]
                )
            
            return nat_gateway_id
            
        except ClientError as e:
            print(f"Erro ao criar NAT Gateway: {e}")
            raise
    
    def create_route_table(
        self,
        vpc_id: str,
        tags: Dict[str, str] = None
    ) -> str:
        """
        Cria Route Table
        
        Route Table:
        - Define rotas para tráfego de rede
        - Cada subnet deve estar associada a uma route table
        - VPC tem route table padrão (main route table)
        - Rotas determinam para onde o tráfego é direcionado
        
        Args:
            vpc_id: ID da VPC
            tags: Tags para organização
        
        Returns:
            route_table_id: ID da route table
        """
        try:
            # Cria route table
            response = self.ec2_client.create_route_table(VpcId=vpc_id)
            route_table_id = response['RouteTable']['RouteTableId']
            print(f"Route Table criada: {route_table_id}")
            
            # Adiciona tags
            if tags:
                self.ec2_client.create_tags(
                    Resources=[route_table_id],
                    Tags=[{'Key': k, 'Value': v} for k, v in tags.items()]
                )
            
            return route_table_id
            
        except ClientError as e:
            print(f"Erro ao criar Route Table: {e}")
            raise
    
    def add_route(
        self,
        route_table_id: str,
        destination_cidr: str,
        gateway_id: str = None,
        nat_gateway_id: str = None,
        instance_id: str = None
    ) -> bool:
        """
        Adiciona rota à route table
        
        Tipos de rotas comuns:
        - 0.0.0.0/0 -> IGW: Rota padrão para internet (subnet pública)
        - 0.0.0.0/0 -> NAT Gateway: Rota para internet via NAT (subnet privada)
        - 10.0.0.0/16 -> local: Rota local (automática)
        - Specific CIDR -> VPN/VPC Peering: Rotas customizadas
        
        Args:
            route_table_id: ID da route table
            destination_cidr: CIDR de destino (ex: 0.0.0.0/0 para internet)
            gateway_id: ID do Internet Gateway (para subnet pública)
            nat_gateway_id: ID do NAT Gateway (para subnet privada)
            instance_id: ID da instância (para rotas customizadas)
        
        Returns:
            bool: True se sucesso
        """
        try:
            params = {
                'RouteTableId': route_table_id,
                'DestinationCidrBlock': destination_cidr
            }
            
            # Adiciona target apropriado
            if gateway_id:
                params['GatewayId'] = gateway_id
            elif nat_gateway_id:
                params['NatGatewayId'] = nat_gateway_id
            elif instance_id:
                params['InstanceId'] = instance_id
            else:
                raise ValueError("Deve fornecer gateway_id, nat_gateway_id ou instance_id")
            
            # Cria a rota
            self.ec2_client.create_route(**params)
            print(f"Rota adicionada: {destination_cidr} -> {gateway_id or nat_gateway_id or instance_id}")
            
            return True
            
        except ClientError as e:
            print(f"Erro ao adicionar rota: {e}")
            return False
    
    def associate_route_table(
        self,
        route_table_id: str,
        subnet_id: str
    ) -> str:
        """
        Associa route table a uma subnet
        
        Args:
            route_table_id: ID da route table
            subnet_id: ID da subnet
        
        Returns:
            association_id: ID da associação
        """
        try:
            # Associa route table à subnet
            response = self.ec2_client.associate_route_table(
                RouteTableId=route_table_id,
                SubnetId=subnet_id
            )
            
            association_id = response['AssociationId']
            print(f"Route Table {route_table_id} associada à Subnet {subnet_id}")
            
            return association_id
            
        except ClientError as e:
            print(f"Erro ao associar route table: {e}")
            raise
    
    def create_security_group(
        self,
        vpc_id: str,
        group_name: str,
        description: str,
        tags: Dict[str, str] = None
    ) -> str:
        """
        Cria Security Group
        
        Security Group:
        - Firewall virtual stateful (rastreia conexões)
        - Controla tráfego inbound e outbound
        - Regras permissivas apenas (não há deny)
        - Pode referenciar outros security groups
        - Avaliado antes de NACLs
        
        Args:
            vpc_id: ID da VPC
            group_name: Nome do security group
            description: Descrição do security group
            tags: Tags para organização
        
        Returns:
            security_group_id: ID do security group
        """
        try:
            # Cria security group
            response = self.ec2_client.create_security_group(
                GroupName=group_name,
                Description=description,
                VpcId=vpc_id
            )
            
            security_group_id = response['GroupId']
            print(f"Security Group criado: {security_group_id}")
            
            # Adiciona tags
            if tags:
                self.ec2_client.create_tags(
                    Resources=[security_group_id],
                    Tags=[{'Key': k, 'Value': v} for k, v in tags.items()]
                )
            
            return security_group_id
            
        except ClientError as e:
            print(f"Erro ao criar Security Group: {e}")
            raise
    
    def add_security_group_rule(
        self,
        security_group_id: str,
        ip_protocol: str,
        from_port: int,
        to_port: int,
        cidr_ip: str = None,
        source_security_group_id: str = None,
        direction: str = 'ingress'
    ) -> bool:
        """
        Adiciona regra ao Security Group
        
        Args:
            security_group_id: ID do security group
            ip_protocol: Protocolo (tcp, udp, icmp, -1 para all)
            from_port: Porta inicial
            to_port: Porta final
            cidr_ip: CIDR de origem/destino (ex: 0.0.0.0/0)
            source_security_group_id: ID de outro security group
            direction: 'ingress' (inbound) ou 'egress' (outbound)
        
        Returns:
            bool: True se sucesso
        """
        try:
            # Prepara permissão
            ip_permission = {
                'IpProtocol': ip_protocol,
                'FromPort': from_port,
                'ToPort': to_port
            }
            
            # Adiciona origem/destino
            if cidr_ip:
                ip_permission['IpRanges'] = [{'CidrIp': cidr_ip}]
            elif source_security_group_id:
                ip_permission['UserIdGroupPairs'] = [{'GroupId': source_security_group_id}]
            
            # Adiciona regra inbound ou outbound
            if direction == 'ingress':
                self.ec2_client.authorize_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[ip_permission]
                )
                print(f"Regra inbound adicionada ao SG {security_group_id}")
            else:
                self.ec2_client.authorize_security_group_egress(
                    GroupId=security_group_id,
                    IpPermissions=[ip_permission]
                )
                print(f"Regra outbound adicionada ao SG {security_group_id}")
            
            return True
            
        except ClientError as e:
            print(f"Erro ao adicionar regra: {e}")
            return False


def create_complete_vpc_architecture():
    """
    Cria arquitetura VPC completa com subnets públicas e privadas
    
    Arquitetura:
    - VPC com CIDR 10.0.0.0/16
    - 2 Subnets públicas (10.0.1.0/24, 10.0.2.0/24) em AZs diferentes
    - 2 Subnets privadas (10.0.11.0/24, 10.0.12.0/24) em AZs diferentes
    - Internet Gateway para subnets públicas
    - NAT Gateway para subnets privadas
    - Route tables apropriadas
    - Security Groups para web e database
    
    Esta é uma arquitetura típica de produção (High Availability)
    """
    vpc_manager = VPCManager(region_name='us-east-1')
    
    print("\n=== Criando VPC ===")
    vpc_id = vpc_manager.create_vpc(
        cidr_block='10.0.0.0/16',
        tags={'Name': 'Production-VPC', 'Environment': 'Production'}
    )
    
    print("\n=== Criando Subnets Públicas ===")
    public_subnet_1 = vpc_manager.create_subnet(
        vpc_id=vpc_id,
        cidr_block='10.0.1.0/24',
        availability_zone='us-east-1a',
        is_public=True,
        tags={'Name': 'Public-Subnet-1A', 'Type': 'Public'}
    )
    
    public_subnet_2 = vpc_manager.create_subnet(
        vpc_id=vpc_id,
        cidr_block='10.0.2.0/24',
        availability_zone='us-east-1b',
        is_public=True,
        tags={'Name': 'Public-Subnet-1B', 'Type': 'Public'}
    )
    
    print("\n=== Criando Subnets Privadas ===")
    private_subnet_1 = vpc_manager.create_subnet(
        vpc_id=vpc_id,
        cidr_block='10.0.11.0/24',
        availability_zone='us-east-1a',
        is_public=False,
        tags={'Name': 'Private-Subnet-1A', 'Type': 'Private'}
    )
    
    private_subnet_2 = vpc_manager.create_subnet(
        vpc_id=vpc_id,
        cidr_block='10.0.12.0/24',
        availability_zone='us-east-1b',
        is_public=False,
        tags={'Name': 'Private-Subnet-1B', 'Type': 'Private'}
    )
    
    print("\n=== Criando Internet Gateway ===")
    igw_id = vpc_manager.create_internet_gateway(
        vpc_id=vpc_id,
        tags={'Name': 'Production-IGW'}
    )
    
    print("\n=== Criando NAT Gateway ===")
    nat_gateway_id = vpc_manager.create_nat_gateway(
        subnet_id=public_subnet_1,
        tags={'Name': 'Production-NAT'}
    )
    
    print("\n=== Configurando Route Tables ===")
    # Route table para subnets públicas
    public_rt = vpc_manager.create_route_table(
        vpc_id=vpc_id,
        tags={'Name': 'Public-RT'}
    )
    vpc_manager.add_route(public_rt, '0.0.0.0/0', gateway_id=igw_id)
    vpc_manager.associate_route_table(public_rt, public_subnet_1)
    vpc_manager.associate_route_table(public_rt, public_subnet_2)
    
    # Route table para subnets privadas
    private_rt = vpc_manager.create_route_table(
        vpc_id=vpc_id,
        tags={'Name': 'Private-RT'}
    )
    vpc_manager.add_route(private_rt, '0.0.0.0/0', nat_gateway_id=nat_gateway_id)
    vpc_manager.associate_route_table(private_rt, private_subnet_1)
    vpc_manager.associate_route_table(private_rt, private_subnet_2)
    
    print("\n=== Criando Security Groups ===")
    # Security Group para Web Servers
    web_sg = vpc_manager.create_security_group(
        vpc_id=vpc_id,
        group_name='web-servers-sg',
        description='Security group for web servers',
        tags={'Name': 'Web-Servers-SG'}
    )
    vpc_manager.add_security_group_rule(web_sg, 'tcp', 80, 80, cidr_ip='0.0.0.0/0')
    vpc_manager.add_security_group_rule(web_sg, 'tcp', 443, 443, cidr_ip='0.0.0.0/0')
    
    # Security Group para Database
    db_sg = vpc_manager.create_security_group(
        vpc_id=vpc_id,
        group_name='database-sg',
        description='Security group for database',
        tags={'Name': 'Database-SG'}
    )
    vpc_manager.add_security_group_rule(
        db_sg, 'tcp', 3306, 3306,
        source_security_group_id=web_sg
    )
    
    print("\n✅ Arquitetura VPC criada com sucesso!")
    print(f"VPC ID: {vpc_id}")
    print(f"Public Subnets: {public_subnet_1}, {public_subnet_2}")
    print(f"Private Subnets: {private_subnet_1}, {private_subnet_2}")


if __name__ == "__main__":
    create_complete_vpc_architecture()
