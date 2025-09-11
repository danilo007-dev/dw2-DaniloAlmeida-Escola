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
    
    // Elementos DOM
    const userAvatar = document.getElementById('user-avatar');
    const userName = document.getElementById('user-name');
    const userRole = document.getElementById('user-role');
    const logoutBtn = document.getElementById('logout-btn');
    
    // Tabs
    const tabs = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Inicialização
    init();
    
    async function init() {
        // Verificar autenticação
        if (!checkAuth()) {
            return;
        }
        
        // Carregar dados do usuário
        await loadUserData();
        
        // Carregar dados iniciais
        await loadInitialData();
        
        // Configurar event listeners
        setupEventListeners();
        
        // Mostrar tab inicial
        showTab('dashboard');
        
        console.log('✅ Sistema inicializado com sucesso!');
    }
    
    function checkAuth() {
        authToken = localStorage.getItem('token') || sessionStorage.getItem('token');
        const tokenType = localStorage.getItem('token_type') || sessionStorage.getItem('token_type');
        
        if (!authToken) {
            window.location.href = 'login.html';
            return false;
        }
        
        // Configurar header padrão para requests
        window.authHeader = `${tokenType || 'Bearer'} ${authToken}`;
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
            if (userAvatar) userAvatar.textContent = currentUser.nome.charAt(0).toUpperCase();
        }
    }
    
    function getRoleDisplay(cargo) {
        const roles = {
            'diretor': 'Diretor(a)',
            'coordenador': 'Coordenador(a)',
            'secretario': 'Secretário(a)',
            'professor': 'Professor(a)'
        };
        return roles[cargo] || cargo;
    }
    
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
        try {
            const response = await fetch(`${API_BASE_URL}/turmas/`, {
                headers: {
                    'Authorization': window.authHeader
                }
            });
            
            if (response.ok) {
                turmasData = await response.json();
                renderTurmasTable();
            }
        } catch (error) {
            console.error('Erro ao carregar turmas:', error);
        }
    }
    
    async function loadAlunos() {
        try {
            const response = await fetch(`${API_BASE_URL}/alunos/`, {
                headers: {
                    'Authorization': window.authHeader
                }
            });
            
            if (response.ok) {
                alunosData = await response.json();
                renderAlunosTable();
            }
        } catch (error) {
            console.error('Erro ao carregar alunos:', error);
        }
    }
    
    async function loadUsuarios() {
        try {
            const response = await fetch(`${API_BASE_URL}/usuarios/`, {
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
            const response = await fetch(`${API_BASE_URL}/dashboard/stats`, {
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
        const elements = {
            'total-alunos': stats.total_alunos,
            'alunos-ativos': stats.alunos_ativos,
            'total-turmas': stats.total_turmas,
            'total-usuarios': stats.total_usuarios
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) element.textContent = value;
        });
    }
    
    function renderTurmasTable() {
        const tbody = document.querySelector('#turmas-table tbody');
        if (!tbody || !turmasData) return;
        
        tbody.innerHTML = turmasData.map(turma => `
            <tr>
                <td>${turma.nome}</td>
                <td>${turma.descricao}</td>
                <td>${turma.capacidade}</td>
                <td>${turma.total_alunos || 0}</td>
                <td>${turma.periodo}</td>
                <td>
                    <button class="btn-action edit-turma" data-id="${turma.id}">✏️</button>
                    <button class="btn-action delete-turma" data-id="${turma.id}">🗑️</button>
                </td>
            </tr>
        `).join('');
    }
    
    function renderAlunosTable() {
        const tbody = document.querySelector('#alunos-table tbody');
        if (!tbody || !alunosData) return;
        
        tbody.innerHTML = alunosData.map(aluno => `
            <tr>
                <td>${aluno.nome}</td>
                <td>${aluno.cpf}</td>
                <td>${formatDate(aluno.data_nascimento)}</td>
                <td>${aluno.turma ? aluno.turma.nome : 'Sem turma'}</td>
                <td>
                    <span class="status ${aluno.status}">${getStatusDisplay(aluno.status)}</span>
                </td>
                <td>
                    <button class="btn-action edit-aluno" data-id="${aluno.id}">✏️</button>
                    <button class="btn-action delete-aluno" data-id="${aluno.id}">🗑️</button>
                </td>
            </tr>
        `).join('');
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
        return new Date(dateString).toLocaleDateString('pt-BR');
    }
    
    function formatDateTime(dateString) {
        if (!dateString) return '';
        return new Date(dateString).toLocaleString('pt-BR');
    }
    
    function setupEventListeners() {
        // Tabs
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetTab = tab.getAttribute('data-tab');
                showTab(targetTab);
            });
        });
        
        // Logout
        if (logoutBtn) {
            logoutBtn.addEventListener('click', logout);
        }
        
        // Refresh buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-refresh')) {
                loadInitialData();
            }
        });
    }
    
    function showTab(tabName) {
        // Remove active from all tabs and contents
        tabs.forEach(tab => tab.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        // Add active to selected tab and content
        const selectedTab = document.querySelector(`[data-tab="${tabName}"]`);
        const selectedContent = document.getElementById(tabName);
        
        if (selectedTab) selectedTab.classList.add('active');
        if (selectedContent) selectedContent.classList.add('active');
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
    
    // Expor funções globais para uso em modals/forms
    window.schoolSystem = {
        loadTurmas,
        loadAlunos,
        loadUsuarios,
        loadDashboardStats,
        showToast,
        authHeader: () => window.authHeader,
        currentUser: () => currentUser,
        API_BASE_URL
    };
    
    console.log('🎯 Sistema configurado e pronto para uso!');
});
