# 🏫 Sistema de Gestão Escolar

Sistema completo de gestão escolar desenvolvido com FastAPI (backend) e HTML/CSS/JavaScript (frontend).

## 📋 Funcionalidades

### 🔐 Autenticação
- Sistema de login/registro seguro
- JWT Tokens para autenticação
- Controle de sessão (lembrar-me)
- Diferentes níveis de acesso por cargo

### 👥 Gestão de Usuários
- Cadastro de usuários (Diretor, Coordenador, Secretário, Professor)
- Controle de permissões por cargo
- Histórico de login

### 🎓 Gestão de Alunos
- Cadastro completo de alunos
- Status (Ativo, Inativo, Suspenso, Transferido)
- Vinculação com turmas
- Histórico acadêmico

### 📚 Gestão de Turmas
- Criação e edição de turmas
- Controle de capacidade
- Associação de alunos

### 📊 Dashboard
- Estatísticas em tempo real
- Indicadores de performance
- Visão geral do sistema

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Navegador web moderno

### 1. Instalar Dependências
```bash
cd back-end
pip install -r requirements.txt
```

### 2. Inicializar Sistema
```bash
# Opção 1: Script automatizado
python start.py

# Opção 2: Manual
python seed.py  # Popular banco com dados iniciais
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Acessar o Sistema
- **Frontend**: Abra `front-end/login.html` no navegador
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs

## 👤 Usuários de Teste

Após executar o seed, você pode usar estas credenciais:

| Email | Senha | Cargo |
|-------|--------|-------|
| admin@escola.com | 123456 | Diretor |
| maria@escola.com | 123456 | Coordenadora |
| ana@escola.com | 123456 | Secretária |
| joao@escola.com | 123456 | Professor |

## 🏗️ Arquitetura

### Backend (FastAPI)
```
back-end/
├── app.py          # Aplicação principal FastAPI
├── models.py       # Modelos SQLAlchemy
├── schemas.py      # Schemas Pydantic
├── database.py     # Configuração do banco
├── auth.py         # Sistema de autenticação JWT
├── services.py     # Lógica de negócios
├── seed.py         # População inicial do banco
├── start.py        # Script de inicialização
└── requirements.txt # Dependências Python
```

### Frontend (HTML/CSS/JS)
```
front-end/
├── login.html      # Página de login/registro
├── index.html      # Aplicação principal
├── auth-style.css  # Estilos da autenticação
├── style.css       # Estilos principais
├── auth-script.js  # Script de autenticação
└── script.js       # Script principal
```

## 🔧 Tecnologias

### Backend
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para Python
- **SQLite**: Banco de dados
- **JWT**: Autenticação stateless
- **Bcrypt**: Hash de senhas
- **Pydantic**: Validação de dados
- **Uvicorn**: Servidor ASGI

### Frontend
- **HTML5**: Estrutura semântica
- **CSS3**: Design moderno com CSS Variables
- **JavaScript ES6+**: Funcionalidades interativas
- **Fetch API**: Comunicação com backend

## 📱 Interface

### Design Moderno
- ✨ Interface limpa e profissional
- 📱 Totalmente responsiva
- 🎨 Sistema de cores consistente
- 🔄 Animações fluidas
- 📋 Tabelas interativas

### Experiência do Usuário
- 🔍 Busca em tempo real
- 📊 Feedback visual
- ⚡ Carregamento rápido
- 🎯 Navegação intuitiva

## 🔐 Segurança

- **Autenticação JWT**: Tokens seguros com expiração
- **Hash de Senhas**: Bcrypt com salt
- **Validação de Dados**: Pydantic schemas
- **CORS**: Configurado para produção
- **Controle de Acesso**: Por cargo de usuário

## 📈 Funcionalidades por Cargo

### 👑 Diretor
- Acesso total ao sistema
- Gestão de usuários
- Relatórios completos

### 👩‍🏫 Coordenador
- Gestão de turmas e alunos
- Relatórios acadêmicos
- Acompanhamento pedagógico

### 📝 Secretário
- Cadastro de alunos
- Gestão de matrículas
- Documentação

### 👨‍🏫 Professor
- Visualização de turmas
- Consulta de alunos
- Relatórios básicos

## 🛠️ Desenvolvimento

### Estrutura da API
- **Rotas RESTful**: Padrão REST para todas as operações
- **Documentação Automática**: Swagger/OpenAPI
- **Validação**: Schemas Pydantic
- **Tratamento de Erros**: Respostas padronizadas

### Banco de Dados
- **Relacionamentos**: Foreign keys bem definidas
- **Indexes**: Otimização de consultas
- **Enums**: Tipos padronizados
- **Timestamps**: Auditoria de criação/atualização

## 🐛 Resolução de Problemas

### Erro de Conexão
1. Verifique se o backend está rodando na porta 8000
2. Confirme se não há firewall bloqueando
3. Teste o acesso a http://localhost:8000/docs

### Problemas de Login
1. Verifique as credenciais de teste
2. Execute o seed novamente se necessário
3. Limpe o cache do navegador

### Banco de Dados
1. Delete o arquivo `school.db` para resetar
2. Execute `python seed.py` novamente
3. Verifique permissões de escrita na pasta

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação da API em `/docs`
2. Verifique os logs do servidor
3. Teste com dados do seed

---

**Desenvolvido com ❤️ para gestão educacional eficiente**
