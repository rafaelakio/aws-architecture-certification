# AWS Architecture Certification - Guia Completo

## 📚 Sobre o Projeto

Este repositório contém exemplos práticos e detalhados dos tópicos mais cobrados nas certificações de arquitetura AWS (Solutions Architect Associate e Professional), com código comentado linha por linha.

## 🎯 Tópicos Cobertos

### 1. **Compute Services**
- EC2 (Elastic Compute Cloud)
- Lambda (Serverless)
- Auto Scaling Groups
- Elastic Load Balancing

### 2. **Storage Services**
- S3 (Simple Storage Service)
- EBS (Elastic Block Store)
- EFS (Elastic File System)
- Storage Gateway

### 3. **Database Services**
- RDS (Relational Database Service)
- DynamoDB
- ElastiCache
- Aurora

### 4. **Networking & Content Delivery**
- VPC (Virtual Private Cloud)
- Route 53
- CloudFront
- API Gateway

### 5. **Security & Identity**
- IAM (Identity and Access Management)
- KMS (Key Management Service)
- Secrets Manager
- Security Groups & NACLs

### 6. **Application Integration**
- SQS (Simple Queue Service)
- SNS (Simple Notification Service)
- EventBridge
- Step Functions

### 7. **Monitoring & Management**
- CloudWatch
- CloudTrail
- Systems Manager
- AWS Config

### 8. **Infrastructure as Code**
- CloudFormation
- CDK (Cloud Development Kit)
- Terraform

## 🚀 Como Usar

Cada pasta contém:
- Código de exemplo com comentários detalhados
- Arquivo README específico explicando o serviço
- Diagramas de arquitetura
- Casos de uso reais
- Perguntas comuns de certificação

## 📋 Pré-requisitos

- Conta AWS (Free Tier é suficiente para maioria dos exemplos)
- AWS CLI configurado
- Python 3.8+
- Node.js 14+ (para exemplos CDK)
- Terraform (opcional)

## 🔧 Configuração Inicial

```bash
# Instalar AWS CLI
pip install awscli

# Configurar credenciais
aws configure

# Instalar dependências Python
pip install -r requirements.txt

# Instalar AWS CDK (opcional)
npm install -g aws-cdk
```

## 📖 Estrutura do Projeto

```
aws-architecture-certification/
├── 01-compute/
├── 02-storage/
├── 03-database/
├── 04-networking/
├── 05-security/
├── 06-integration/
├── 07-monitoring/
├── 08-iac/
├── 09-architectures/
└── 10-exam-tips/
```

## 🎓 Dicas para Certificação

- Foque em casos de uso práticos
- Entenda os limites e quotas de cada serviço
- Pratique com cenários reais
- Revise os Well-Architected Framework pillars
- Faça simulados regularmente

## 📝 Licença

MIT License - Sinta-se livre para usar em seus estudos!
