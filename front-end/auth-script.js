// Sistema de Autenticação - Integrado com Backend
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔐 Sistema de Autenticação carregado!');
    
    // Configuração da API
    const API_BASE_URL = 'http://localhost:8000';
    
    // Elementos dos modais
    const modalLogin = document.getElementById('modal-login');
    const modalRegister = document.getElementById('modal-register');
    
    // Botões de abertura
    const btnLogin = document.getElementById('btn-login');
    const btnRegister = document.getElementById('btn-register');
    const btnHeroStart = document.getElementById('btn-hero-start');
    const btnHeroDemo = document.getElementById('btn-hero-demo');
    
    // Botões de fechamento
    const fecharModalLogin = document.getElementById('fechar-modal-login');
    const fecharModalRegister = document.getElementById('fechar-modal-register');
    
    // Formulários
    const formLogin = document.getElementById('form-login');
    const formRegister = document.getElementById('form-register');
    
    // Switches entre modais
    const switchToRegister = document.getElementById('switch-to-register');
    const switchToLogin = document.getElementById('switch-to-login');
    
    // Toast
    const toast = document.getElementById('toast');
    
    // Verificar se já está logado
    checkAuthStatus();
    
    function checkAuthStatus() {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        if (token) {
            window.location.href = 'index.html';
        }
    }
    
    // Função para mostrar toast
    function mostrarToast(mensagem, tipo = 'success', icone = '✅') {
        const toastIcon = document.querySelector('.toast-icon');
        const toastMessage = document.querySelector('.toast-message');
        
        if (tipo === 'error') icone = '❌';
        else if (tipo === 'warning') icone = '⚠️';
        else if (tipo === 'info') icone = 'ℹ️';
        
        toastIcon.textContent = icone;
        toastMessage.textContent = mensagem;
        
        toast.className = `toast ${tipo}`;
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    }
    
    // Função para abrir modal
    function abrirModal(modal) {
        modal.style.display = 'flex';
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);
    }
    
    // Função para fechar modal
    function fecharModal(modal) {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }
    
    // Função para validar email
    function validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
    
    // Função para mostrar loading no botão
    function mostrarLoading(button, loading = true) {
        if (loading) {
            button.disabled = true;
            button.innerHTML = '<div class="spinner"></div> Carregando...';
        } else {
            button.disabled = false;
            button.innerHTML = button.getAttribute('data-original-text');
        }
    }
    
    // Login
    async function realizarLogin(email, senha, manterLogado = false) {
        try {
            // Preparar dados para OAuth2 form
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', senha);
            
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Salvar token
                const storage = manterLogado ? localStorage : sessionStorage;
                storage.setItem('token', data.access_token);
                storage.setItem('token_type', data.token_type);
                
                mostrarToast('Login realizado com sucesso!', 'success');
                
                // Redirecionar após delay
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
                
                return { success: true };
            } else {
                throw new Error(data.detail || 'Credenciais inválidas');
            }
        } catch (error) {
            console.error('Erro no login:', error);
            throw error;
        }
    }
    
    // Registro
    async function realizarRegistro(nome, email, senha) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nome: nome,
                    email: email,
                    senha: senha,
                    cargo: "secretario"  // Padrão para novos usuários
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                mostrarToast('Cadastro realizado! Aguarde aprovação do administrador.', 'success');
                
                // Fechar modal de registro e abrir de login
                fecharModal(modalRegister);
                setTimeout(() => {
                    abrirModal(modalLogin);
                    document.getElementById('email-login').value = email;
                }, 500);
                
                return { success: true };
            } else {
                throw new Error(data.detail || 'Erro no cadastro');
            }
        } catch (error) {
            console.error('Erro no registro:', error);
            throw error;
        }
    }
    
    // Event Listeners
    
    // Abrir modais
    if (btnLogin) {
        btnLogin.addEventListener('click', () => abrirModal(modalLogin));
    }
    
    if (btnRegister) {
        btnRegister.addEventListener('click', () => abrirModal(modalRegister));
    }
    
    if (btnHeroStart) {
        btnHeroStart.addEventListener('click', () => abrirModal(modalLogin));
    }
    
    if (btnHeroDemo) {
        btnHeroDemo.addEventListener('click', () => {
            // Preencher dados de demonstração
            document.getElementById('email-login').value = 'admin@escola.com';
            document.getElementById('senha-login').value = '123456';
            abrirModal(modalLogin);
        });
    }
    
    // Fechar modais
    if (fecharModalLogin) {
        fecharModalLogin.addEventListener('click', () => fecharModal(modalLogin));
    }
    
    if (fecharModalRegister) {
        fecharModalRegister.addEventListener('click', () => fecharModal(modalRegister));
    }
    
    // Switch entre modais
    if (switchToRegister) {
        switchToRegister.addEventListener('click', (e) => {
            e.preventDefault();
            fecharModal(modalLogin);
            setTimeout(() => abrirModal(modalRegister), 300);
        });
    }
    
    if (switchToLogin) {
        switchToLogin.addEventListener('click', (e) => {
            e.preventDefault();
            fecharModal(modalRegister);
            setTimeout(() => abrirModal(modalLogin), 300);
        });
    }
    
    // Fechar modal clicando fora
    [modalLogin, modalRegister].forEach(modal => {
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    fecharModal(modal);
                }
            });
        }
    });
    
    // Formulário de login
    if (formLogin) {
        formLogin.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const btnSubmit = formLogin.querySelector('button[type="submit"]');
            if (!btnSubmit.getAttribute('data-original-text')) {
                btnSubmit.setAttribute('data-original-text', btnSubmit.innerHTML);
            }
            
            const email = document.getElementById('email-login').value.trim();
            const senha = document.getElementById('senha-login').value;
            const manterLogado = document.getElementById('manter-logado')?.checked || false;
            
            // Validações
            if (!email || !senha) {
                mostrarToast('Preencha todos os campos!', 'error');
                return;
            }
            
            if (!validarEmail(email)) {
                mostrarToast('Email inválido!', 'error');
                return;
            }
            
            mostrarLoading(btnSubmit, true);
            
            try {
                await realizarLogin(email, senha, manterLogado);
            } catch (error) {
                mostrarToast(error.message || 'Erro no login', 'error');
            } finally {
                mostrarLoading(btnSubmit, false);
            }
        });
    }
    
    // Formulário de registro
    if (formRegister) {
        formRegister.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const btnSubmit = formRegister.querySelector('button[type="submit"]');
            if (!btnSubmit.getAttribute('data-original-text')) {
                btnSubmit.setAttribute('data-original-text', btnSubmit.innerHTML);
            }
            
            const nome = document.getElementById('nome-registro').value.trim();
            const email = document.getElementById('email-registro').value.trim();
            const senha = document.getElementById('senha-registro').value;
            const confirmarSenha = document.getElementById('confirmar-senha').value;
            
            // Validações
            if (!nome || !email || !senha || !confirmarSenha) {
                mostrarToast('Preencha todos os campos!', 'error');
                return;
            }
            
            if (!validarEmail(email)) {
                mostrarToast('Email inválido!', 'error');
                return;
            }
            
            if (senha.length < 6) {
                mostrarToast('A senha deve ter pelo menos 6 caracteres!', 'error');
                return;
            }
            
            if (senha !== confirmarSenha) {
                mostrarToast('As senhas não coincidem!', 'error');
                return;
            }
            
            mostrarLoading(btnSubmit, true);
            
            try {
                await realizarRegistro(nome, email, senha);
            } catch (error) {
                mostrarToast(error.message || 'Erro no cadastro', 'error');
            } finally {
                mostrarLoading(btnSubmit, false);
            }
        });
    }
    
    // Fechar toast
    const toastClose = document.querySelector('.toast-close');
    if (toastClose) {
        toastClose.addEventListener('click', () => {
            toast.classList.remove('show');
        });
    }
    
    // ESC para fechar modais
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (modalLogin?.classList.contains('active')) {
                fecharModal(modalLogin);
            }
            if (modalRegister?.classList.contains('active')) {
                fecharModal(modalRegister);
            }
        }
    });
    
    console.log('✅ Sistema de autenticação pronto!');
});
