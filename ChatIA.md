# Projeto Escola

Este é o repositório inicial do projeto de desenvolvimento web para a disciplina DW2.

## Estrutura Inicial
- index.html
- style.css
- script.js

## Autor
Danilo Almeida

## Chat AI
25/08
Eu: Olá, bom dia! Eu estou fazendo um projeto escolar e comecei a fazer os primeiros arquivos. Ele está guardado em um repositório no github, mas já fiz o push aqui para adiantar. Você pode me ajudar com o projeto?

AI: Bom dia! Claro, posso te ajudar com o seu projeto escolar. Por favor, me diga qual funcionalidade ou parte do projeto você gostaria de trabalhar agora, ou se há alguma dúvida específica que você tem sobre o código, estrutura ou requisitos.

10/09
Eu: Olá, estou fazendo o projeto de trabalho bimestral da minha escola e aula passada já criei toda a estrutura dos arquivos como você pode ver ao lado, desde o front-end ao back-end e arquivos .md. Nessa aula eu pretendo praticamente finalizar o projeto. Você pode me ajudar de onde parei?

AI: Olá! Claro, posso te ajudar a finalizar seu projeto. Para começar, preciso saber:
- Qual é o objetivo principal do seu sistema?
- Quais funcionalidades você já implementou e quais ainda faltam?
- Você está usando algum framework ou biblioteca específica no back-end (por exemplo, Flask)?
- O front-end está integrado ao back-end ou ainda falta essa parte?
Se quiser, posso analisar os arquivos existentes e sugerir os próximos passos para finalizar o projeto. Me diga como prefere seguir!

Eu: Antes de analisar o código e os arquivos, vou te mandar todas as especificações do projeto, mas ainda não precisa fazer nada

AI: Perfeito! Pode enviar as especificações do projeto quando quiser. Assim que receber, aguardarei suas próximas instruções antes de realizar qualquer ação.

Eu: 1) Objetivo
Construir um mini-sistema web completo com o tema Escola, individual, usando:
• Front-end: HTML5, CSS3 (Flex/Grid), JavaScript (ES6+, sem framework).
• Back-end/API: Python (FastAPI ou Flask), SQLite via SQLAlchemy (ou sqlite3).
• Ferramentas: VS Code, Copilot, Git/GitHub, Thunder Client/Insomnia.
• Entrega: repositório público no GitHub + relatório técnico.

2) Padrão Técnico
• Estrutura de pastas
• /frontend
• index.html
• styles.css
• scripts.js
• /backend
• app.py (FastAPI/Flask)
• models.py
• database.py
• seed.py
• requirements.txt
• README.md
• REPORT.md
• API: RESTful, retornando JSON, status codes (200, 201, 400, 404, 422, 500).
• SQLite: app.db na pasta /backend.
• Seed: script para inserir ~20 registros plausíveis na tabela principal.
• Acessibilidade: aria-label, foco visível, contraste mínimo 4.5:1, navegação por teclado.
• Testes manuais: coleção do Thunder Client/Insomnia ou arquivo .http no repo.
• GitHub: repositório público dw2-<seunome>-<tema>, commits frequentes, tag v1.0.0.

AI: Recebido! Suas especificações estão claras. O projeto deve ser um sistema web escolar, com front-end em HTML/CSS/JS puro e back-end em Python (FastAPI ou Flask) usando SQLite, seguindo boas práticas de estrutura, acessibilidade e testes.
Quando quiser, posso:
- Analisar o que já está pronto nos arquivos.
- Sugerir ou implementar as próximas etapas.
- Validar requisitos técnicos e acessibilidade.
- Ajudar com integração, testes ou documentação.
Me avise como deseja prosseguir!

Eu: Muito obrigado, quero fazer tudo isso. Mas primeiro, analise o que já está pronto nos arquivos

AI: Aqui está o resumo do que já está pronto nos seus arquivos:
Back-end
- app.py: FastAPI configurado, rota GET / retorna mensagem simples.
- models.py: Modelos ORM definidos para Turma e Aluno, com relacionamento e enum de status.
- database.py: Configuração do SQLite com SQLAlchemy, função para criar tabelas.
- seed.py: Arquivo criado, mas ainda sem implementação.
- requirements.txt: Inclui fastapi, uvicorn, sqlalchemy.
Front-end
- index.html: Estrutura básica, título "Projeto Inicial", inclui CSS e JS.
- script.js: Apenas um console.log ao carregar a página.
- style.css: Estilização simples para body e h1.
Situação atual
- Estrutura técnica está correta.
- Modelos e banco prontos para uso.
- Front-end básico, sem integração com API.
- Seed e rotas REST ainda precisam ser implementados.
- Acessibilidade e testes manuais não estão presentes.
Próximos passos sugeridos:
1. Implementar rotas RESTful no back-end (CRUD para Aluno e Turma).
2. Criar o script de seed com ~20 registros.
3. Evoluir o front-end para consumir a API e exibir dados.
4. Adicionar recursos de acessibilidade.
5. Preparar testes manuais e documentação.
Me avise por qual parte deseja começar!

Eu: Vamos começar pelo front-end. Vou mandar as expecificações:
3) Sistemas e Especificações do Front-end
3.3 Escola (Turmas e Matrículas)
Identidade visual
• Primária: #2563EB (azul)
• Secundária: #10B981 (verde)
• Acento: #F97316 (laranja)
• Fundo: #F1F5F9 (cinza claro)
• Texto: #0B1220
• Fonte sugerida: “Roboto” ou “Inter” (sans-serif)
Layout
• Header com “Gestão Escolar” + busca por aluno.
• Duas colunas: à esquerda filtro/estatísticas rápidas; à direita listagem principal.
• Modais para Novo Aluno e Nova Matrícula.
Páginas/Seções
1. Alunos: listagem com filtros (turma, status).
2. Turmas: listagem de turmas com capacidade e ocupação.
3. Relatórios (front): exportar CSV/JSON de alunos ou matrículas.
Formulário de Aluno (front)
• Campos: nome* (3–80), data_nascimento* (date), email (pattern), status* (ativo/inativo), turma_id (select opcional).
• Validações front: required, data válida ≥ 5 anos atrás, email regex, status.
Interações JS
• CRUD via fetch.
• Filtro combinado (turma + status + texto).
• Ordenação por nome/idade.
• Indicadores: total de alunos, ativos, por turma.
• Acessibilidade: foco visível, legenda em tabelas, aria-live para feedback de operações.
Regra de negócio (front + back)
• Ao matricular, não exceder capacidade da turma.
• Alterar status do aluno para “ativo” ao ser matriculado.

AI: Ótimo! Suas especificações do front-end estão detalhadas. Aqui está um plano de ação para começar:
1. Identidade Visual
- Atualizar o CSS com as cores e fonte sugeridas.
2. Estrutura do Layout
- Criar o header com “Gestão Escolar” e campo de busca.
- Implementar layout com duas colunas (filtros/estatísticas à esquerda, listagem à direita).
3. Componentes
- Modais para Novo Aluno e Nova Matrícula.
- Seções para Alunos, Turmas e Relatórios.
4. Formulário de Aluno
- Campos e validações conforme especificado.
5. Interações JS
- Estruturar funções para CRUD, filtros, ordenação e indicadores.
- Garantir acessibilidade (foco, aria-label, aria-live).
Posso começar atualizando o CSS para a identidade visual e preparando o HTML para o layout principal. Deseja que eu faça isso agora?

Eu: Sim, por favor!

AI: O HTML foi atualizado com o layout principal, header, busca, duas colunas, placeholders para listagem, filtros e modais. O CSS foi atualizado para a identidade visual, layout flex, acessibilidade e estilos dos componentes.
No entanto, o CSS apresentou erros de sintaxe devido a linhas antigas que não foram removidas corretamente. Vou corrigir o arquivo style.css para garantir que só o novo código esteja presente e sem erros.

AI: Pronto! O layout e a identidade visual do front-end foram aplicados corretamente. O HTML agora possui header, busca, duas colunas, navegação e modais, e o CSS está limpo, sem erros, com as cores e fontes especificadas.
Se quiser, posso seguir para:
- Implementar os filtros, estatísticas e placeholders de listagem.
- Criar os formulários dos modais.
- Iniciar a integração com a API.
Me avise o próximo passo!

Eu: Antes de continuar, só vamos fazer umas alterações no layout:
- Coloque o campo de buscar aluno de um lado e "Gestão Escolar do Outro"

AI: O header foi ajustado: agora "Gestão Escolar" aparece à esquerda e o campo de busca à direita, alinhados em linha com layout flex.
Se quiser, posso seguir para os próximos ajustes ou implementar novas funcionalidades. Como deseja prosseguir?

Eu: Pode fazer os próximos ajustes e implementar novas funcionalidades.

AI: Ótimo! Vou avançar com os próximos ajustes e funcionalidades do front-end:
1. Adicionar filtros de turma, status e texto na lateral.
2. Exibir estatísticas rápidas (total de alunos, ativos, por turma).
3. Estruturar a listagem principal de alunos.
4. Criar o formulário do modal de novo aluno com validações.
5. Preparar navegação entre Alunos, Turmas e Relatórios.
Vou começar implementando os filtros, estatísticas e a estrutura da listagem principal. Depois sigo para o modal de aluno.

AI: Os filtros, estatísticas e a estrutura da listagem principal de alunos foram adicionados ao HTML. O formulário do modal de novo aluno também foi iniciado com todos os campos e validações básicas.
Próximos passos sugeridos:
- Implementar a lógica JS para preencher filtros, estatísticas e listagem.
- Adicionar navegação entre Alunos, Turmas e Relatórios.
- Finalizar o modal de matrícula.
Deseja que eu avance para a implementação do JavaScript dessas funcionalidades?

Eu: Muito obrigado! Vou continua na próxima aula. Você pode mandar esse chat inteiro para o arquivo ChatIA.md, especificando as minhas e as suas falas no mesmo modelo que já está lá?

AI: Seu arquivo ChatIA.md já possui um histórico de conversa, com as falas separadas por "Eu:" e "AI:". Vou adicionar todo o chat desta aula seguindo o mesmo modelo, mantendo a ordem e clareza das interações. Vou preparar o conteúdo e inserir no final do arquivo, mantendo o padrão.

