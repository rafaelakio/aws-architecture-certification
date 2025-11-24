# Arquiteturas AWS Comuns - Guia Completo

## 📐 Arquiteturas Mais Cobradas na Certificação

---

## 1. Three-Tier Web Application (Arquitetura Clássica)

### Descrição:
Aplicação web com três camadas: apresentação, lógica e dados.

### Componentes:
```
Internet
    ↓
CloudFront (CDN)
    ↓
Route 53 (DNS)
    ↓
Application Load Balancer (Public Subnets)
    ↓
EC2 Auto Scaling Group (Private Subnets)
    ↓
RDS Multi-AZ (Private Subnets)
```

### Detalhes:
- **Camada de Apresentação**: CloudFront + S3 (static assets)
- **Camada de Aplicação**: ALB + EC2 Auto Scaling
- **Camada de Dados**: RDS Multi-AZ ou Aurora

### Características:
- ✅ Alta Disponibilidade (Multi-AZ)
- ✅ Escalabilidade (Auto Scaling)
- ✅ Segurança (Private subnets para app e DB)
- ✅ Performance (CloudFront para cache)

### Quando Usar:
- Aplicações web tradicionais
- E-commerce
- Portais corporativos
- CMS (WordPress, Drupal)

### Custo Estimado:
- **Pequeno**: $100-300/mês
- **Médio**: $500-1500/mês
- **Grande**: $2000+/mês

---

## 2. Serverless Web Application

### Descrição:
Aplicação completamente serverless, sem gerenciamento de servidores.

### Componentes:
```
Internet
    ↓
CloudFront + S3 (Frontend)
    ↓
API Gateway
    ↓
Lambda Functions
    ↓
DynamoDB
```

### Detalhes:
- **Frontend**: S3 + CloudFront (SPA - React, Vue, Angular)
- **Backend**: API Gateway + Lambda
- **Database**: DynamoDB
- **Auth**: Cognito
- **Storage**: S3

### Características:
- ✅ Zero gerenciamento de servidor
- ✅ Auto-scaling automático
- ✅ Pay-per-use (muito econômico para baixo tráfego)
- ✅ Alta disponibilidade nativa

### Quando Usar:
- Startups e MVPs
- Aplicações com tráfego variável
- APIs REST
- Microservices

### Custo Estimado:
- **Baixo tráfego**: $5-50/mês
- **Médio tráfego**: $100-500/mês
- **Alto tráfego**: $1000+/mês

---

## 3. Microservices Architecture

### Descrição:
Aplicação dividida em serviços independentes e desacoplados.

### Componentes:
```
Internet
    ↓
API Gateway / ALB
    ↓
ECS/Fargate Clusters (múltiplos serviços)
    ↓
Service Discovery (Cloud Map)
    ↓
RDS / DynamoDB / ElastiCache
    ↓
SQS / SNS / EventBridge (comunicação assíncrona)
```

### Detalhes:
- **Container Orchestration**: ECS ou EKS
- **Service Mesh**: App Mesh (opcional)
- **Messaging**: SQS, SNS, EventBridge
- **Databases**: Polyglot persistence (RDS, DynamoDB, etc)

### Características:
- ✅ Independência de deploy
- ✅ Escalabilidade granular
- ✅ Resiliência (falha isolada)
- ✅ Tecnologias heterogêneas

### Quando Usar:
- Aplicações complexas
- Times grandes e distribuídos
- Necessidade de escalar componentes independentemente
- Ciclos de release frequentes

### Custo Estimado:
- **Médio**: $1000-3000/mês
- **Grande**: $5000+/mês

---

## 4. Data Lake Architecture

### Descrição:
Armazenamento centralizado de dados estruturados e não estruturados.

### Componentes:
```
Data Sources
    ↓
Kinesis / DMS / DataSync
    ↓
S3 (Data Lake)
    ↓
Glue (ETL) / Athena (Query)
    ↓
QuickSight (Visualization)
```

### Detalhes:
- **Ingestion**: Kinesis, DMS, DataSync, Transfer Family
- **Storage**: S3 (com lifecycle policies)
- **Catalog**: Glue Data Catalog
- **Processing**: Glue ETL, EMR, Lambda
- **Analytics**: Athena, Redshift Spectrum
- **Visualization**: QuickSight

### Características:
- ✅ Armazenamento ilimitado
- ✅ Schema-on-read
- ✅ Suporta qualquer tipo de dado
- ✅ Análise em escala

### Quando Usar:
- Big Data analytics
- Machine Learning
- Business Intelligence
- Data warehousing

### Custo Estimado:
- **Pequeno**: $200-500/mês
- **Médio**: $1000-5000/mês
- **Grande**: $10000+/mês

---

## 5. Disaster Recovery (DR) Architecture

### Descrição:
Estratégias para recuperação de desastres.

### Estratégias (do mais barato ao mais caro):

#### A. Backup and Restore (RPO: horas, RTO: horas)
```
Primary Region
    ↓
Automated Backups → S3
    ↓
Cross-Region Replication
    ↓
DR Region (restore quando necessário)
```

#### B. Pilot Light (RPO: minutos, RTO: horas)
```
Primary Region (full environment)
    ↓
DR Region (minimal resources running)
    - RDS replica
    - AMIs prontas
    - Scripts de scale-up
```

#### C. Warm Standby (RPO: segundos, RTO: minutos)
```
Primary Region (full capacity)
    ↓
DR Region (reduced capacity running)
    - Auto Scaling (min capacity)
    - RDS replica
    - Route 53 failover
```

#### D. Multi-Site Active/Active (RPO: zero, RTO: zero)
```
Region 1 (full capacity)
    ↓
Route 53 (weighted routing)
    ↓
Region 2 (full capacity)
```

### Quando Usar Cada Estratégia:
- **Backup/Restore**: Dados não críticos, custo mínimo
- **Pilot Light**: Aplicações importantes, budget limitado
- **Warm Standby**: Aplicações críticas, RTO < 1 hora
- **Multi-Site**: Aplicações mission-critical, zero downtime

---

## 6. Hybrid Cloud Architecture

### Descrição:
Integração entre on-premises e AWS.

### Componentes:
```
On-Premises Data Center
    ↓
VPN / Direct Connect
    ↓
AWS VPC
    ↓
AWS Services
```

### Opções de Conectividade:

#### A. Site-to-Site VPN
- Conexão criptografada via internet
- Setup rápido (minutos)
- Bandwidth limitado
- Custo baixo

#### B. Direct Connect
- Conexão dedicada
- Setup lento (semanas/meses)
- Bandwidth alto (1-100 Gbps)
- Custo alto
- Baixa latência

#### C. Storage Gateway
- File Gateway: NFS/SMB para S3
- Volume Gateway: iSCSI para EBS
- Tape Gateway: Backup virtual

### Quando Usar:
- Migração gradual para cloud
- Compliance (dados on-premises)
- Latência crítica
- Investimento existente em hardware

---

## 7. Event-Driven Architecture

### Descrição:
Arquitetura baseada em eventos assíncronos.

### Componentes:
```
Event Producers
    ↓
EventBridge / SNS / SQS
    ↓
Event Consumers (Lambda, ECS, etc)
    ↓
Databases / Storage
```

### Padrões Comuns:

#### A. Fan-Out Pattern
```
SNS Topic
    ↓
├─ SQS Queue 1 → Lambda 1
├─ SQS Queue 2 → Lambda 2
└─ SQS Queue 3 → Lambda 3
```

#### B. Event Sourcing
```
Events → EventBridge → Lambda → DynamoDB Streams → Aggregation
```

#### C. CQRS (Command Query Responsibility Segregation)
```
Write Model (DynamoDB) → Streams → Read Model (ElastiCache)
```

### Características:
- ✅ Desacoplamento total
- ✅ Escalabilidade independente
- ✅ Resiliência (retry automático)
- ✅ Processamento assíncrono

### Quando Usar:
- Microservices
- Real-time processing
- IoT applications
- Workflows complexos

---

## 8. Static Website Hosting

### Descrição:
Hospedagem de site estático com alta performance.

### Componentes:
```
S3 Bucket (static files)
    ↓
CloudFront (CDN)
    ↓
Route 53 (DNS)
    ↓
ACM (SSL Certificate)
```

### Detalhes:
- **S3**: Hospedagem de HTML, CSS, JS, imagens
- **CloudFront**: Cache global, HTTPS
- **Route 53**: DNS customizado
- **ACM**: Certificado SSL gratuito

### Características:
- ✅ Custo extremamente baixo
- ✅ Performance global
- ✅ Escalabilidade infinita
- ✅ Zero manutenção

### Quando Usar:
- Landing pages
- Documentação
- Blogs estáticos (Jekyll, Hugo)
- SPAs (React, Vue, Angular)

### Custo Estimado:
- **Típico**: $1-10/mês

---

## 9. Real-Time Analytics

### Descrição:
Processamento e análise de dados em tempo real.

### Componentes:
```
Data Sources (IoT, Apps, Logs)
    ↓
Kinesis Data Streams
    ↓
Kinesis Data Analytics / Lambda
    ↓
Kinesis Data Firehose
    ↓
S3 / Redshift / OpenSearch
    ↓
QuickSight / Grafana
```

### Detalhes:
- **Ingestion**: Kinesis Data Streams
- **Processing**: Kinesis Analytics, Lambda, Flink
- **Storage**: S3, Redshift, OpenSearch
- **Visualization**: QuickSight, Grafana

### Quando Usar:
- IoT analytics
- Clickstream analysis
- Log analytics
- Fraud detection
- Gaming leaderboards

---

## 10. Machine Learning Pipeline

### Descrição:
Pipeline completo de ML na AWS.

### Componentes:
```
Data Sources
    ↓
S3 (Data Lake)
    ↓
SageMaker (Training)
    ↓
SageMaker (Model)
    ↓
SageMaker Endpoint / Lambda
    ↓
Application
```

### Detalhes:
- **Data Prep**: Glue, EMR
- **Training**: SageMaker Training Jobs
- **Model Registry**: SageMaker Model Registry
- **Deployment**: SageMaker Endpoints
- **Inference**: Real-time ou Batch

### Quando Usar:
- Recomendações
- Previsões
- Classificação de imagens
- NLP
- Detecção de anomalias

---

## 📊 Comparação de Arquiteturas

| Arquitetura | Complexidade | Custo | Escalabilidade | HA | Manutenção |
|-------------|--------------|-------|----------------|----|-----------| 
| Three-Tier | Média | Médio | Alta | Alta | Média |
| Serverless | Baixa | Baixo | Muito Alta | Muito Alta | Muito Baixa |
| Microservices | Alta | Alto | Muito Alta | Alta | Alta |
| Data Lake | Média | Médio-Alto | Muito Alta | Alta | Média |
| Static Website | Muito Baixa | Muito Baixo | Infinita | Muito Alta | Muito Baixa |

---

## 🎯 Escolhendo a Arquitetura Certa

### Perguntas a Fazer:

1. **Qual o budget?**
   - Baixo → Serverless ou Static
   - Médio → Three-Tier
   - Alto → Microservices

2. **Qual a expertise do time?**
   - Iniciante → Serverless
   - Intermediário → Three-Tier
   - Avançado → Microservices

3. **Qual o padrão de tráfego?**
   - Variável → Serverless
   - Previsível → Three-Tier com Reserved Instances
   - Constante → EC2 com Reserved

4. **Quais os requisitos de disponibilidade?**
   - 99.9% → Single-AZ
   - 99.99% → Multi-AZ
   - 99.999% → Multi-Region

5. **Há requisitos de compliance?**
   - Sim → Considerar Hybrid ou GovCloud
   - Não → Full cloud

---

## 💡 Best Practices Gerais

1. **Design for Failure**
   - Assuma que tudo pode falhar
   - Multi-AZ deployment
   - Health checks e auto-recovery

2. **Decouple Components**
   - Use queues (SQS)
   - Use load balancers
   - Evite tight coupling

3. **Implement Elasticity**
   - Auto Scaling
   - Serverless quando possível
   - Right-sizing de recursos

4. **Think Parallel**
   - Processe em paralelo
   - Use múltiplas AZs
   - Distribua carga

5. **Security in Depth**
   - Múltiplas camadas de segurança
   - Principle of least privilege
   - Encryption everywhere

6. **Optimize for Cost**
   - Use Reserved/Spot quando apropriado
   - Lifecycle policies
   - Right-sizing contínuo

---

## 📚 Recursos Adicionais

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [AWS Reference Architectures](https://github.com/aws-samples)
- [AWS This Is My Architecture](https://aws.amazon.com/this-is-my-architecture/)

---

**Lembre-se**: Não existe arquitetura perfeita, apenas trade-offs. Escolha baseado em requisitos específicos do seu caso de uso!
