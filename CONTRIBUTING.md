# Guia de Contribuição - AWS Architecture Certification

Obrigado por considerar contribuir com este projeto de estudos para certificação AWS!

## 🤝 Como Contribuir

### 1. Fork e Clone

```bash
git clone https://github.com/seu-usuario/aws-architecture-certification.git
cd aws-architecture-certification
```

### 2. Configure o Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar AWS CLI
aws configure
```

### 3. Crie uma Branch

```bash
git checkout -b feature/minha-contribuicao
```

### 4. Faça suas Alterações

- Adicione novos exemplos de código
- Melhore documentação
- Adicione diagramas
- Corrija erros

### 5. Teste suas Alterações

```bash
# Validar código Python
python -m py_compile 01-compute/ec2_management.py

# Testar script (cuidado com custos!)
python 01-compute/ec2_management.py --dry-run
```

### 6. Commit e Push

```bash
git add .
git commit -m "feat: adiciona exemplo de [serviço]"
git push origin feature/minha-contribuicao
```

## 📝 Padrões de Código

### Python

```python
# Imports organizados
import boto3
from botocore.exceptions import ClientError
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Funções documentadas
def create_ec2_instance(instance_type='t2.micro'):
    """
    Cria uma instância EC2.
    
    Args:
        instance_type (str): Tipo da instância
        
    Returns:
        dict: Informações da instância criada
        
    Raises:
        ClientError: Se houver erro na criação
    """
    try:
        # Implementação
        pass
    except ClientError as e:
        logger.error(f"Erro ao criar instância: {e}")
        raise
```

### Estrutura de Exemplos

Cada pasta de serviço deve ter:

```
01-compute/
├── ec2_management.py       # Código de exemplo
├── README.md               # Documentação do serviço
├── diagrams/               # Diagramas (opcional)
│   └── architecture.png
└── cloudformation/         # Templates CF (opcional)
    └── ec2-stack.yaml
```

### Documentação de Serviços

```markdown
# Nome do Serviço AWS

## O Que É?

Breve descrição do serviço.

## Por Que é Importante para a Certificação?

- Tópico cobrado no exame
- Casos de uso comuns
- Perguntas frequentes

## Conceitos Principais

### Conceito 1
Explicação

### Conceito 2
Explicação

## Exemplos Práticos

### Exemplo 1: Caso Básico
```python
# Código
```

### Exemplo 2: Caso Avançado
```python
# Código
```

## Perguntas de Certificação

1. **Pergunta típica do exame**
   - Resposta correta
   - Por que as outras estão erradas

## Limites e Quotas

- Limite 1
- Limite 2

## Custos

- Modelo de precificação
- Estimativa de custos

## Melhores Práticas

- Prática 1
- Prática 2

## Recursos Adicionais

- [Documentação AWS](link)
- [FAQ](link)
- [Whitepapers](link)
```

## 🎯 Áreas para Contribuição

### Novos Serviços

- [ ] AWS Backup
- [ ] AWS Transfer Family
- [ ] AWS DataSync
- [ ] AWS App Runner
- [ ] AWS Amplify
- [ ] AWS AppSync
- [ ] AWS Cognito
- [ ] AWS WAF

### Melhorias em Serviços Existentes

- [ ] Adicionar mais exemplos
- [ ] Incluir diagramas
- [ ] Adicionar templates CloudFormation
- [ ] Adicionar templates CDK
- [ ] Melhorar explicações
- [ ] Adicionar perguntas de exame

### Documentação

- [ ] Guias de estudo por tópico
- [ ] Flashcards
- [ ] Simulados
- [ ] Cheat sheets
- [ ] Vídeos explicativos
- [ ] Diagramas de arquitetura

### Arquiteturas

- [ ] Serverless patterns
- [ ] Microservices patterns
- [ ] Data lake architecture
- [ ] Disaster recovery patterns
- [ ] High availability patterns
- [ ] Cost optimization patterns

## 📋 Checklist do Pull Request

- [ ] Código Python está funcional
- [ ] Documentação atualizada
- [ ] Exemplos testados (ou marcados como dry-run)
- [ ] Custos estimados documentados
- [ ] Segue padrões do projeto
- [ ] Não contém credenciais AWS
- [ ] Commit messages descritivas

## ⚠️ Importante: Segurança

### Nunca Commite

- ❌ Access Keys
- ❌ Secret Keys
- ❌ Senhas
- ❌ Tokens
- ❌ Certificados privados

### Use

- ✅ Variáveis de ambiente
- ✅ AWS CLI profiles
- ✅ IAM roles
- ✅ Secrets Manager
- ✅ `.env` files (no .gitignore)

### Exemplo Seguro

```python
# ❌ Ruim
aws_access_key = "AKIAIOSFODNN7EXAMPLE"

# ✅ Bom
import os
aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')

# ✅ Melhor ainda
session = boto3.Session(profile_name='default')
```

## 💰 Custos

### Antes de Contribuir

- Entenda os custos do serviço
- Use Free Tier quando possível
- Documente custos estimados
- Adicione avisos sobre recursos pagos

### Exemplo de Documentação de Custos

```markdown
## ⚠️ Custos

Este exemplo cria recursos que **geram custos**:

- NAT Gateway: ~$32/mês
- EIP: $3.60/mês (se não associado)
- Data Transfer: $0.09/GB

**Estimativa total**: ~$35-40/mês

**Free Tier**: Não aplicável para NAT Gateway

**Recomendação**: Delete recursos após testes
```

## 🧪 Testando

### Testes Locais

```bash
# Validar sintaxe
python -m py_compile script.py

# Dry-run (sem criar recursos)
python script.py --dry-run

# Validar CloudFormation
aws cloudformation validate-template --template-body file://template.yaml
```

### Testes na AWS

```bash
# Usar conta de testes
export AWS_PROFILE=test-account

# Criar recursos em região de teste
export AWS_DEFAULT_REGION=us-east-1

# Sempre limpar após testes
python cleanup.py
```

## 🐛 Reportando Bugs

```markdown
**Descrição**
Descrição clara do problema.

**Serviço AWS**
Nome do serviço afetado.

**Arquivo**
`01-compute/ec2_management.py`

**Como Reproduzir**
1. Execute `python script.py`
2. Observe erro...

**Erro**
```
Cole o erro aqui
```

**Ambiente**
- Python version: [3.8, 3.9, 3.10]
- AWS CLI version: [2.x]
- Região: [us-east-1]
- OS: [Windows, Linux, Mac]
```

## 💡 Sugerindo Melhorias

```markdown
**Serviço/Tópico**
Nome do serviço ou tópico.

**Por Que é Importante**
Relevância para a certificação.

**Conteúdo Proposto**
- Conceito 1
- Conceito 2
- Exemplos

**Referências**
- Link para documentação AWS
- Link para whitepapers
```

## 📚 Recursos para Contribuidores

### Documentação AWS

- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Whitepapers](https://aws.amazon.com/whitepapers/)
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)

### Certificação

- [Exam Guide](https://aws.amazon.com/certification/certified-solutions-architect-associate/)
- [Sample Questions](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Sample-Questions.pdf)
- [AWS Training](https://www.aws.training/)

### Ferramentas

- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS CLI Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/index.html)
- [CloudFormation Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html)

## 🎓 Dicas para Contribuidores

### 1. Foco na Certificação

Priorize conteúdo que:
- É cobrado no exame
- Aparece em perguntas frequentes
- É difícil de entender
- Tem pegadinhas comuns

### 2. Exemplos Práticos

- Use casos reais
- Mostre boas práticas
- Inclua anti-patterns
- Explique trade-offs

### 3. Documentação Clara

- Explique o "por quê", não só o "como"
- Use diagramas quando possível
- Inclua links para docs oficiais
- Adicione dicas de exame

## 🙏 Agradecimentos

Obrigado por ajudar outros desenvolvedores a se prepararem para a certificação AWS!

Cada contribuição, por menor que seja, faz diferença na jornada de aprendizado de alguém.

