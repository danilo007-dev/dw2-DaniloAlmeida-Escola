# 🏫 Sistema de Gestão Escolar - Guia de Setup

## 📋 Pré-requisitos

### Software necessário:
- **Python 3.9+** (recomendado 3.11)
- **Git** para clonar o repositório
- **VS Code** (opcional, mas recomendado)

## 🚀 Passo a Passo para Setup

### 1. Clonar o Repositório
```bash
git clone https://github.com/danilo007-dev/dw2-DaniloAlmeida-Escola.git
cd dw2-DaniloAlmeida-Escola
```

### 2. Setup do Backend

#### 2.1 Navegue para o diretório backend:
```bash
cd back-end
```

#### 2.2 Instale as dependências:
```bash
pip install -r requirements.txt
```

#### 2.3 Inicie o servidor backend:
```bash
python start.py
```
✅ **Servidor rodará em:** http://localhost:8000

### 3. Setup do Frontend

#### 3.1 Abra um novo terminal e navegue para o frontend:
```bash
cd front-end
```

#### 3.2 Inicie o servidor HTTP:
```bash
python -m http.server 8080
```
✅ **Frontend rodará em:** http://localhost:8080

## 🔐 Credenciais de Acesso

### Usuários pré-cadastrados:
- **Diretor:** admin@escola.com | 123456
- **Coordenador:** maria@escola.com | 123456
- **Secretário:** ana@escola.com | 123456
- **Professor:** joao@escola.com | 123456

## 📊 Dados do Sistema

### Banco de dados já populado com:
- ✅ **24 turmas completas** (1º ao 9º ano + Ensino Médio)
- ✅ **10 alunos de exemplo**
- ✅ **4 usuários com diferentes permissões**

### Turmas disponíveis:
- **Ensino Fundamental I:** 1º ao 5º ANO (A e B) - Matutino/Vespertino
- **Ensino Fundamental II:** 6º ao 9º ANO (A e B) - Matutino/Vespertino
- **Ensino Médio:** 1º ao 3º ANO EM (A e B) - Matutino/Vespertino/Noturno

## 🛠️ Solução de Problemas

### Problema: Token inválido ou dados não carregam
**Solução:**
1. Acesse: http://localhost:8080/debug.html
2. Clique em "Limpar Tokens"
3. Clique em "Novo Login"
4. Faça login normalmente

### Problema: Erro de dependências
**Solução:**
```bash
cd back-end
pip install --upgrade pip
pip install -r requirements.txt
```

### Problema: Porta ocupada
**Solução:**
- Backend: Mude a porta no arquivo `start.py`
- Frontend: Use `python -m http.server 8081` (ou outra porta)

## 🔄 Reset do Banco de Dados (se necessário)

Se precisar recriar o banco com dados limpos:
```bash
cd back-end
python reset_db.py
```

## 📁 Estrutura do Projeto

```
dw2-DaniloAlmeida-Escola/
├── back-end/
│   ├── app.py          # API principal
│   ├── start.py        # Servidor de inicialização
│   ├── models.py       # Modelos do banco
│   ├── database.py     # Configuração do banco
│   ├── seed.py         # Dados iniciais
│   └── requirements.txt # Dependências Python
├── front-end/
│   ├── index.html      # Dashboard principal
│   ├── login.html      # Página de login
│   ├── script.js       # JavaScript principal
│   ├── style.css       # Estilos CSS
│   └── debug.html      # Página de debug
└── README.md
```

## ✨ Funcionalidades Implementadas

### 📚 Gestão de Alunos:
- ✅ Cadastro, edição e exclusão
- ✅ Filtros por turma, status e busca
- ✅ Soft delete para alunos ativos
- ✅ Histórico de ações

### 🏫 Gestão de Turmas:
- ✅ Sistema completo de ensino brasileiro
- ✅ Diferentes períodos (Matutino/Vespertino/Noturno)
- ✅ Controle de capacidade

### 👥 Sistema de Usuários:
- ✅ Autenticação JWT
- ✅ Diferentes níveis de acesso
- ✅ Gestão de perfis

### 🎨 Interface:
- ✅ Tema claro/escuro
- ✅ Design responsivo
- ✅ Experiência moderna

### 📊 Relatórios:
- ✅ Estatísticas em tempo real
- ✅ Dashboards informativos
- ✅ Filtros avançados

## 🆘 Contatos de Suporte

Se houver problemas:
1. Verifique os logs no console do navegador
2. Use a página de debug: http://localhost:8080/debug.html
3. Verifique se ambos os servidores estão rodando

## 🎯 Comandos Rápidos

### Iniciar tudo de uma vez (Windows PowerShell):
```powershell
# Terminal 1 - Backend
cd back-end; python start.py

# Terminal 2 - Frontend  
cd front-end; python -m http.server 8080
```

### Iniciar tudo de uma vez (Linux/Mac):
```bash
# Terminal 1 - Backend
cd back-end && python start.py

# Terminal 2 - Frontend
cd front-end && python -m http.server 8080
```

---

## 🚀 Sistema Pronto!

Após seguir estes passos, acesse:
- **Sistema:** http://localhost:8080
- **Login:** admin@escola.com / 123456
- **API Docs:** http://localhost:8000/docs

**O sistema estará 100% funcional com todas as turmas e dados implementados!** 🎉📚