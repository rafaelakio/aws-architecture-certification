# 🚀 Guia de Início Rápido

## Bem-vindo ao Projeto AWS Architecture Certification!

Este guia vai te ajudar a começar rapidamente com os exemplos práticos.

---

## 📋 Pré-requisitos

### 1. Conta AWS
- Crie uma conta AWS (Free Tier): https://aws.amazon.com/free/
- Configure billing alerts para evitar surpresas

### 2. AWS CLI
```bash
# Windows (usando pip)
pip install awscli

# macOS (usando Homebrew)
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### 3. Python 3.8+
```bash
# Verificar versão
python --version

# Instalar dependências do projeto
pip install -r requirements.txt
```

### 4. Configurar Credenciais AWS
```bash
aws configure
```

Você precisará:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (ex: us-east-1)
- Default output format (json)

---

## 🎯 Primeiros Passos

### Passo 1: Validar Configuração

```bash
# Validar credenciais
python deploy.py validate

# Listar recursos existentes
python deploy.py list
```

### Passo 2: Explorar os Exemplos

#### Estrutura do Projeto:
```
aws-architecture-certification/
├── 01-compute/          # EC2, Lambda, Auto Scaling
├── 02-storage/          # S3, EBS, EFS
├── 03-database/         # RDS, DynamoDB
├── 04-networking/       # VPC, Route 53, CloudFront
├── 05-security/         # IAM, KMS, Security Groups
├── 06-integration/      # SQS, SNS, EventBridge
├── 07-monitoring/       # CloudWatch, CloudTrail
├── 08-iac/             # CloudFormation, CDK
├── 09-architectures/    # Arquiteturas comuns
└── 10-exam-tips/       # Dicas para certificação
```

### Passo 3: Executar Exemplos Práticos

#### Exemplo 1: Gerenciar EC2
```bash
cd 01-compute
python ec2_management.py
```

#### Exemplo 2: Operações S3
```bash
cd 02-storage
python s3_operations.py
```

#### Exemplo 3: DynamoDB
```bash
cd 03-database
python dynamodb_operations.py
```

#### Exemplo 4: Criar VPC Completa
```bash
cd 04-networking
python vpc_setup.py
```

#### Exemplo 5: Gerenciar IAM
```bash
cd 05-security
python iam_management.py
```

---

## 🏗️ Deploy de Infraestrutura Completa

### Usando CloudFormation

```bash
# Deploy da stack completa
python deploy.py deploy \
  --stack-name my-certification-stack \
  --template 08-iac/cloudformation_template.yaml \
  --param EnvironmentName=Development \
  --param InstanceType=t2.micro \
  --param KeyName=my-key-pair \
  --param DBUsername=admin \
  --param DBPassword=MySecurePassword123

# Verificar status
python deploy.py list

# Deletar stack (quando terminar)
python deploy.py delete --stack-name my-certification-stack
```

### Estimativa de Custos

```bash
python deploy.py estimate --template 08-iac/cloudformation_template.yaml
```

---

## 📚 Roteiro de Estudos Recomendado

### Semana 1-2: Fundamentos
1. **Dia 1-2**: VPC e Networking
   - Leia: `04-networking/README.md`
   - Execute: `vpc_setup.py`
   - Pratique: Criar VPC no console

2. **Dia 3-4**: EC2 e Compute
   - Leia: `01-compute/README.md`
   - Execute: `ec2_management.py`
   - Pratique: Lançar instâncias

3. **Dia 5-6**: S3 e Storage
   - Leia: `02-storage/`
   - Execute: `s3_operations.py`
   - Pratique: Upload/download de arquivos

4. **Dia 7**: IAM e Security
   - Leia: `05-security/`
   - Execute: `iam_management.py`
   - Pratique: Criar users, groups, roles

### Semana 3-4: Serviços Avançados
1. **Dia 8-9**: Databases
   - RDS e DynamoDB
   - Execute exemplos práticos

2. **Dia 10-11**: Lambda e Serverless
   - Lambda functions
   - API Gateway

3. **Dia 12-13**: Load Balancing e Auto Scaling
   - ALB, NLB
   - Auto Scaling Groups

4. **Dia 14**: Monitoring
   - CloudWatch
   - CloudTrail

### Semana 5-6: Arquiteturas e Prática
1. **Dia 15-18**: Arquiteturas Comuns
   - Leia: `09-architectures/COMMON_ARCHITECTURES.md`
   - Implemente: Three-Tier Architecture
   - Implemente: Serverless Architecture

2. **Dia 19-21**: Infrastructure as Code
   - CloudFormation
   - Deploy stacks completas

3. **Dia 22-28**: Revisão e Simulados
   - Leia: `10-exam-tips/EXAM_GUIDE.md`
   - Faça simulados
   - Revise pontos fracos

---

## 💡 Dicas Importantes

### 1. Use Free Tier
A maioria dos exemplos usa recursos Free Tier:
- EC2: t2.micro (750 horas/mês)
- S3: 5 GB storage
- RDS: db.t2.micro (750 horas/mês)
- Lambda: 1M requests/mês
- DynamoDB: 25 GB storage

### 2. Sempre Limpe Recursos
```bash
# Deletar recursos após prática
python deploy.py delete --stack-name <nome-da-stack>

# Verificar recursos órfãos no console
# - EC2 Instances
# - RDS Databases
# - S3 Buckets
# - Elastic IPs
# - NAT Gateways
```

### 3. Configure Billing Alerts
1. Acesse AWS Billing Console
2. Configure alert para $10, $50, $100
3. Monitore diariamente

### 4. Use Tags
Sempre adicione tags aos recursos:
```python
tags = {
    'Project': 'AWS-Certification',
    'Environment': 'Learning',
    'Owner': 'YourName'
}
```

---

## 🔧 Troubleshooting

### Erro: "Unable to locate credentials"
```bash
# Reconfigure AWS CLI
aws configure

# Ou defina variáveis de ambiente
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

### Erro: "Access Denied"
- Verifique permissões IAM do usuário
- Certifique-se de ter permissões necessárias

### Erro: "Resource already exists"
- Recurso já foi criado
- Use nomes únicos ou delete o existente

### Erro: "Limit exceeded"
- Você atingiu limite de serviço
- Solicite aumento de limite ou use outra região

---

## 📖 Recursos Adicionais

### Documentação Oficial:
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)
- [AWS Whitepapers](https://aws.amazon.com/whitepapers/)

### Prática:
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Workshops](https://workshops.aws/)
- [AWS Hands-On Tutorials](https://aws.amazon.com/getting-started/hands-on/)

### Simulados:
- [AWS Practice Exams](https://aws.amazon.com/certification/certification-prep/)
- [Tutorials Dojo](https://tutorialsdojo.com/)
- [Whizlabs](https://www.whizlabs.com/)

### Comunidade:
- [AWS Reddit](https://www.reddit.com/r/aws/)
- [AWS re:Post](https://repost.aws/)
- [Stack Overflow - AWS Tag](https://stackoverflow.com/questions/tagged/amazon-web-services)

---

## 🎓 Próximos Passos

1. ✅ Configure seu ambiente AWS
2. ✅ Execute os exemplos básicos
3. ✅ Leia a documentação de cada serviço
4. ✅ Pratique no console AWS
5. ✅ Implemente arquiteturas completas
6. ✅ Faça simulados
7. ✅ Agende seu exame!

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique a documentação do serviço
2. Consulte o guia de troubleshooting
3. Pesquise no Stack Overflow
4. Consulte AWS Support (se tiver plano)

---

## ⚠️ Avisos Importantes

1. **Custos**: Mesmo com Free Tier, alguns recursos geram custos
2. **Segurança**: Nunca commite credenciais AWS no Git
3. **Limpeza**: Sempre delete recursos após prática
4. **Região**: Use us-east-1 para melhor compatibilidade com Free Tier

---

## 🎯 Meta Final

**Passar na certificação AWS Solutions Architect Associate!**

Boa sorte nos estudos! 🚀

---

**Lembre-se**: A prática leva à perfeição. Quanto mais você usar os serviços AWS, mais confortável ficará com eles no exame.

**Você consegue! 💪**
