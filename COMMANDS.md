# 🔧 Comandos Úteis AWS CLI

## Guia de Referência Rápida

Este documento contém comandos AWS CLI mais usados para certificação.

---

## 📋 Configuração Inicial

### Configurar AWS CLI
```bash
# Configuração interativa
aws configure

# Configurar profile específico
aws configure --profile production

# Listar profiles configurados
aws configure list-profiles

# Ver configuração atual
aws configure list
```

### Verificar Identidade
```bash
# Ver informações da conta
aws sts get-caller-identity

# Ver região configurada
aws configure get region
```

---

## 🖥️ EC2 (Elastic Compute Cloud)

### Instâncias
```bash
# Listar todas as instâncias
aws ec2 describe-instances

# Listar instâncias running
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"

# Criar instância
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --key-name my-key \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx

# Iniciar instância
aws ec2 start-instances --instance-ids i-xxxxx

# Parar instância
aws ec2 stop-instances --instance-ids i-xxxxx

# Terminar instância
aws ec2 terminate-instances --instance-ids i-xxxxx

# Descrever instância específica
aws ec2 describe-instances --instance-ids i-xxxxx
```

### AMIs
```bash
# Listar AMIs
aws ec2 describe-images --owners self

# Criar AMI de instância
aws ec2 create-image \
  --instance-id i-xxxxx \
  --name "My-AMI-$(date +%Y%m%d)" \
  --description "Backup AMI"

# Deletar AMI
aws ec2 deregister-image --image-id ami-xxxxx
```

### Key Pairs
```bash
# Criar key pair
aws ec2 create-key-pair \
  --key-name my-key \
  --query 'KeyMaterial' \
  --output text > my-key.pem

# Listar key pairs
aws ec2 describe-key-pairs

# Deletar key pair
aws ec2 delete-key-pair --key-name my-key
```

---

## 🌐 VPC (Virtual Private Cloud)

### VPC
```bash
# Listar VPCs
aws ec2 describe-vpcs

# Criar VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Deletar VPC
aws ec2 delete-vpc --vpc-id vpc-xxxxx

# Habilitar DNS hostnames
aws ec2 modify-vpc-attribute \
  --vpc-id vpc-xxxxx \
  --enable-dns-hostnames
```

### Subnets
```bash
# Listar subnets
aws ec2 describe-subnets

# Criar subnet
aws ec2 create-subnet \
  --vpc-id vpc-xxxxx \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a

# Deletar subnet
aws ec2 delete-subnet --subnet-id subnet-xxxxx
```

### Internet Gateway
```bash
# Criar Internet Gateway
aws ec2 create-internet-gateway

# Anexar IGW à VPC
aws ec2 attach-internet-gateway \
  --internet-gateway-id igw-xxxxx \
  --vpc-id vpc-xxxxx

# Desanexar IGW
aws ec2 detach-internet-gateway \
  --internet-gateway-id igw-xxxxx \
  --vpc-id vpc-xxxxx
```

### Security Groups
```bash
# Listar security groups
aws ec2 describe-security-groups

# Criar security group
aws ec2 create-security-group \
  --group-name my-sg \
  --description "My security group" \
  --vpc-id vpc-xxxxx

# Adicionar regra inbound
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Remover regra
aws ec2 revoke-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```

---

## 📦 S3 (Simple Storage Service)

### Buckets
```bash
# Listar buckets
aws s3 ls

# Criar bucket
aws s3 mb s3://my-bucket-name

# Deletar bucket (vazio)
aws s3 rb s3://my-bucket-name

# Deletar bucket (com conteúdo)
aws s3 rb s3://my-bucket-name --force

# Listar objetos em bucket
aws s3 ls s3://my-bucket-name
aws s3 ls s3://my-bucket-name/folder/ --recursive
```

### Objetos
```bash
# Upload de arquivo
aws s3 cp file.txt s3://my-bucket/

# Upload de pasta
aws s3 cp folder/ s3://my-bucket/folder/ --recursive

# Download de arquivo
aws s3 cp s3://my-bucket/file.txt ./

# Download de pasta
aws s3 cp s3://my-bucket/folder/ ./folder/ --recursive

# Sync (sincronizar)
aws s3 sync ./local-folder s3://my-bucket/remote-folder

# Deletar objeto
aws s3 rm s3://my-bucket/file.txt

# Deletar pasta
aws s3 rm s3://my-bucket/folder/ --recursive
```

### Configurações
```bash
# Habilitar versioning
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Configurar lifecycle
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json

# Configurar website
aws s3 website s3://my-bucket/ \
  --index-document index.html \
  --error-document error.html
```

---

## 🗄️ DynamoDB

### Tabelas
```bash
# Listar tabelas
aws dynamodb list-tables

# Criar tabela
aws dynamodb create-table \
  --table-name Users \
  --attribute-definitions \
    AttributeName=UserId,AttributeType=S \
  --key-schema \
    AttributeName=UserId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Descrever tabela
aws dynamodb describe-table --table-name Users

# Deletar tabela
aws dynamodb delete-table --table-name Users
```

### Itens
```bash
# Inserir item
aws dynamodb put-item \
  --table-name Users \
  --item '{"UserId": {"S": "user123"}, "Name": {"S": "John"}}'

# Buscar item
aws dynamodb get-item \
  --table-name Users \
  --key '{"UserId": {"S": "user123"}}'

# Scan (todos os itens)
aws dynamodb scan --table-name Users

# Query
aws dynamodb query \
  --table-name Users \
  --key-condition-expression "UserId = :id" \
  --expression-attribute-values '{":id": {"S": "user123"}}'
```

---

## 🔐 IAM (Identity and Access Management)

### Usuários
```bash
# Listar usuários
aws iam list-users

# Criar usuário
aws iam create-user --user-name john

# Deletar usuário
aws iam delete-user --user-name john

# Criar access key
aws iam create-access-key --user-name john

# Listar access keys
aws iam list-access-keys --user-name john
```

### Grupos
```bash
# Listar grupos
aws iam list-groups

# Criar grupo
aws iam create-group --group-name developers

# Adicionar usuário ao grupo
aws iam add-user-to-group \
  --user-name john \
  --group-name developers
```

### Roles
```bash
# Listar roles
aws iam list-roles

# Criar role
aws iam create-role \
  --role-name MyRole \
  --assume-role-policy-document file://trust-policy.json

# Anexar policy à role
aws iam attach-role-policy \
  --role-name MyRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

### Policies
```bash
# Listar policies
aws iam list-policies --scope Local

# Criar policy
aws iam create-policy \
  --policy-name MyPolicy \
  --policy-document file://policy.json

# Anexar policy a usuário
aws iam attach-user-policy \
  --user-name john \
  --policy-arn arn:aws:iam::123456789012:policy/MyPolicy
```

---

## ⚖️ ELB (Elastic Load Balancing)

### Application Load Balancer
```bash
# Listar load balancers
aws elbv2 describe-load-balancers

# Criar ALB
aws elbv2 create-load-balancer \
  --name my-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx

# Criar target group
aws elbv2 create-target-group \
  --name my-targets \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-xxxxx

# Registrar targets
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --targets Id=i-xxxxx Id=i-yyyyy
```

---

## 📊 CloudWatch

### Logs
```bash
# Listar log groups
aws logs describe-log-groups

# Criar log group
aws logs create-log-group --log-group-name /aws/lambda/my-function

# Ver logs
aws logs tail /aws/lambda/my-function --follow
```

### Métricas
```bash
# Listar métricas
aws cloudwatch list-metrics

# Obter estatísticas
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z \
  --period 3600 \
  --statistics Average
```

### Alarmes
```bash
# Listar alarmes
aws cloudwatch describe-alarms

# Criar alarme
aws cloudwatch put-metric-alarm \
  --alarm-name cpu-high \
  --alarm-description "CPU > 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

---

## 📚 CloudFormation

### Stacks
```bash
# Listar stacks
aws cloudformation list-stacks

# Criar stack
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=my-key

# Atualizar stack
aws cloudformation update-stack \
  --stack-name my-stack \
  --template-body file://template.yaml

# Deletar stack
aws cloudformation delete-stack --stack-name my-stack

# Descrever stack
aws cloudformation describe-stacks --stack-name my-stack

# Ver eventos da stack
aws cloudformation describe-stack-events --stack-name my-stack
```

---

## 🔔 SNS (Simple Notification Service)

### Tópicos
```bash
# Listar tópicos
aws sns list-topics

# Criar tópico
aws sns create-topic --name my-topic

# Publicar mensagem
aws sns publish \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
  --message "Hello World"

# Inscrever email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
  --protocol email \
  --notification-endpoint user@example.com
```

---

## 📬 SQS (Simple Queue Service)

### Filas
```bash
# Listar filas
aws sqs list-queues

# Criar fila
aws sqs create-queue --queue-name my-queue

# Enviar mensagem
aws sqs send-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --message-body "Hello World"

# Receber mensagens
aws sqs receive-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue

# Deletar mensagem
aws sqs delete-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --receipt-handle <receipt-handle>
```

---

## ⚡ Lambda

### Funções
```bash
# Listar funções
aws lambda list-functions

# Criar função
aws lambda create-function \
  --function-name my-function \
  --runtime python3.9 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip

# Invocar função
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  response.json

# Atualizar código
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://function.zip

# Deletar função
aws lambda delete-function --function-name my-function
```

---

## 🔍 Comandos Úteis de Filtro e Formatação

### Filtros JMESPath
```bash
# Listar apenas IDs de instâncias
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].InstanceId' \
  --output text

# Listar instâncias com nome e estado
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`].Value|[0],State.Name]' \
  --output table

# Filtrar por tag
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=Production"
```

### Formatos de Output
```bash
# JSON (padrão)
aws ec2 describe-instances --output json

# Tabela
aws ec2 describe-instances --output table

# Texto
aws ec2 describe-instances --output text

# YAML
aws ec2 describe-instances --output yaml
```

---

## 💡 Dicas Úteis

### Usar Profiles
```bash
# Executar comando com profile específico
aws s3 ls --profile production

# Definir profile padrão temporariamente
export AWS_PROFILE=production
```

### Dry Run
```bash
# Testar comando sem executar
aws ec2 run-instances \
  --image-id ami-xxxxx \
  --instance-type t2.micro \
  --dry-run
```

### Paginação
```bash
# Listar todos os resultados (auto-paginação)
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --max-items 1000

# Controle manual de paginação
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --max-keys 100 \
  --starting-token <token>
```

---

## 📝 Scripts Úteis

### Backup de Instância EC2
```bash
#!/bin/bash
INSTANCE_ID="i-xxxxx"
DATE=$(date +%Y%m%d-%H%M%S)

aws ec2 create-image \
  --instance-id $INSTANCE_ID \
  --name "backup-$INSTANCE_ID-$DATE" \
  --description "Automated backup" \
  --no-reboot
```

### Limpar Snapshots Antigos
```bash
#!/bin/bash
# Deletar snapshots com mais de 30 dias
CUTOFF_DATE=$(date -d '30 days ago' +%Y-%m-%d)

aws ec2 describe-snapshots --owner-ids self \
  --query "Snapshots[?StartTime<='$CUTOFF_DATE'].SnapshotId" \
  --output text | xargs -n 1 aws ec2 delete-snapshot --snapshot-id
```

---

## 🔗 Recursos Adicionais

- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [AWS CLI Command Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/index.html)
- [JMESPath Tutorial](https://jmespath.org/tutorial.html)

---

**Dica**: Use `aws <service> help` para ver ajuda de qualquer comando!

Exemplo:
```bash
aws ec2 help
aws s3 cp help
```
