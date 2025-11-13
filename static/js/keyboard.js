/**
 * ═══════════════════════════════════════════════════════════════════════════
 * SISTEMA DE ATALHOS DE TECLADO - Hierarquia Clara e Organizada
 * ═══════════════════════════════════════════════════════════════════════════
 * 
 * REGRAS:
 * - Apenas caracteres numéricos e matemáticos: 0-9, /, *, -, +, .
 * - Suporte total ao teclado numérico (numpad)
 * - Não funciona dentro de campos de texto (INPUT, TEXTAREA)
 * 
 * HIERARQUIA DE PRIORIDADE (maior → menor):
 * 1. MODO MENU (ativado por '-')      → Teclas 0-9 viram navegação
 * 2. ATALHOS UTILITÁRIOS (/, *, +)    → Sempre disponíveis
 * 3. ATALHOS CONTEXTUAIS (0-9)        → Dependem da página atual
 * 
 * ═══════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════
// ESTADO GLOBAL
// ═══════════════════════════════════════════════════════════════════════════
const Estado = {
    modoMenuAtivo: false,           // Se true, teclas 0-9 viram navegação
    atalhosContextuais: {},         // Atalhos da página atual
    ultimoAnuncio: ''               // Último texto anunciado (para *)
};

// ═══════════════════════════════════════════════════════════════════════════
// CAMADA 1: ATALHOS UTILITÁRIOS (Sempre disponíveis, exceto em text fields)
// ═══════════════════════════════════════════════════════════════════════════
const UTILITARIOS = {
    '-': { 
        nome: 'Menu de Navegação',
        descricao: 'Ativa menu com opções 1, 2, 3 para navegar entre módulos',
        acao: () => ativarMenu()
    },
    '/': { 
        nome: 'Ajuda',
        descricao: 'Lista todos os atalhos disponíveis',
        acao: () => listarAjuda()
    },
    '*': { 
        nome: 'Repetir',
        descricao: 'Repete o último anúncio de áudio',
        acao: () => repetirAnuncio()
    },
    '+': { 
        nome: 'Mute/Unmute',
        descricao: 'Alterna entre mutar e desmutar o áudio',
        acao: () => alternarMute()
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// CAMADA 2: MENU DE NAVEGAÇÃO (Ativado por '-', usa teclas 0-9)
// ═══════════════════════════════════════════════════════════════════════════
const MENU_NAVEGACAO = {
    '1': { 
        nome: 'Página Inicial',
        acao: () => navegar('/')
    },
    '2': { 
        nome: 'Módulo ECG',
        acao: () => navegar('/ecg')
    },
    '3': { 
        nome: 'Módulo Hemograma',
        acao: () => navegar('/hemograma')
    },
    '0': { 
        nome: 'Cancelar Menu',
        acao: () => desativarMenu()
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// CAMADA 3: ATALHOS CONTEXTUAIS (Definidos por cada página, usam 0-9)
// ═══════════════════════════════════════════════════════════════════════════
// Exemplo de uso em uma página:
// registrarAtalhos({
//     '1': { nome: 'Análise por Dados', acao: () => irPara('/analise') },
//     '2': { nome: 'Análise por Imagem', acao: () => irPara('/analise-imagem') }
// });

// ═══════════════════════════════════════════════════════════════════════════
// UTILITÁRIOS: Tradução de Teclas
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Traduz teclas do numpad para equivalente normal
 * Numpad1 → '1', NumpadAdd → '+', etc.
 */
function traduzirNumpad(code) {
    const mapa = {
        'Numpad0': '0', 'Numpad1': '1', 'Numpad2': '2', 'Numpad3': '3',
        'Numpad4': '4', 'Numpad5': '5', 'Numpad6': '6', 'Numpad7': '7',
        'Numpad8': '8', 'Numpad9': '9',
        'NumpadDivide': '/', 'NumpadMultiply': '*',
        'NumpadSubtract': '-', 'NumpadAdd': '+',
        'NumpadDecimal': '.'
    };
    return mapa[code] || null;
}

/**
 * Verifica se a tecla é permitida (0-9, /, *, -, +, .)
 */
function ehTeclaPermitida(key) {
    return /^[0-9\/\*\-\+\.]$/.test(key);
}

/**
 * Verifica se o elemento atual é campo de texto
 */
function ehCampoDeTexto(element) {
    const tag = element.tagName;
    return tag === 'INPUT' || tag === 'TEXTAREA' || element.isContentEditable;
}

// ═══════════════════════════════════════════════════════════════════════════
// AÇÕES: Camada 1 (Utilitários)
// ═══════════════════════════════════════════════════════════════════════════

function ativarMenu() {
    Estado.modoMenuAtivo = true;
    
    const opcoes = Object.entries(MENU_NAVEGACAO)
        .map(([tecla, config]) => `${tecla}: ${config.nome}`)
        .join('. ');
    
    anunciarSeDisponivel(`Menu de navegação ativado. ${opcoes}`);
    console.log('📂 Menu de navegação ATIVADO');
}

function desativarMenu() {
    Estado.modoMenuAtivo = false;
    anunciarSeDisponivel('Menu cancelado');
    console.log('📂 Menu de navegação DESATIVADO');
}

function listarAjuda() {
    let ajuda = 'Atalhos disponíveis. ';
    
    // Utilitários
    ajuda += 'Utilitários: ';
    for (const [tecla, config] of Object.entries(UTILITARIOS)) {
        ajuda += `${tecla} para ${config.nome}. `;
    }
    
    // Contextuais (se houver)
    const contextuais = Object.keys(Estado.atalhosContextuais);
    if (contextuais.length > 0) {
        ajuda += 'Nesta página: ';
        for (const [tecla, config] of Object.entries(Estado.atalhosContextuais)) {
            ajuda += `${tecla} para ${config.nome}. `;
        }
    }
    
    anunciarSeDisponivel(ajuda, true);
}

function repetirAnuncio() {
    if (Estado.ultimoAnuncio) {
        anunciarSeDisponivel(Estado.ultimoAnuncio);
    } else {
        anunciarSeDisponivel('Nenhum anúncio anterior para repetir');
    }
}

function alternarMute() {
    if (typeof toggleMute === 'function') {
        toggleMute();
    } else {
        console.warn('⚠️ Função toggleMute não disponível');
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// AÇÕES: Camada 2 (Menu de Navegação)
// ═══════════════════════════════════════════════════════════════════════════

function navegar(url) {
    console.log('🔗 Navegando para:', url);
    window.location.href = url;
}

// ═══════════════════════════════════════════════════════════════════════════
// AÇÕES: Camada 3 (Contextuais)
// ═══════════════════════════════════════════════════════════════════════════

function executarContextual(tecla) {
    const config = Estado.atalhosContextuais[tecla];
    if (config) {
        anunciarSeDisponivel(config.nome);
        config.acao();
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// UTILITÁRIOS: Integração com Sistema de Áudio
// ═══════════════════════════════════════════════════════════════════════════

function anunciarSeDisponivel(texto, prioridade = false) {
    Estado.ultimoAnuncio = texto;
    
    if (typeof anunciar === 'function') {
        anunciar(texto, prioridade);
    } else {
        console.log('🔊', texto);
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// PROCESSADOR PRINCIPAL DE TECLAS
// ═══════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════
// PROCESSADOR PRINCIPAL DE TECLAS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Processa cada tecla pressionada seguindo a hierarquia:
 * 1º) Normaliza tecla (numpad → normal)
 * 2º) Valida se é permitida (0-9, /, *, -, +, .)
 * 3º) Ignora se está em campo de texto (exceto utilitários)
 * 4º) Aplica hierarquia: Menu > Utilitários > Contextuais
 */
function processarTecla(evento) {
    // ─────────────────────────────────────────────────────────────────────
    // PASSO 1: Normalizar tecla (traduzir numpad)
    // ─────────────────────────────────────────────────────────────────────
    let tecla = evento.key;
    
    if (evento.code && evento.code.startsWith('Numpad')) {
        const traduzida = traduzirNumpad(evento.code);
        if (traduzida) tecla = traduzida;
    }
    
    // ─────────────────────────────────────────────────────────────────────
    // PASSO 2: Validar tecla permitida
    // ─────────────────────────────────────────────────────────────────────
    if (!ehTeclaPermitida(tecla)) {
        return; // Ignora teclas não permitidas silenciosamente
    }
    
    // ─────────────────────────────────────────────────────────────────────
    // PASSO 3: Verificar contexto (campo de texto?)
    // ─────────────────────────────────────────────────────────────────────
    const emCampoTexto = ehCampoDeTexto(evento.target);
    
    // Em campos de texto, só processa utilitários
    if (emCampoTexto && !UTILITARIOS[tecla]) {
        return; // Permite digitação normal
    }
    
    // ─────────────────────────────────────────────────────────────────────
    // PASSO 4: Aplicar HIERARQUIA de processamento
    // ─────────────────────────────────────────────────────────────────────
    
    console.log(`🔑 Tecla: "${tecla}" | Menu: ${Estado.modoMenuAtivo} | Contexto: ${emCampoTexto ? 'TEXTO' : 'NORMAL'}`);
    
    // ╔═══════════════════════════════════════════════════════════════════╗
    // ║ PRIORIDADE 1: MODO MENU ATIVO (teclas 0-9 viram navegação)       ║
    // ╚═══════════════════════════════════════════════════════════════════╝
    if (Estado.modoMenuAtivo) {
        evento.preventDefault();
        
        const opcaoMenu = MENU_NAVEGACAO[tecla];
        if (opcaoMenu) {
            console.log(`📂 Executando menu: ${opcaoMenu.nome}`);
            opcaoMenu.acao();
            
            // Desativa menu automaticamente (exceto na opção '0' que já desativa)
            if (tecla !== '0') {
                Estado.modoMenuAtivo = false;
            }
        } else {
            anunciarSeDisponivel(`Opção ${tecla} não existe no menu`);
        }
        return;
    }
    
    // ╔═══════════════════════════════════════════════════════════════════╗
    // ║ PRIORIDADE 2: ATALHOS UTILITÁRIOS (-, /, *, +)                   ║
    // ╚═══════════════════════════════════════════════════════════════════╝
    if (UTILITARIOS[tecla]) {
        evento.preventDefault();
        
        const utilitario = UTILITARIOS[tecla];
        console.log(`🛠️ Executando utilitário: ${utilitario.nome}`);
        utilitario.acao();
        return;
    }
    
    // ╔═══════════════════════════════════════════════════════════════════╗
    // ║ PRIORIDADE 3: ATALHOS CONTEXTUAIS (0-9 definidos pela página)    ║
    // ╚═══════════════════════════════════════════════════════════════════╝
    if (Estado.atalhosContextuais[tecla]) {
        evento.preventDefault();
        
        const contextual = Estado.atalhosContextuais[tecla];
        console.log(`📄 Executando contextual: ${contextual.nome}`);
        executarContextual(tecla);
        return;
    }
    
    // Se chegou aqui, tecla é válida mas não tem ação associada
    console.log(`⚠️ Tecla "${tecla}" sem ação definida neste contexto`);
}

// ═══════════════════════════════════════════════════════════════════════════
// API PÚBLICA: Funções expostas para uso externo
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Registra atalhos contextuais para a página atual
 * @param {Object} atalhos - Objeto com tecla: {nome, acao}
 * 
 * Exemplo:
 * registrarAtalhos({
 *     '1': { nome: 'Análise por Dados', acao: () => location.href = '/analise' },
 *     '2': { nome: 'Ver Exemplos', acao: () => location.href = '/exemplos' }
 * });
 */
function registrarAtalhos(atalhos) {
    Estado.atalhosContextuais = atalhos;
    const teclas = Object.keys(atalhos).join(', ');
    console.log(`📋 Atalhos contextuais registrados: ${teclas}`);
}

/**
 * Salva texto para função de repetir (*)
 * @param {string} texto - Texto do anúncio
 */
function salvarUltimoAnuncio(texto) {
    Estado.ultimoAnuncio = texto;
}

/**
 * Inicializa o sistema de atalhos
 * Chamada automaticamente pelo base.html
 */
function inicializarAtalhos() {
    console.log('');
    console.log('═══════════════════════════════════════════════════════════');
    console.log('⌨️  SISTEMA DE ATALHOS INICIALIZADO');
    console.log('═══════════════════════════════════════════════════════════');
    console.log('Utilitários disponíveis:');
    for (const [tecla, config] of Object.entries(UTILITARIOS)) {
        console.log(`  ${tecla} → ${config.nome}`);
    }
    console.log('═══════════════════════════════════════════════════════════');
    console.log('');
    
    // Registra listener único
    document.addEventListener('keydown', processarTecla);
}

// ═══════════════════════════════════════════════════════════════════════════
// EXPORTAÇÃO GLOBAL
// ═══════════════════════════════════════════════════════════════════════════

window.registrarAtalhos = registrarAtalhos;
window.salvarUltimoAnuncio = salvarUltimoAnuncio;
window.inicializarAtalhos = inicializarAtalhos;

console.log('✅ keyboard.js carregado com sucesso');

