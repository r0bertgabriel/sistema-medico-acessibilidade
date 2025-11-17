/**
 * ═══════════════════════════════════════════════════════════════════════════
 * SISTEMA DE ATALHOS DE TECLADO - Mapeamento Direto (Sem Hierarquia)
 * ═══════════════════════════════════════════════════════════════════════════
 * 
 * REGRAS:
 * - Teclas do numpad: 0-9, Num Lock, /, *, -, +, ., Enter
 * - Cada tecla tem uma função direta, sem necessidade de combinações
 * - Não funciona dentro de campos de texto (INPUT, TEXTAREA)
 * 
 * MAPEAMENTO GLOBAL (funciona em todas as páginas):
 * 
 * NAVEGAÇÃO PRINCIPAL:
 * - 0: Página Inicial
 * - 1: Hub ECG
 * - 2: Hub Hemograma
 * - 3: Análise Hemograma
 * 
 * EXEMPLOS RÁPIDOS (Reprodução de Laudos):
 * - 4: ECG Normal
 * - 5: ECG Arritmia Sinusal
 * - 6: ECG Bloqueo de Rama
 * - 7: Hemograma Normal
 * - 8: Hemograma Anemia
 * - 9: Hemograma Leucocitose
 * 
 * UTILITÁRIOS:
 * - /: Ajuda (lista todos os atalhos)
 * - *: Repetir último anúncio
 * - -: (reservado)
 * - +: Silenciar/Ativar áudio
 * - .: (reservado)
 * - Enter: (reservado)
 * 
 * ═══════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════
// ESTADO GLOBAL
// ═══════════════════════════════════════════════════════════════════════════
const Estado = {
    ultimoAnuncio: ''               // Último texto anunciado (para *)
};

// ═══════════════════════════════════════════════════════════════════════════
// MAPEAMENTO DIRETO DE ATALHOS (Sempre disponíveis)
// ═══════════════════════════════════════════════════════════════════════════
const ATALHOS_GLOBAIS = {
    // NAVEGAÇÃO PRINCIPAL
    '0': { 
        nome: 'Página Inicial',
        descricao: 'Ir a la página inicial',
        acao: () => navegar('/')
    },
    '1': { 
        nome: 'Hub ECG',
        descricao: 'Ir al hub del módulo ECG',
        acao: () => navegar('/ecg')
    },
    '2': { 
        nome: 'Hub Hemograma',
        descricao: 'Ir al hub del módulo Hemograma',
        acao: () => navegar('/hemograma')
    },
    '3': { 
        nome: 'Análisis Hemograma',
        descricao: 'Ir a análisis de hemograma',
        acao: () => navegar('/hemograma/analise')
    },
    '4': { 
        nome: 'ECG Normal',
        descricao: 'Reproducir laudo de ECG normal',
        acao: () => reproducirLaudo('ecg', 'normal')
    },
    '5': { 
        nome: 'ECG Arritmia',
        descricao: 'Reproducir laudo de ECG con arritmia sinusal',
        acao: () => reproducirLaudo('ecg', 'arritmia_sinusal')
    },
    '6': { 
        nome: 'ECG Bloqueo',
        descricao: 'Reproducir laudo de ECG con bloqueo de rama',
        acao: () => reproducirLaudo('ecg', 'bloqueio_ramo')
    },
    '7': { 
        nome: 'Hemograma Normal',
        descricao: 'Reproducir laudo de hemograma normal',
        acao: () => reproducirLaudo('hemograma', 'normal')
    },
    '8': { 
        nome: 'Hemograma Anemia',
        descricao: 'Reproducir laudo de hemograma con anemia',
        acao: () => reproducirLaudo('hemograma', 'anemia')
    },
    '9': { 
        nome: 'Hemograma Leucocitose',
        descricao: 'Reproducir laudo de hemograma con leucocitosis',
        acao: () => reproducirLaudo('hemograma', 'leucocitose')
    },
    
    // UTILITÁRIOS
    '/': { 
        nome: 'Ayuda',
        descricao: 'Lista todos los atajos disponibles',
        acao: () => listarAjuda()
    },
    '*': { 
        nome: 'Repetir',
        descricao: 'Repite el último anuncio de audio',
        acao: () => repetirAnuncio()
    },
    '+': { 
        nome: 'Silenciar/Activar',
        descricao: 'Alterna entre silenciar y activar el audio',
        acao: () => alternarMute()
    }
};

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
// AÇÕES
// ═══════════════════════════════════════════════════════════════════════════

function listarAjuda() {
    let ajuda = 'Atajos disponibles: ';
    
    // Listar todos os atalhos globais
    for (const [tecla, config] of Object.entries(ATALHOS_GLOBAIS)) {
        ajuda += `${tecla} para ${config.nome}. `;
    }
    
    anunciarSeDisponivel(ajuda, true);
}

function repetirAnuncio() {
    if (Estado.ultimoAnuncio) {
        anunciarSeDisponivel(Estado.ultimoAnuncio);
    } else {
        anunciarSeDisponivel('Ningún anuncio anterior para repetir');
    }
}

function alternarMute() {
    if (typeof toggleMute === 'function') {
        toggleMute();
    } else {
        console.warn('⚠️ Função toggleMute não disponível');
    }
}

function navegar(url) {
    console.log('🔗 Navegando para:', url);
    window.location.href = url;
}

function reproducirLaudo(tipo, exemplo) {
    console.log(`🔊 Reproduciendo laudo: ${tipo} - ${exemplo}`);
    
    // Se estamos na página correta, simula o clique do botão
    if (tipo === 'ecg' && window.location.pathname === '/resultados') {
        // Chama diretamente a função processarResultado se existir
        if (typeof processarResultado === 'function') {
            processarResultado(exemplo);
        } else {
            anunciarSeDisponivel('Función no disponible en esta página');
        }
    } else if (tipo === 'hemograma' && window.location.pathname === '/hemograma-resultados') {
        // Chama diretamente a função carregarExemplo se existir
        if (typeof carregarExemplo === 'function') {
            carregarExemplo(exemplo);
        } else {
            anunciarSeDisponivel('Función no disponible en esta página');
        }
    } else {
        // Não estamos na página correta, navega e depois reproduz
        const paginaDestino = tipo === 'ecg' ? '/resultados' : '/hemograma-resultados';
        anunciarSeDisponivel(`Navegando a ${tipo === 'ecg' ? 'resultados de ECG' : 'resultados de hemograma'} para reproducir ejemplo`);
        
        // Salva o exemplo no sessionStorage para reproduzir após navegação
        sessionStorage.setItem('autoplay_tipo', tipo);
        sessionStorage.setItem('autoplay_exemplo', exemplo);
        
        window.location.href = paginaDestino;
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
 * Processa cada tecla pressionada de forma direta:
 * 1º) Normaliza tecla (numpad → normal)
 * 2º) Valida se é permitida (0-9, /, *, -, +, ., Enter)
 * 3º) Ignora se está em campo de texto (exceto utilitários)
 * 4º) Executa ação direta do mapeamento global
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
    
    // Em campos de texto, só permite utilitários (/, *, +)
    const ehUtilitario = ['/', '*', '+'].includes(tecla);
    if (emCampoTexto && !ehUtilitario) {
        return; // Permite digitação normal
    }
    
    // ─────────────────────────────────────────────────────────────────────
    // PASSO 4: Executar ação direta
    // ─────────────────────────────────────────────────────────────────────
    
    console.log(`🔑 Tecla: "${tecla}" | Contexto: ${emCampoTexto ? 'TEXTO' : 'NORMAL'}`);
    
    const atalho = ATALHOS_GLOBAIS[tecla];
    if (atalho) {
        evento.preventDefault();
        console.log(`⚡ Executando: ${atalho.nome}`);
        
        // Anunciar nome do atalho antes de executar
        anunciarSeDisponivel(atalho.nome);
        
        // Executar ação
        atalho.acao();
    } else {
        // Tecla válida mas sem atalho definido
        console.log(`⚠️ Tecla "${tecla}" sem atalho definido`);
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// API PÚBLICA: Funções expostas para uso externo
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Função mantida para retrocompatibilidade - não faz nada
 * Atalhos agora são mapeamentos globais diretos (ATALHOS_GLOBAIS)
 * @deprecated Use ATALHOS_GLOBAIS diretamente
 */
function registrarAtalhos(atalhos) {
    console.log('⚠️ registrarAtalhos() obsoleto - atalhos agora são globais e diretos');
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
    console.log('⌨️  SISTEMA DE ATALHOS DIRETOS INICIALIZADO');
    console.log('═══════════════════════════════════════════════════════════');
    console.log('Atalhos globais disponíveis:');
    for (const [tecla, config] of Object.entries(ATALHOS_GLOBAIS)) {
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

window.registrarAtalhos = registrarAtalhos; // Mantido para compatibilidade
window.salvarUltimoAnuncio = salvarUltimoAnuncio;
window.inicializarAtalhos = inicializarAtalhos;

console.log('✅ keyboard.js carregado com sucesso');

