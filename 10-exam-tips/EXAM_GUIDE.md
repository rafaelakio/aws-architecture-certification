# Guia Completo para Certificação AWS Solutions Architect

## 📋 Visão Geral do Exame

### AWS Certified Solutions Architect - Associate (SAA-C03)
- **Duração**: 130 minutos
- **Questões**: 65 questões (múltipla escolha e múltipla resposta)
- **Pontuação**: 100-1000 (mínimo 720 para passar)
- **Custo**: $150 USD
- **Validade**: 3 anos

### Domínios do Exame
1. **Design de Arquiteturas Seguras** (30%)
2. **Design de Arquiteturas Resilientes** (26%)
3. **Design de Arquiteturas de Alto Desempenho** (24%)
4. **Design de Arquiteturas Otimizadas em Custo** (20%)

---

## 🎯 Tópicos Mais Cobrados

### 1. VPC e Networking (MUITO IMPORTANTE)

#### Conceitos Essenciais:
- **CIDR Blocks**: Entenda cálculo de IPs
  - /16 = 65,536 IPs
  - /24 = 256 IPs
  - /28 = 16 IPs (AWS reserva 5)

- **Subnets**:
  - Pública: Tem rota para Internet Gateway
  - Privada: Sem rota direta para internet
  - Cada subnet em uma única AZ

- **Internet Gateway (IGW)**:
  - Um por VPC
  - Horizontally scaled, redundante
  - Necessário para subnets públicas

- **NAT Gateway vs NAT Instance**:
  - NAT Gateway: Managed, HA, mais caro
  - NAT Instance: Você gerencia, mais barato, single point of failure

- **Security Groups vs NACLs**:
  - SG: Stateful, apenas allow, nível de instância
  - NACL: Stateless, allow e deny, nível de subnet

#### Perguntas Comuns:
❓ **Como permitir instâncias privadas acessarem internet?**
✅ NAT Gateway em subnet pública + rota 0.0.0.0/0 na route table privada

❓ **Como conectar duas VPCs?**
✅ VPC Peering ou Transit Gateway

❓ **Como conectar on-premises com AWS?**
✅ VPN (rápido, internet) ou Direct Connect (dedicado, mais caro)

---

### 2. EC2 (MUITO IMPORTANTE)

#### Instance Types:
- **T2/T3**: Burstable, bom para cargas variáveis
- **M5**: General purpose, balanceado
- **C5**: Compute optimized, CPU intensivo
- **R5**: Memory optimized, bancos de dados
- **I3**: Storage optimized, NoSQL

#### Pricing Models:
- **On-Demand**: Paga por hora, sem compromisso
- **Reserved**: 1-3 anos, até 75% desconto
- **Spot**: Até 90% desconto, pode ser interrompido
- **Savings Plans**: Flexível, desconto por compromisso de uso

#### Placement Groups:
- **Cluster**: Mesma AZ, baixa latência, HPC
- **Spread**: AZs diferentes, HA, máx 7 instâncias/AZ
- **Partition**: Grupos isolados, big data

#### Perguntas Comuns:
❓ **Aplicação precisa de baixa latência entre instâncias?**
✅ Cluster Placement Group

❓ **Como reduzir custos de instâncias previsíveis?**
✅ Reserved Instances ou Savings Plans

❓ **Workload pode ser interrompido?**
✅ Spot Instances

---

### 3. S3 (MUITO IMPORTANTE)

#### Storage Classes:
- **Standard**: Acesso frequente, 99.99% disponibilidade
- **Intelligent-Tiering**: Move automaticamente entre tiers
- **Standard-IA**: Acesso infrequente, mais barato
- **One Zone-IA**: Uma AZ, mais barato ainda
- **Glacier Instant**: Retrieval em ms, arquivamento
- **Glacier Flexible**: Retrieval em min-horas
- **Glacier Deep Archive**: Retrieval em 12h, mais barato

#### Conceitos Importantes:
- **Versioning**: Protege contra deleção acidental
- **Lifecycle Policies**: Transição automática entre classes
- **Replication**: CRR (cross-region) ou SRR (same-region)
- **Encryption**: SSE-S3, SSE-KMS, SSE-C
- **Presigned URLs**: Acesso temporário sem credenciais

#### Perguntas Comuns:
❓ **Dados acessados raramente, mas precisam estar disponíveis imediatamente?**
✅ S3 Standard-IA ou Intelligent-Tiering

❓ **Arquivos de log antigos, acesso raro?**
✅ Lifecycle policy para Glacier

❓ **Como compartilhar arquivo privado temporariamente?**
✅ Presigned URL

---

### 4. RDS e Databases

#### RDS:
- **Multi-AZ**: HA, failover automático, mesma região
- **Read Replicas**: Escala leitura, pode ser cross-region
- **Backup**: Automático (35 dias) ou manual (indefinido)
- **Engines**: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora

#### Aurora:
- 5x mais rápido que MySQL, 3x que PostgreSQL
- Storage auto-scaling até 128 TB
- 6 cópias em 3 AZs
- Aurora Serverless: Auto-scaling, pay per second

#### DynamoDB:
- NoSQL, serverless, single-digit ms latency
- **Partition Key**: Obrigatória
- **Sort Key**: Opcional, permite queries
- **GSI**: Índice com chaves diferentes
- **Streams**: Captura mudanças (24h retenção)

#### Perguntas Comuns:
❓ **Banco precisa de HA automática?**
✅ RDS Multi-AZ ou Aurora

❓ **Escalar leitura de banco relacional?**
✅ Read Replicas

❓ **NoSQL com latência < 10ms?**
✅ DynamoDB

---

### 5. Load Balancing e Auto Scaling

#### Load Balancers:
- **ALB** (Application): Layer 7, HTTP/HTTPS, path-based routing
- **NLB** (Network): Layer 4, TCP/UDP, ultra performance
- **GLB** (Gateway): Layer 3, appliances virtuais

#### Auto Scaling:
- **Target Tracking**: Mantém métrica em valor alvo
- **Step Scaling**: Escala baseado em thresholds
- **Scheduled**: Escala em horários específicos
- **Predictive**: ML para prever demanda

#### Perguntas Comuns:
❓ **Rotear baseado em URL path (/api, /images)?**
✅ Application Load Balancer

❓ **Milhões de requisições/segundo, latência extremamente baixa?**
✅ Network Load Balancer

❓ **Escalar baseado em CPU média de 70%?**
✅ Target Tracking Scaling Policy

---

### 6. Lambda e Serverless

#### Lambda:
- **Timeout**: Máximo 15 minutos
- **Memory**: 128 MB - 10 GB
- **Pricing**: Por requisição e duração
- **Cold Start**: Primeira execução mais lenta
- **Concurrency**: Execuções simultâneas

#### API Gateway:
- REST API ou HTTP API
- WebSocket API para real-time
- Throttling, caching, authentication
- Integra com Lambda, HTTP endpoints

#### Perguntas Comuns:
❓ **Processar arquivos S3 automaticamente?**
✅ Lambda trigger em S3 event

❓ **API REST serverless?**
✅ API Gateway + Lambda

❓ **Processamento > 15 minutos?**
✅ ECS/Fargate ou Step Functions

---

### 7. CloudFront e Route 53

#### CloudFront:
- CDN global, cache em edge locations
- Reduz latência, protege contra DDoS
- Integra com S3, ALB, custom origins
- Signed URLs/Cookies para conteúdo privado

#### Route 53:
- **Simple**: Um registro, um ou mais IPs
- **Weighted**: Distribui tráfego por peso
- **Latency**: Roteia para menor latência
- **Failover**: Primary/Secondary para HA
- **Geolocation**: Baseado em localização do usuário
- **Geoproximity**: Baseado em proximidade geográfica

#### Perguntas Comuns:
❓ **Reduzir latência para usuários globais?**
✅ CloudFront

❓ **Rotear usuários para região mais próxima?**
✅ Route 53 Latency-based routing

❓ **Failover automático entre regiões?**
✅ Route 53 Failover routing

---

### 8. IAM e Security

#### IAM:
- **Users**: Identidade permanente
- **Groups**: Coleção de usuários
- **Roles**: Identidade temporária, sem credenciais
- **Policies**: Documento JSON com permissões

#### Best Practices:
- Princípio do menor privilégio
- MFA para usuários privilegiados
- Roles para EC2/Lambda (não access keys)
- Rotação de credenciais
- CloudTrail para auditoria

#### Perguntas Comuns:
❓ **EC2 precisa acessar S3?**
✅ IAM Role anexada à instância

❓ **Acesso cross-account?**
✅ IAM Role com trust policy

❓ **Auditoria de ações na conta?**
✅ CloudTrail

---

### 9. Monitoring e Management

#### CloudWatch:
- **Metrics**: Monitoramento de recursos
- **Logs**: Centralização de logs
- **Alarms**: Alertas baseados em métricas
- **Events/EventBridge**: Automação baseada em eventos

#### CloudTrail:
- Auditoria de API calls
- Compliance e governança
- Integra com S3 e CloudWatch Logs

#### Systems Manager:
- Gerenciamento de instâncias
- Patch management
- Parameter Store (configurações)
- Session Manager (SSH sem bastion)

#### Perguntas Comuns:
❓ **Alertar quando CPU > 80%?**
✅ CloudWatch Alarm

❓ **Quem deletou o bucket S3?**
✅ CloudTrail

❓ **Armazenar configurações sensíveis?**
✅ Systems Manager Parameter Store ou Secrets Manager

---

### 10. Messaging e Integration

#### SQS:
- Fila de mensagens, desacoplamento
- Standard: At-least-once, ordem não garantida
- FIFO: Exactly-once, ordem garantida
- Visibility timeout, dead-letter queue

#### SNS:
- Pub/Sub, notificações push
- Múltiplos subscribers (email, SMS, Lambda, SQS)
- Fan-out pattern

#### EventBridge:
- Event bus serverless
- Integra com 90+ AWS services
- Regras e filtros de eventos

#### Perguntas Comuns:
❓ **Desacoplar componentes de aplicação?**
✅ SQS

❓ **Notificar múltiplos sistemas de um evento?**
✅ SNS

❓ **Processar eventos de múltiplos serviços AWS?**
✅ EventBridge

---

## 💡 Dicas de Estudo

### Estratégia de Preparação:
1. **Fundamentos** (2-3 semanas):
   - VPC, EC2, S3, IAM
   - Hands-on com Free Tier

2. **Serviços Avançados** (2-3 semanas):
   - RDS, DynamoDB, Lambda
   - Load Balancers, Auto Scaling
   - CloudFront, Route 53

3. **Arquiteturas** (1-2 semanas):
   - Well-Architected Framework
   - Casos de uso reais
   - Trade-offs de design

4. **Simulados** (1 semana):
   - Practice exams
   - Revisar erros
   - Identificar gaps

### Recursos Recomendados:
- ✅ AWS Free Tier (hands-on prático)
- ✅ AWS Well-Architected Framework
- ✅ AWS Whitepapers
- ✅ Practice Exams (Tutorials Dojo, Whizlabs)
- ✅ AWS Documentation

---

## 🎓 Padrões de Perguntas

### Tipo 1: Escolha o Serviço Correto
**Exemplo**: "Uma empresa precisa de um banco de dados NoSQL com latência de single-digit milliseconds..."
- Leia com atenção os requisitos
- Elimine opções claramente erradas
- Considere trade-offs (custo vs performance)

### Tipo 2: Arquitetura de Alta Disponibilidade
**Exemplo**: "Como garantir que a aplicação continue funcionando se uma AZ falhar?"
- Multi-AZ deployment
- Load balancer em múltiplas AZs
- Auto Scaling em múltiplas AZs

### Tipo 3: Otimização de Custos
**Exemplo**: "Como reduzir custos de armazenamento S3?"
- Lifecycle policies
- Storage classes apropriadas
- Intelligent-Tiering

### Tipo 4: Segurança
**Exemplo**: "Como permitir EC2 acessar S3 de forma segura?"
- IAM Roles (NUNCA access keys em instâncias)
- Princípio do menor privilégio
- Encryption at rest e in transit

---

## ⚠️ Erros Comuns a Evitar

1. **Não ler a pergunta completamente**
   - Preste atenção em "MOST cost-effective", "LEAST operational overhead"

2. **Ignorar requisitos de HA**
   - Multi-AZ é diferente de Multi-Region
   - Read Replicas não são para HA (use Multi-AZ)

3. **Confundir serviços similares**
   - SQS vs SNS vs EventBridge
   - CloudWatch vs CloudTrail
   - Security Groups vs NACLs

4. **Esquecer limitações**
   - Lambda: 15 min timeout
   - S3: Eventual consistency para overwrites (agora strong consistency)
   - DynamoDB: 400 KB item size limit

5. **Não considerar custo**
   - Perguntas frequentemente pedem solução "cost-effective"
   - Serverless geralmente mais barato para cargas variáveis
   - Reserved Instances para cargas previsíveis

---

## 📊 Checklist Final

### Antes do Exame:
- [ ] Revisei todos os serviços principais
- [ ] Fiz pelo menos 3 simulados completos
- [ ] Entendo Well-Architected Framework
- [ ] Pratiquei hands-on com AWS Console
- [ ] Revisei meus erros em simulados
- [ ] Descansado e alimentado

### Durante o Exame:
- [ ] Ler pergunta completamente
- [ ] Identificar palavras-chave (cost-effective, HA, etc)
- [ ] Eliminar opções claramente erradas
- [ ] Marcar questões difíceis para revisar
- [ ] Gerenciar tempo (2 min por questão)

---

## 🎯 Palavras-Chave nas Perguntas

- **"Most cost-effective"** → Serverless, Spot, Reserved, Lifecycle
- **"Least operational overhead"** → Managed services, Serverless
- **"High availability"** → Multi-AZ, Load Balancer, Auto Scaling
- **"Disaster recovery"** → Backups, Replication, Multi-Region
- **"Scalable"** → Auto Scaling, DynamoDB, Lambda
- **"Secure"** → IAM Roles, Encryption, VPC, Security Groups
- **"Low latency"** → CloudFront, ElastiCache, DynamoDB
- **"Real-time"** → Kinesis, DynamoDB Streams, Lambda

---

## 🚀 Boa Sorte!

Lembre-se:
- **Prática** é essencial - use AWS Free Tier
- **Entenda conceitos**, não decore
- **Pense como arquiteto** - trade-offs e requisitos
- **Gerencie seu tempo** no exame
- **Confie na sua preparação**

**Você consegue! 💪**
