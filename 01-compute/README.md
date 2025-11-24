# Compute Services - AWS

## EC2 (Elastic Compute Cloud)

Serviço fundamental de computação em nuvem que fornece capacidade de computação redimensionável.

### Conceitos Importantes para Certificação:

1. **Instance Types**: T2/T3 (burstable), M5 (general purpose), C5 (compute optimized), R5 (memory optimized)
2. **Pricing Models**: On-Demand, Reserved, Spot, Savings Plans
3. **Placement Groups**: Cluster, Spread, Partition
4. **User Data**: Scripts de inicialização
5. **Instance Metadata**: Informações sobre a instância

## Lambda (Serverless Computing)

Executa código sem provisionar servidores.

### Conceitos Importantes:

1. **Execution Time**: Máximo 15 minutos
2. **Memory**: 128 MB a 10 GB
3. **Triggers**: S3, API Gateway, EventBridge, etc.
4. **Cold Start**: Primeira execução é mais lenta
5. **Concurrency**: Execuções simultâneas

## Auto Scaling

Ajusta automaticamente a capacidade de computação.

### Conceitos Importantes:

1. **Launch Templates**: Configuração de instâncias
2. **Scaling Policies**: Target Tracking, Step Scaling, Simple Scaling
3. **Health Checks**: EC2 e ELB
4. **Cooldown Period**: Tempo entre scaling actions

## Elastic Load Balancing

Distribui tráfego entre múltiplos targets.

### Tipos:

1. **ALB** (Application Load Balancer): Layer 7, HTTP/HTTPS
2. **NLB** (Network Load Balancer): Layer 4, TCP/UDP, ultra performance
3. **GLB** (Gateway Load Balancer): Layer 3, para appliances virtuais
