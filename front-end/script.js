// Sistema de Gestão Escolar - Script Principal Integrado
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏫 Sistema de Gestão Escolar carregado!');
    
    // Configuração da API
    const API_BASE_URL = 'http://localhost:8000';
    
    // Estado da aplicação
    let currentUser = null;
    let authToken = null;
    let turmasData = [];
    let alunosData = [];
    let usuariosData = [];
    
    // Sistema de Temas
    const ThemeManager = {
        init() {
            // Carregar tema salvo ou usar tema claro como padrão
            const savedTheme = localStorage.getItem('theme') || 'light';
            this.setTheme(savedTheme);
            this.setupThemeToggle();
        },
        
        setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            this.updateThemeToggle(theme);
        },
        
        toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            this.setTheme(newTheme);
        },
        
        updateThemeToggle(theme) {
            const themeToggle = document.getElementById('theme-toggle');
            const themeIcon = themeToggle?.querySelector('.theme-icon');
            const themeText = themeToggle?.querySelector('.theme-text');
            
            if (themeIcon && themeText) {
                if (theme === 'dark') {
                    themeIcon.textContent = '☀️';
                    themeText.textContent = 'Tema Claro';
                } else {
                    themeIcon.textContent = '🌙';
                    themeText.textContent = 'Tema Escuro';
                }
            }
        },
        
        setupThemeToggle() {
            const themeToggle = document.getElementById('theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    this.toggleTheme();
                });
            }
        }
    };
    
    // Elementos DOM
    const userAvatar = document.getElementById('user-avatar');
    const userName = document.getElementById('user-name');
    const userRole = document.getElementById('user-role');
    const logoutBtn = document.getElementById('logout-btn');
    
    // Tabs
    const tabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.content-section');
    
    // Inicialização
    init();
    
    async function init() {
        console.log('🚀 Iniciando sistema...');
        
        // Inicializar sistema de temas
        ThemeManager.init();
        console.log('✅ Temas inicializados');
        
        // Verificar autenticação
        console.log('🔐 Verificando autenticação...');
        if (!checkAuth()) {
            console.log('❌ Falha na autenticação, redirecionando...');
            return;
        }
        console.log('✅ Autenticação OK');
        
        // Carregar dados do usuário
        console.log('👤 Carregando dados do usuário...');
        await loadUserData();
        console.log('✅ Dados do usuário carregados');
        
        // Carregar dados iniciais
        console.log('📊 Carregando dados iniciais...');
        await loadInitialData();
        console.log('✅ Dados iniciais carregados');
        
        // Configurar event listeners
        console.log('🎯 Configurando event listeners...');
        setupEventListeners();
        console.log('✅ Event listeners configurados');
        
        // Configurar monitor do user-role
        console.log('🔍 Configurando monitor do user-role...');
        setupUserRoleMonitor();
        console.log('✅ Monitor configurado');
        
        // Mostrar tab inicial
        console.log('🏠 Mostrando seção de alunos...');
        showTab('section-alunos');
        
        // Adicionar evento de teste para debug
        window.testShowTab = function(tabName) {
            console.log('🧪 Teste manual showTab:', tabName);
            showTab(tabName);
        };
        
        console.log('✅ Sistema inicializado com sucesso!');
    }
    
    function checkAuth() {
        console.log('🔐 Verificando autenticação...');
        authToken = localStorage.getItem('token') || sessionStorage.getItem('token');
        const tokenType = localStorage.getItem('token_type') || sessionStorage.getItem('token_type');
        
        console.log('🔑 Token encontrado:', !!authToken);
        console.log('🏷️ Token type:', tokenType);
        
        if (!authToken) {
            console.log('❌ Sem token, redirecionando para login');
            window.location.href = 'login.html';
            return false;
        }
        
        // Configurar header padrão para requests
        window.authHeader = `${tokenType || 'Bearer'} ${authToken}`;
        console.log('✅ Auth header configurado');
        return true;
    }
    
    async function loadUserData() {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                headers: {
                    'Authorization': window.authHeader
                }
            });
            
            if (response.ok) {
                currentUser = await response.json();
                updateUserInterface();
            } else if (response.status === 401) {
                console.error('❌ Token inválido ou expirado, redirecionando para login...');
                // Limpar tokens inválidos
                localStorage.removeItem('token');
                localStorage.removeItem('token_type');
                sessionStorage.removeItem('token');
                sessionStorage.removeItem('token_type');
                // Redirecionar para login
                window.location.href = 'login.html';
            } else {
                throw new Error('Falha ao carregar dados do usuário');
            }
        } catch (error) {
            console.error('Erro ao carregar usuário:', error);
            showToast('Erro ao carregar dados do usuário', 'error');
        }
    }
    
    function updateUserInterface() {
        if (currentUser) {
            if (userName) userName.textContent = currentUser.nome;
            if (userRole) userRole.textContent = getRoleDisplay(currentUser.cargo);
            if (userAvatar) {
                userAvatar.textContent = currentUser.nome.charAt(0).toUpperCase();
                
                // Definir cor do avatar baseado no cargo
                const avatarColors = {
                    'diretor': 'linear-gradient(135deg, #dc2626 0%, #ef4444 100%)', // Vermelho
                    'coordenador': 'linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)', // Azul
                    'secretario': 'linear-gradient(135deg, #059669 0%, #10b981 100%)', // Verde
                    'professor': 'linear-gradient(135deg, #ea580c 0%, #f97316 100%)' // Laranja
                };
                
                userAvatar.style.background = avatarColors[currentUser.cargo] || avatarColors['secretario'];
            }
        }
    }
    
    function getRoleDisplay(cargo) {
        // Converter para string se for um objeto
        const cargoStr = typeof cargo === 'object' ? cargo.value || cargo : String(cargo);
        
        const roles = {
            'diretor': 'Diretor(a)',
            'coordenador': 'Coordenador(a)',
            'secretario': 'Secretário(a)',
            'professor': 'Professor(a)'
        };
        
        return roles[cargoStr] || cargoStr;
    }
    
    // Debug function para forçar atualização do cargo
    window.debugForceUpdateRole = function() {
        console.log('🔧 [DEBUG] Forçando atualização do cargo...');
        if (currentUser) {
            console.log('👤 [DEBUG] currentUser:', currentUser);
            const roleDisplay = getRoleDisplay(currentUser.cargo);
            console.log('🔍 [DEBUG] roleDisplay:', roleDisplay);
            
            const userRoleElement = document.getElementById('user-role');
            if (userRoleElement) {
                userRoleElement.textContent = roleDisplay;
                console.log('✅ [DEBUG] Cargo atualizado forçadamente para:', roleDisplay);
            }
        } else {
            console.log('❌ [DEBUG] currentUser não está definido');
        }
    };
    
    // Debug function
    window.debugAlunosData = function() {
        console.log('🔍 DEBUG - Estado atual dos dados:');
        console.log('📊 alunosData:', alunosData);
        console.log('📊 turmasData:', turmasData);
        console.log('🎯 editandoAlunoId:', editandoAlunoId);
        
        const tbody = document.querySelector('#tabela-alunos tbody');
        console.log('📋 Tbody elemento:', tbody);
        console.log('📋 Tbody conteúdo:', tbody?.innerHTML?.substring(0, 200) + '...');
        
        if (alunosData && alunosData.length > 0) {
            console.log('✅ Dados disponíveis - Re-renderizando...');
            renderAlunosTable();
        } else {
            console.log('❌ Nenhum dado disponível');
        }
    };
    
    async function loadInitialData() {
        try {
            // Carregar em paralelo
            await Promise.all([
                loadTurmas(),
                loadAlunos(),
                loadUsuarios(),
                loadDashboardStats()
            ]);
        } catch (error) {
            console.error('Erro ao carregar dados iniciais:', error);
            showToast('Erro ao carregar dados', 'error');
        }
    }
    
    async function loadTurmas() {
        console.log('🔄 Carregando turmas...');
        console.log('🔑 Auth header:', window.authHeader);
        try {
            const response = await fetch(`${API_BASE_URL}/turmas`, {
                headers: {
                    'Authorization': window.authHeader
                }
            });
            
            console.log('📡 Response status:', response.status);
            
            if (response.ok) {
                turmasData = await response.json();
                console.log('✅ Turmas carregadas:', turmasData.length);
                console.log('📚 Turmas:', turmasData);
                renderTurmasTable();
                
                // Atualizar dropdowns após carregar turmas
                loadFiltroTurmas();
                loadTurmasSelect();
            } else {
                const errorText = await response.text();
                console.error('❌ Erro na resposta:', response.status, errorText);
            }
        } catch (error) {
            console.error('❌ Erro ao carregar turmas:', error);
        }
    }
    
    async function loadAlunos() {
        console.log('🔄 Carregando alunos...');
        console.log('🔑 Auth header:', window.authHeader);
        try {
            const response = await fetch(`${API_BASE_URL}/alunos`, {
                headers: {
                    'Authorization': window.authHeader
                }
            });
            
            console.log('📡 Response status alunos:', response.status);
            
            if (response.ok) {
                alunosData = await response.json();
                console.log('✅ Alunos carregados:', alunosData.length);
                console.log('🎓 Alunos:', alunosData);
                renderAlunosTable();
            } else {
                const errorText = await response.text();
                console.error('❌ Erro na resposta alunos:', response.status, errorText);
            }
        } catch (error) {
            console.error('❌ Erro ao carregar alunos:', error);
        }
    }
    
    async function loadUsuarios() {
        try {
            const response = await fetch(`${API_BASE_URL}/users`, {
                headers: {
                    'Authorization': window.authHeader
                }
            });
            
            if (response.ok) {
                usuariosData = await response.json();
                renderUsuariosTable();
            }
        } catch (error) {
            console.error('Erro ao carregar usuários:', error);
        }
    }
    
    async function loadDashboardStats() {
        try {
            const response = await fetch(`${API_BASE_URL}/statistics`, {
                headers: {
                    'Authorization': window.authHeader
                }
            });
            
            if (response.ok) {
                const stats = await response.json();
                updateDashboardStats(stats);
            }
        } catch (error) {
            console.error('Erro ao carregar estatísticas:', error);
        }
    }
    
    function updateDashboardStats(stats) {
        console.log('Atualizando estatísticas:', stats);
        
        const elements = {
            'total-alunos': stats.total_alunos,
            'alunos-ativos': stats.alunos_ativos,
            'total-turmas': stats.total_turmas,
            'total-usuarios': stats.usuarios_ativos
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
                console.log(`Atualizando ${id} com valor:`, value);
            } else {
                console.warn(`Elemento não encontrado: ${id}`);
            }
        });
        
        // Atualizar lista de alunos por turma
        const alunosPorTurmaElement = document.getElementById('alunos-por-turma');
        if (alunosPorTurmaElement && stats.alunos_por_turma) {
            alunosPorTurmaElement.innerHTML = stats.alunos_por_turma.map(item => 
                `<li class="stat-list-item">
                    <span class="turma-nome">${item.turma}</span>
                    <span class="turma-count">${item.total}</span>
                </li>`
            ).join('');
        }
    }
    
    function renderTurmasSection() {
        console.log('🎨 Renderizando seção de turmas...');
        renderTurmasStats();
        renderTurmasTable();
    }

    function renderTurmasStats() {
        if (!turmasData || turmasData.length === 0) return;
        
        const totalTurmas = turmasData.length;
        const totalAlunosMatriculados = turmasData.reduce((sum, turma) => sum + (turma.total_alunos || 0), 0);
        const capacidadeTotal = turmasData.reduce((sum, turma) => sum + turma.capacidade, 0);
        const ocupacaoMedia = capacidadeTotal > 0 ? Math.round((totalAlunosMatriculados / capacidadeTotal) * 100) : 0;
        
        // Atualizar cards de estatísticas
        const totalTurmasEl = document.getElementById('total-turmas-display');
        const totalAlunosEl = document.getElementById('total-alunos-turmas');
        const ocupacaoMediaEl = document.getElementById('ocupacao-media');
        
        if (totalTurmasEl) totalTurmasEl.textContent = totalTurmas;
        if (totalAlunosEl) totalAlunosEl.textContent = totalAlunosMatriculados;
        if (ocupacaoMediaEl) ocupacaoMediaEl.textContent = `${ocupacaoMedia}%`;
    }

    function renderTurmasTable() {
        const tbody = document.querySelector('#turmas-table tbody');
        if (!tbody || !turmasData) return;
        
        tbody.innerHTML = turmasData.map(turma => {
            const totalAlunos = turma.total_alunos || 0;
            const capacidade = turma.capacidade;
            const ocupacao = capacidade > 0 ? Math.round((totalAlunos / capacidade) * 100) : 0;
            const ocupacaoClass = getOcupacaoClass(ocupacao);
            const periodoIcon = getPeriodoIcon(turma.periodo);
            
            return `
                <tr>
                    <td>
                        <div class="turma-info">
                            <strong>${turma.nome}</strong>
                            <small>${turma.ano_letivo}</small>
                        </div>
                    </td>
                    <td>${turma.descricao || '-'}</td>
                    <td class="text-center">${capacidade}</td>
                    <td>
                        <div class="ocupacao-info">
                            <div class="ocupacao-bar">
                                <div class="ocupacao-fill ${ocupacaoClass}" style="width: ${ocupacao}%"></div>
                            </div>
                            <span class="ocupacao-text ${ocupacaoClass}">${totalAlunos}/${capacidade}</span>
                        </div>
                    </td>
                    <td>
                        <span class="periodo-badge">
                            ${periodoIcon} ${formatPeriodo(turma.periodo)}
                        </span>
                    </td>
                    <td>
                        <div class="taxa-ocupacao ${ocupacaoClass}">
                            ${ocupacao}%
                        </div>
                    </td>
                    <td>
                        <div class="actions-group">
                            <button class="btn-action edit-turma" data-id="${turma.id}" title="Editar Turma">✏️</button>
                            <button class="btn-action delete-turma" data-id="${turma.id}" title="Excluir Turma">🗑️</button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }

    function getOcupacaoClass(ocupacao) {
        if (ocupacao >= 100) return 'lotada';
        if (ocupacao >= 80) return 'alta';
        if (ocupacao >= 50) return 'media';
        return 'baixa';
    }

    function getPeriodoIcon(periodo) {
        const icons = {
            'matutino': '🌅',
            'vespertino': '🌤️',
            'noturno': '🌙',
            'integral': '⏰'
        };
        return icons[periodo] || '📅';
    }

    function formatPeriodo(periodo) {
        const formatted = {
            'matutino': 'Matutino',
            'vespertino': 'Vespertino', 
            'noturno': 'Noturno',
            'integral': 'Integral'
        };
        return formatted[periodo] || periodo;
    }
    
    function renderAlunosTable() {
        console.log('🎨 Renderizando tabela de alunos...');
        
        // Carregar opções de turmas no filtro
        loadFiltroTurmas();
        
        // Aplicar filtros (que renderiza a tabela)
        aplicarFiltros();
        console.log('✅ Tabela renderizada com filtros aplicados!');
    }
    
    function renderUsuariosTable() {
        const tbody = document.querySelector('#usuarios-table tbody');
        if (!tbody || !usuariosData) return;
        
        tbody.innerHTML = usuariosData.map(usuario => `
            <tr>
                <td>${usuario.nome}</td>
                <td>${usuario.email}</td>
                <td>${getRoleDisplay(usuario.cargo)}</td>
                <td>
                    <span class="status ${usuario.ativo ? 'ativo' : 'inativo'}">
                        ${usuario.ativo ? 'Ativo' : 'Inativo'}
                    </span>
                </td>
                <td>${formatDateTime(usuario.criado_em)}</td>
                <td>
                    <button class="btn-action edit-usuario" data-id="${usuario.id}">✏️</button>
                    ${usuario.id !== currentUser?.id ? `<button class="btn-action delete-usuario" data-id="${usuario.id}">🗑️</button>` : ''}
                </td>
            </tr>
        `).join('');
    }
    
    function getStatusDisplay(status) {
        const statuses = {
            'ativo': 'Ativo',
            'inativo': 'Inativo',
            'suspenso': 'Suspenso',
            'transferido': 'Transferido'
        };
        return statuses[status] || status;
    }
    
    function formatDate(dateString) {
        if (!dateString) return '';
        
        // Corrigir problema de fuso horário para datas no formato YYYY-MM-DD
        const [year, month, day] = dateString.split('-');
        const date = new Date(year, month - 1, day); // Criar data local
        
        return date.toLocaleDateString('pt-BR');
    }
    
    function formatDateTime(dateString) {
        if (!dateString) return '';
        return new Date(dateString).toLocaleString('pt-BR');
    }
    
    function setupEventListeners() {
        // Tabs
        console.log('🎯 Configurando event listeners para tabs...');
        console.log('📊 Número de tabs encontradas:', tabs.length);
        
        tabs.forEach((tab, index) => {
            const tabName = tab.getAttribute('data-tab');
            const tabText = tab.textContent.trim();
            console.log(`🔗 Tab ${index + 1}: "${tabText}" -> ${tabName}`);
            
            tab.addEventListener('click', () => {
                const targetTab = tab.getAttribute('data-tab');
                console.log('🖱️ Click na tab:', tabText, '-> Alvo:', targetTab);
                showTab(targetTab);
            });
        });
        
        // User dropdown
        const userDropdownBtn = document.getElementById('user-dropdown-btn');
        const userDropdown = document.getElementById('user-dropdown');
        const userInfo = document.querySelector('.user-info');
        
        if (userDropdownBtn && userDropdown) {
            userInfo.addEventListener('click', (e) => {
                e.stopPropagation();
                userDropdown.classList.toggle('show');
            });
            
            // Fechar dropdown ao clicar fora
            document.addEventListener('click', () => {
                userDropdown.classList.remove('show');
            });
            
            // Prevenir fechamento ao clicar no dropdown
            userDropdown.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }
        
        // User menu actions
        const userProfile = document.getElementById('user-profile');
        const userSettings = document.getElementById('user-settings');
        
        if (userProfile) {
            userProfile.addEventListener('click', () => {
                showToast('Funcionalidade de perfil em desenvolvimento', 'info');
                userDropdown.classList.remove('show');
            });
        }
        
        if (userSettings) {
            userSettings.addEventListener('click', () => {
                showToast('Funcionalidade de configurações em desenvolvimento', 'info');
                userDropdown.classList.remove('show');
            });
        }
        
        // Logout
        if (logoutBtn) {
            logoutBtn.addEventListener('click', logout);
        }
        
        // Botão Novo Aluno
        const btnNovoAluno = document.getElementById('btn-novo-aluno');
        if (btnNovoAluno) {
            btnNovoAluno.addEventListener('click', openModalAluno);
        }
        
        // Botão Nova Turma
        const btnNovaTurma = document.getElementById('btn-nova-turma');
        if (btnNovaTurma) {
            btnNovaTurma.addEventListener('click', openModalTurma);
        }
        
        // Busca de Turmas
        const buscaTurma = document.getElementById('busca-turma');
        if (buscaTurma) {
            buscaTurma.addEventListener('input', filtrarTurmas);
        }
        
        // Modal Aluno
        setupModalAluno();
        
        // Modal Turma
        setupModalTurma();
        
        // Event listeners para ações da tabela
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('edit-aluno')) {
                const alunoId = e.target.getAttribute('data-id');
                editarAluno(alunoId);
            } else if (e.target.classList.contains('delete-aluno')) {
                const alunoId = e.target.getAttribute('data-id');
                excluirAluno(alunoId);
            } else if (e.target.classList.contains('edit-turma')) {
                const turmaId = e.target.getAttribute('data-id');
                editarTurma(turmaId);
            } else if (e.target.classList.contains('delete-turma')) {
                const turmaId = e.target.getAttribute('data-id');
                excluirTurma(turmaId);
            }
        });
        
        // Refresh buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-refresh')) {
                loadInitialData();
            }
        });
        
        // Setup dos filtros
        setupFilters();
    }
    
    // Filtros e busca
    function setupFilters() {
        const filtroTurma = document.getElementById('filtro-turma');
        const filtroStatus = document.getElementById('filtro-status');
        const filtroTexto = document.getElementById('filtro-texto');
        const buscaAluno = document.getElementById('busca-aluno');
        
        // Event listeners para filtros
        if (filtroTurma) {
            filtroTurma.addEventListener('change', aplicarFiltros);
        }
        
        if (filtroStatus) {
            filtroStatus.addEventListener('change', aplicarFiltros);
        }
        
        if (filtroTexto) {
            filtroTexto.addEventListener('input', aplicarFiltros);
        }
        
        if (buscaAluno) {
            buscaAluno.addEventListener('input', aplicarFiltros);
        }
        
        // Carregar opções de turmas no filtro
        loadFiltroTurmas();
    }
    
    function loadFiltroTurmas() {
        console.log('📋 Carregando filtro de turmas...');
        const filtroTurma = document.getElementById('filtro-turma');
        if (!filtroTurma) {
            console.log('❌ Elemento filtro-turma não encontrado');
            return;
        }
        if (!turmasData) {
            console.log('❌ turmasData não está disponível');
            return;
        }
        
        console.log('🔄 Populando filtro com', turmasData.length, 'turmas');
        
        // Limpar opções existentes exceto a primeira
        filtroTurma.innerHTML = '<option value="">Todas as turmas</option>';
        
        // Adicionar turmas
        turmasData.forEach(turma => {
            const option = document.createElement('option');
            option.value = turma.id;
            option.textContent = turma.nome;
            filtroTurma.appendChild(option);
        });
        
        console.log('✅ Filtro de turmas atualizado!');
    }
    
    function aplicarFiltros() {
        if (!alunosData) {
            console.log('⚠️ alunosData não está disponível!');
            return;
        }
        
        const filtroTurmaValue = document.getElementById('filtro-turma')?.value || '';
        const filtroStatusValue = document.getElementById('filtro-status')?.value || '';
        const filtroTextoValue = document.getElementById('filtro-texto')?.value.toLowerCase() || '';
        const buscaAlunoValue = document.getElementById('busca-aluno')?.value.toLowerCase() || '';
        
        // Combinar texto de busca dos dois campos
        const textoCompleto = (filtroTextoValue + ' ' + buscaAlunoValue).trim();
        
        const alunosFiltrados = alunosData.filter(aluno => {
            // Filtro por turma
            const passaTurma = !filtroTurmaValue || aluno.turma_id == filtroTurmaValue;
            
            // Filtro por status
            const passaStatus = !filtroStatusValue || aluno.status === filtroStatusValue;
            
            // Filtro por texto (nome, email, turma)
            let passaTexto = true;
            if (textoCompleto) {
                const nomeMatch = aluno.nome.toLowerCase().includes(textoCompleto);
                const emailMatch = aluno.email && aluno.email.toLowerCase().includes(textoCompleto);
                const turmaMatch = aluno.turma_nome && aluno.turma_nome.toLowerCase().includes(textoCompleto);
                passaTexto = nomeMatch || emailMatch || turmaMatch;
            }
            
            return passaTurma && passaStatus && passaTexto;
        });
        
        // Renderizar tabela filtrada
        renderAlunosTableFiltrada(alunosFiltrados);
    }
    
    function renderAlunosTableFiltrada(alunosFiltrados) {
        const tbody = document.querySelector('#tabela-alunos tbody');
        if (!tbody) {
            console.log('❌ Elemento tbody não encontrado!');
            return;
        }
        
        // Ordenar alunos por nome em ordem alfabética
        const alunosOrdenados = [...alunosFiltrados].sort((a, b) => 
            a.nome.localeCompare(b.nome, 'pt-BR', { sensitivity: 'base' })
        );
        
        tbody.innerHTML = alunosOrdenados.map(aluno => `
            <tr>
                <td>${aluno.nome}</td>
                <td>${formatDate(aluno.data_nascimento)}</td>
                <td>${aluno.email || 'Não informado'}</td>
                <td>
                    <span class="status ${aluno.status}">${getStatusDisplay(aluno.status)}</span>
                </td>
                <td>${aluno.turma_nome || 'Sem turma'}</td>
                <td>
                    <button class="btn-action edit-aluno" data-id="${aluno.id}" title="Editar Aluno">✏️</button>
                    <button class="btn-action delete-aluno" data-id="${aluno.id}" title="Excluir Aluno">🗑️</button>
                </td>
            </tr>
        `).join('');
        
        // Mostrar contador de resultados
        const total = alunosFiltrados.length;
        const totalGeral = alunosData.length;
        
        // Atualizar indicador de filtros (se existir)
        const indicator = document.getElementById('filter-indicator');
        if (indicator) {
            if (total === totalGeral) {
                indicator.textContent = `Exibindo todos os ${total} alunos`;
            } else {
                indicator.textContent = `Exibindo ${total} de ${totalGeral} alunos`;
            }
        }
    }
    
    // Funções do Modal de Aluno
    function openModalAluno() {
        const modal = document.getElementById('modal-aluno');
        const form = document.getElementById('form-aluno');
        
        if (modal && form) {
            // Resetar modo de edição
            editandoAlunoId = null;
            
            // Resetar título e botão
            document.getElementById('titulo-modal-aluno').textContent = '✨ Novo Aluno';
            document.getElementById('salvar-aluno').textContent = '💾 Salvar Aluno';
            
            // Limpar formulário
            form.reset();
            
            // Carregar turmas e mostrar modal
            loadTurmasSelect().then(() => {
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
                
                const nomeInput = document.getElementById('nome');
                if (nomeInput) {
                    setTimeout(() => nomeInput.focus(), 100);
                }
            });
        }
    }
    
    function closeModalAluno() {
        const modal = document.getElementById('modal-aluno');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            
            // Limpar estado de edição
            editandoAlunoId = null;
            
            // Resetar título e botão
            document.getElementById('titulo-modal-aluno').textContent = '✨ Novo Aluno';
            document.getElementById('salvar-aluno').textContent = '💾 Salvar Aluno';
        }
    }
    
    function setupModalAluno() {
        const modal = document.getElementById('modal-aluno');
        const fecharModal = document.getElementById('fechar-modal-aluno');
        const cancelarBtn = document.getElementById('cancelar-aluno');
        const form = document.getElementById('form-aluno');
        
        // Fechar modal
        if (fecharModal) {
            fecharModal.addEventListener('click', closeModalAluno);
        }
        
        if (cancelarBtn) {
            cancelarBtn.addEventListener('click', closeModalAluno);
        }
        
        // Fechar ao clicar fora do modal
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    closeModalAluno();
                }
            });
        }
        
        // Fechar com ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal && modal.style.display === 'flex') {
                closeModalAluno();
            }
        });
        
        // Submit do formulário
        if (form) {
            form.addEventListener('submit', handleSubmitAluno);
        }
    }
    
    // Variável para controlar modo de edição
    let editandoAlunoId = null;
    
    async function editarAluno(alunoId) {
        console.log('Editando aluno ID:', alunoId);
        try {
            // Buscar dados do aluno
            console.log('Fazendo requisição para:', `${API_BASE_URL}/alunos/${alunoId}`);
            console.log('Authorization header:', window.authHeader);
            
            const response = await fetch(`${API_BASE_URL}/alunos/${alunoId}`, {
                headers: {
                    'Authorization': window.authHeader
                }
            });
            
            console.log('Response status:', response.status);
            
            if (response.ok) {
                const aluno = await response.json();
                console.log('Dados do aluno recebidos:', aluno);
                
                // Definir modo de edição
                editandoAlunoId = alunoId;
                console.log('Modo de edição ativado para ID:', editandoAlunoId);
                
                // Preencher formulário
                document.getElementById('nome').value = aluno.nome || '';
                document.getElementById('data_nascimento').value = aluno.data_nascimento || '';
                document.getElementById('email').value = aluno.email || '';
                document.getElementById('status').value = aluno.status || 'ativo';
                document.getElementById('turma_id').value = aluno.turma_id || '';
                
                // Alterar título e botão do modal
                document.getElementById('titulo-modal-aluno').textContent = '✏️ Editar Aluno';
                document.getElementById('salvar-aluno').textContent = '💾 Atualizar Aluno';
                
                // Abrir modal
                const modal = document.getElementById('modal-aluno');
                if (modal) {
                    // Carregar turmas antes de abrir
                    await loadTurmasSelect();
                    modal.style.display = 'flex';
                    document.body.style.overflow = 'hidden';
                    
                    const nomeInput = document.getElementById('nome');
                    if (nomeInput) {
                        setTimeout(() => nomeInput.focus(), 100);
                    }
                }
            } else {
                const errorText = await response.text();
                console.error('Erro na resposta:', errorText);
                showToast('Erro ao carregar dados do aluno', 'error');
            }
        } catch (error) {
            console.error('Erro ao carregar aluno:', error);
            showToast('Erro ao carregar dados do aluno', 'error');
        }
    }
    
    async function excluirAluno(alunoId) {
        console.log('Excluindo aluno ID:', alunoId);
        
        // Encontrar o nome do aluno para confirmar
        const aluno = alunosData.find(a => a.id == alunoId);
        const nomeAluno = aluno ? aluno.nome : 'este aluno';
        const statusAluno = aluno ? aluno.status : 'ativo';
        
        console.log('Nome do aluno encontrado:', nomeAluno);
        console.log('Status do aluno:', statusAluno);
        
        // Mensagem diferente baseada no status
        let mensagemConfirmacao;
        if (statusAluno === 'inativo') {
            mensagemConfirmacao = `⚠️ ATENÇÃO: ${nomeAluno} já está inativo.\n\nEsta ação irá EXCLUIR PERMANENTEMENTE o aluno do sistema!\n\nTem certeza que deseja continuar? Esta ação não pode ser desfeita.`;
        } else {
            mensagemConfirmacao = `${nomeAluno} será marcado como INATIVO.\n\nPara excluir permanentemente, você precisará clicar novamente após inativar.\n\nDeseja continuar?`;
        }
        
        if (confirm(mensagemConfirmacao)) {
            try {
                console.log('Fazendo DELETE para:', `${API_BASE_URL}/alunos/${alunoId}`);
                console.log('Authorization header:', window.authHeader);
                
                const response = await fetch(`${API_BASE_URL}/alunos/${alunoId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': window.authHeader
                    }
                });
                
                console.log('Response status:', response.status);
                
                if (response.ok) {
                    const responseData = await response.json();
                    console.log('Resposta da API:', responseData);
                    
                    // Mostrar mensagem baseada na resposta da API
                    showToast(responseData.message, 'success');
                    await loadAlunos();
                    await loadDashboardStats();
                } else {
                    const errorData = await response.json();
                    console.error('Erro na API:', errorData);
                    showToast(`Erro ao excluir aluno: ${errorData.detail || 'Erro desconhecido'}`, 'error');
                }
            } catch (error) {
                console.error('Erro ao excluir aluno:', error);
                showToast('Erro ao excluir aluno. Tente novamente.', 'error');
            }
        }
    }

    async function handleSubmitAluno(e) {
        console.log('🚀 handleSubmitAluno chamado!');
        console.log('📝 Event:', e);
        
        e.preventDefault();
        
        console.log('📋 Submit do formulário de aluno');
        console.log('🔧 Modo de edição ID:', editandoAlunoId);
        
        const formData = new FormData(e.target);
        console.log('📊 FormData criado:', formData);
        
        const alunoData = {
            nome: formData.get('nome'),
            data_nascimento: formData.get('data_nascimento'),
            email: formData.get('email'),
            status: formData.get('status'),
            turma_id: parseInt(formData.get('turma_id')) || null
        };
        
        console.log('💾 Dados do formulário:', alunoData);
        
        try {
            let response;
            let mensagemSucesso;
            
            if (editandoAlunoId) {
                // Modo edição
                console.log('Fazendo PUT para atualizar aluno:', editandoAlunoId);
                response = await fetch(`${API_BASE_URL}/alunos/${editandoAlunoId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': window.authHeader
                    },
                    body: JSON.stringify(alunoData)
                });
                mensagemSucesso = 'Aluno atualizado com sucesso!';
            } else {
                // Modo criação
                console.log('Fazendo POST para criar novo aluno');
                response = await fetch(`${API_BASE_URL}/alunos`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': window.authHeader
                    },
                    body: JSON.stringify(alunoData)
                });
                mensagemSucesso = 'Aluno cadastrado com sucesso!';
            }
            
            console.log('Response status:', response.status);
            
            if (response.ok) {
                const responseData = await response.json();
                console.log('Resposta da API:', responseData);
                showToast(mensagemSucesso, 'success');
                closeModalAluno();
                
                // Recarregar dados de forma mais robusta
                console.log('Recarregando dados após operação...');
                
                // Primeiro, limpar dados existentes
                alunosData = null;
                
                // Recarregar dados
                await loadAlunos();
                await loadDashboardStats();
                
                console.log('Dados recarregados. Verificando alunosData:', alunosData);
                
                // Garantir que a tabela seja atualizada
                if (alunosData) {
                    console.log('✅ Dados disponíveis, renderizando tabela...');
                    renderAlunosTable();
                } else {
                    console.log('❌ Erro: alunosData ainda está vazio após recarregar');
                }
                
                console.log('✅ Processo de atualização concluído!');
            } else {
                const errorData = await response.json();
                console.error('Erro na API:', errorData);
                const operacao = editandoAlunoId ? 'atualizar' : 'cadastrar';
                showToast(`Erro ao ${operacao} aluno: ${errorData.detail || 'Erro desconhecido'}`, 'error');
            }
        } catch (error) {
            const operacao = editandoAlunoId ? 'atualizar' : 'cadastrar';
            console.error(`Erro ao ${operacao} aluno:`, error);
            showToast(`Erro ao ${operacao} aluno. Tente novamente.`, 'error');
        }
    }
    
    function loadTurmasSelect() {
        console.log('📝 Carregando dropdown de turmas no modal...');
        const turmaSelect = document.getElementById('turma_id');
        if (!turmaSelect) {
            console.log('❌ Elemento turma_id não encontrado');
            return Promise.resolve();
        }
        
        return new Promise(resolve => {
            // Limpar opções existentes exceto a primeira
            turmaSelect.innerHTML = '<option value="">Selecione uma turma</option>';
            
            console.log('📊 turmasData disponível:', !!turmasData, 'com', turmasData?.length || 0, 'turmas');
            
            // Adicionar turmas disponíveis
            if (turmasData && turmasData.length > 0) {
                turmasData.forEach(turma => {
                    const option = document.createElement('option');
                    option.value = turma.id;
                    option.textContent = `${turma.nome} (${turma.periodo})`;
                    turmaSelect.appendChild(option);
                });
                console.log('✅ Dropdown de turmas atualizado com', turmasData.length, 'opções');
            } else {
                console.log('⚠️ Nenhuma turma disponível para o dropdown');
            }
            resolve();
        });
    }

    function showTab(tabName) {
        console.log('🚀 showTab chamada com:', tabName);
        
        // Remove active from all tabs and hide all content sections  
        console.log('🔄 Removendo active de todas as tabs...');
        tabs.forEach(tab => tab.classList.remove('active'));
        
        console.log('👁️ Escondendo todas as sections...');
        console.log('📊 Número de content sections:', tabContents.length);
        tabContents.forEach((content, index) => {
            console.log(`   Section ${index + 1}: ${content.id} -> escondendo`);
            content.style.display = 'none';
            content.classList.add('hidden');
        });
        
        // Add active to selected tab and show content
        const selectedTab = document.querySelector(`[data-tab="${tabName}"]`);
        const selectedContent = document.getElementById(tabName);
        
        console.log('🎯 Tab selecionada:', selectedTab);
        console.log('📄 Content selecionado:', selectedContent);
        
        if (selectedTab) {
            selectedTab.classList.add('active');
            console.log('✅ Tab marcada como active');
        } else {
            console.log('❌ Tab não encontrada!');
        }
        
        if (selectedContent) {
            selectedContent.classList.remove('hidden');
            selectedContent.style.display = 'block';
            console.log('✅ Content exibido');
            
            // Carregar dados específicos da seção
            if (tabName === 'section-turmas') {
                console.log('🏫 Renderizando seção de turmas...');
                renderTurmasSection();
            } else if (tabName === 'section-alunos') {
                console.log('👥 Renderizando seção de alunos...');
                renderAlunosTable();
            }
        } else {
            console.log('❌ Content não encontrado!');
        }
    }
    
    function logout() {
        // Limpar storage
        localStorage.removeItem('token');
        localStorage.removeItem('token_type');
        sessionStorage.removeItem('token');
        sessionStorage.removeItem('token_type');
        
        showToast('Logout realizado com sucesso!', 'success');
        
        // Redirecionar após delay
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1000);
    }
    
    function showToast(message, type = 'info') {
        // Criar toast element
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${getToastIcon(type)}</span>
            <span class="toast-message">${message}</span>
            <button class="toast-close">×</button>
        `;
        
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
        
        // Manual close
        toast.querySelector('.toast-close').addEventListener('click', () => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        });
    }
    
    function getToastIcon(type) {
        const icons = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        };
        return icons[type] || 'ℹ️';
    }
    
    // Função para monitorar e corrigir mudanças no user-role
    function setupUserRoleMonitor() {
        const userRoleElement = document.getElementById('user-role');
        if (!userRoleElement) return;
        
        console.log('🔍 [MONITOR] Configurando monitor para user-role');
        
        // MutationObserver para detectar mudanças no conteúdo
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList' || mutation.type === 'characterData') {
                    const currentText = userRoleElement.textContent;
                    console.log('🚨 [MONITOR] Mudança detectada no user-role:', currentText);
                    
                    // Se for "Secretário(a)" e temos dados do usuário, corrigir
                    if (currentText === 'Secretário(a)' && currentUser && currentUser.cargo) {
                        console.log('🛠️ [MONITOR] Corrigindo cargo incorreto');
                        const correctRole = getRoleDisplay(currentUser.cargo);
                        userRoleElement.textContent = correctRole;
                        console.log('✅ [MONITOR] Cargo corrigido para:', correctRole);
                    }
                }
            });
        });
        
        // Observar mudanças no conteúdo
        observer.observe(userRoleElement, {
            childList: true,
            subtree: true,
            characterData: true
        });
        
        console.log('✅ [MONITOR] Monitor ativo');
        
        // Também configurar um interval para verificação periódica
        setInterval(() => {
            if (userRoleElement && currentUser) {
                const currentText = userRoleElement.textContent;
                const expectedText = getRoleDisplay(currentUser.cargo);
                
                if (currentText !== expectedText) {
                    console.log('🔄 [INTERVAL] Discrepância detectada. Atual:', currentText, 'Esperado:', expectedText);
                    userRoleElement.textContent = expectedText;
                    console.log('✅ [INTERVAL] Corrigido para:', expectedText);
                }
            }
        }, 1000); // Verificar a cada 1 segundo
    }
    
    // Expor funções globais para uso em modals/forms
    window.schoolSystem = {
        loadTurmas,
        loadAlunos,
        loadUsuarios,
        loadDashboardStats,
        showToast,
        renderTurmasSection,
        authHeader: () => window.authHeader,
        currentUser: () => currentUser,
        API_BASE_URL
    };
    
    // ================================
    // GERENCIAMENTO DE TURMAS
    // ================================

    function filtrarTurmas() {
        const termo = document.getElementById('busca-turma').value.toLowerCase();
        
        if (!termo) {
            renderTurmasTable(); // Mostrar todas as turmas
            return;
        }
        
        const turmasFiltradas = turmasData.filter(turma => 
            turma.nome.toLowerCase().includes(termo) ||
            (turma.descricao && turma.descricao.toLowerCase().includes(termo)) ||
            turma.periodo.toLowerCase().includes(termo)
        );
        
        // Renderizar tabela com turmas filtradas
        const tbody = document.querySelector('#turmas-table tbody');
        if (!tbody) return;
        
        tbody.innerHTML = turmasFiltradas.map(turma => {
            const totalAlunos = turma.total_alunos || 0;
            const capacidade = turma.capacidade;
            const ocupacao = capacidade > 0 ? Math.round((totalAlunos / capacidade) * 100) : 0;
            const ocupacaoClass = getOcupacaoClass(ocupacao);
            const periodoIcon = getPeriodoIcon(turma.periodo);
            
            return `
                <tr>
                    <td>
                        <div class="turma-info">
                            <strong>${turma.nome}</strong>
                            <small>${turma.ano_letivo}</small>
                        </div>
                    </td>
                    <td>${turma.descricao || '-'}</td>
                    <td class="text-center">${capacidade}</td>
                    <td>
                        <div class="ocupacao-info">
                            <div class="ocupacao-bar">
                                <div class="ocupacao-fill ${ocupacaoClass}" style="width: ${ocupacao}%"></div>
                            </div>
                            <span class="ocupacao-text ${ocupacaoClass}">${totalAlunos}/${capacidade}</span>
                        </div>
                    </td>
                    <td>
                        <span class="periodo-badge">
                            ${periodoIcon} ${formatPeriodo(turma.periodo)}
                        </span>
                    </td>
                    <td>
                        <div class="taxa-ocupacao ${ocupacaoClass}">
                            ${ocupacao}%
                        </div>
                    </td>
                    <td>
                        <div class="actions-group">
                            <button class="btn-action edit-turma" data-id="${turma.id}" title="Editar Turma">✏️</button>
                            <button class="btn-action delete-turma" data-id="${turma.id}" title="Excluir Turma">🗑️</button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }

    function openModalTurma(turmaId = null) {
        const modal = document.getElementById('modal-turma');
        const titulo = document.getElementById('titulo-modal-turma');
        const form = document.getElementById('form-turma');
        
        if (turmaId) {
            titulo.textContent = '✏️ Editar Turma';
            const turma = turmasData.find(t => t.id == turmaId);
            if (turma) {
                form.elements['nome'].value = turma.nome;
                form.elements['descricao'].value = turma.descricao || '';
                form.elements['capacidade'].value = turma.capacidade;
                form.elements['ano_letivo'].value = turma.ano_letivo;
                form.elements['periodo'].value = turma.periodo;
                form.dataset.turmaId = turmaId;
            }
        } else {
            titulo.textContent = '📚 Nova Turma';
            form.reset();
            form.elements['ano_letivo'].value = new Date().getFullYear(); // Ano atual por padrão
            form.removeAttribute('data-turma-id');
        }
        
        modal.style.display = 'flex';
        setTimeout(() => modal.classList.add('active'), 10);
    }

    function closeModalTurma() {
        const modal = document.getElementById('modal-turma');
        modal.classList.remove('active');
        setTimeout(() => {
            modal.style.display = 'none';
            document.getElementById('form-turma').reset();
        }, 300);
    }

    function setupModalTurma() {
        const modal = document.getElementById('modal-turma');
        const fecharModal = document.getElementById('fechar-modal-turma');
        const cancelarBtn = document.getElementById('cancelar-turma');
        const form = document.getElementById('form-turma');
        
        if (fecharModal) {
            fecharModal.addEventListener('click', closeModalTurma);
        }
        
        if (cancelarBtn) {
            cancelarBtn.addEventListener('click', closeModalTurma);
        }
        
        // Fechar modal ao clicar fora
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    closeModalTurma();
                }
            });
        }
        
        // ESC para fechar
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal?.classList.contains('active')) {
                closeModalTurma();
            }
        });
        
        // Envio do formulário
        if (form) {
            form.addEventListener('submit', handleSubmitTurma);
        }
    }

    async function handleSubmitTurma(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        const turmaId = form.dataset.turmaId;
        const isEdit = !!turmaId;
        
        const turmaData = {
            nome: formData.get('nome'),
            descricao: formData.get('descricao') || null,
            capacidade: parseInt(formData.get('capacidade')),
            ano_letivo: parseInt(formData.get('ano_letivo')),
            periodo: formData.get('periodo')
        };
        
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        try {
            submitBtn.textContent = '💾 Salvando...';
            submitBtn.disabled = true;
            
            const url = isEdit ? `${API_BASE_URL}/turmas/${turmaId}` : `${API_BASE_URL}/turmas`;
            const method = isEdit ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify(turmaData)
            });
            
            if (response.ok) {
                const action = isEdit ? 'atualizada' : 'criada';
                showToast(`Turma ${action} com sucesso!`, 'success');
                closeModalTurma();
                await loadTurmas(); // Recarregar dados
            } else {
                const error = await response.json();
                throw new Error(error.detail || `Erro ao ${isEdit ? 'atualizar' : 'criar'} turma`);
            }
        } catch (error) {
            console.error('Erro ao salvar turma:', error);
            showToast(error.message, 'error');
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }

    function editarTurma(turmaId) {
        openModalTurma(turmaId);
    }

    async function excluirTurma(turmaId) {
        const turma = turmasData.find(t => t.id == turmaId);
        if (!turma) return;
        
        const confirmDelete = confirm(`Tem certeza que deseja excluir a turma "${turma.nome}"?\n\nEsta ação não pode ser desfeita.`);
        if (!confirmDelete) return;
        
        try {
            const response = await fetch(`${API_BASE_URL}/turmas/${turmaId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });
            
            if (response.ok) {
                showToast('Turma excluída com sucesso!', 'success');
                await loadTurmas(); // Recarregar dados
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Erro ao excluir turma');
            }
        } catch (error) {
            console.error('Erro ao excluir turma:', error);
            showToast(error.message, 'error');
        }
    }

    console.log('🎯 Sistema configurado e pronto para uso!');
});
