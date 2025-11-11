/**
 * Sistema de atalhos de teclado com suporte a numpad
 */

// Mapeamento de atalhos por contexto (página)
let atalhosContexto = {};
let modoMenu = false;

// Atalhos do modo menu (tecla -)
const atalhosMenu = {
    '1': { descricao: 'Voltar para Página Inicial', acao: () => window.location.href = '/' },
    '2': { descricao: 'Ir para Análise de ECG', acao: () => window.location.href = '/analise' },
    '3': { descricao: 'Ir para Fila de Resultados', acao: () => window.location.href = '/resultados' }
};

/**
 * Registra atalhos para a página atual
 */
function registrarAtalhos(atalhos) {
    atalhosContexto = atalhos;
    console.log('📋 Atalhos registrados:', Object.keys(atalhos));
}

/**
 * Anuncia os atalhos disponíveis na página
 */
function anunciarAtalhosPagina() {
    let mensagem = 'Atalhos disponíveis: ';
    const atalhos = [];
    
    for (const [tecla, config] of Object.entries(atalhosContexto)) {
        if (tecla !== 'Enter') { // Não anunciar Enter separadamente
            atalhos.push(`${tecla}: ${config.descricao}`);
        }
    }
    
    mensagem += atalhos.join(', ');
    mensagem += '. Pressione menos para menu de navegação, H para ajuda.';
    
    if (typeof anunciar !== 'undefined') {
        anunciar(mensagem);
    }
}

/**
 * Detecta se a tecla é do numpad
 */
function isNumpadKey(code) {
    const numpadKeys = [
        'Numpad0', 'Numpad1', 'Numpad2', 'Numpad3', 'Numpad4',
        'Numpad5', 'Numpad6', 'Numpad7', 'Numpad8', 'Numpad9',
        'NumpadSubtract', 'NumpadEnter', 'NumLock'
    ];
    return numpadKeys.includes(code);
}

/**
 * Converte código do numpad para tecla
 */
function numpadToKey(code) {
    if (code.startsWith('Numpad')) {
        return code.replace('Numpad', '');
    }
    return null;
}

/**
 * Processa evento de teclado
 */
function processarTecla(e) {
    // Ignora em campos de texto (exceto para alguns atalhos especiais)
    const isTextField = e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA';
    
    // Detecta se é numpad
    const isNumpad = isNumpadKey(e.code);
    let tecla = isNumpad ? numpadToKey(e.code) : e.key;
    
    console.log('⌨️ Tecla:', e.key, 'Code:', e.code, 'Numpad:', isNumpad, 'Tecla processada:', tecla);
    
    // Modo Menu (tecla -)
    if ((e.key === '-' || e.code === 'NumpadSubtract') && !isTextField) {
        e.preventDefault();
        
        if (!modoMenu) {
            modoMenu = true;
            console.log('📋 Modo Menu ativado');
            
            let mensagem = 'Menu de navegação: ';
            const opcoes = [];
            for (const [tecla, config] of Object.entries(atalhosMenu)) {
                opcoes.push(`${tecla} para ${config.descricao}`);
            }
            mensagem += opcoes.join(', ') + '. Pressione Escape para cancelar.';
            
            if (typeof anunciar !== 'undefined') {
                anunciar(mensagem);
            }
        }
        return;
    }
    
    // Se está em modo menu
    if (modoMenu) {
        if (isNumpad && tecla && /^[0-9]$/.test(tecla)) {
            const atalho = atalhosMenu[tecla];
            if (atalho) {
                e.preventDefault();
                console.log(`📋 Menu: ${tecla} - ${atalho.descricao}`);
                if (typeof anunciar !== 'undefined') {
                    anunciar(atalho.descricao);
                }
                atalho.acao();
                modoMenu = false;
            }
        } else if (e.key === 'Escape') {
            e.preventDefault();
            modoMenu = false;
            if (typeof anunciar !== 'undefined') {
                anunciar('Menu cancelado');
            }
            console.log('❌ Modo Menu desativado');
        }
        return;
    }
    
    // Atalhos contextuais - Prioridade numpad numérico
    if (isNumpad && tecla && /^[0-9]$/.test(tecla) && !isTextField) {
        const atalho = atalhosContexto[tecla];
        if (atalho) {
            e.preventDefault();
            console.log(`⚡ Atalho Numpad: ${tecla} - ${atalho.descricao}`);
            if (typeof anunciar !== 'undefined') {
                anunciar(atalho.descricao);
            }
            atalho.acao();
            return;
        }
    }
    
    // Atalhos com letras (teclado principal)
    if (!isTextField) {
        const atalho = atalhosContexto[e.key.toLowerCase()];
        if (atalho && /^[a-z]$/i.test(e.key)) {
            e.preventDefault();
            console.log(`⚡ Atalho letra: ${e.key} - ${atalho.descricao}`);
            if (typeof anunciar !== 'undefined') {
                anunciar(atalho.descricao);
            }
            atalho.acao();
            return;
        }
    }
    
    // NumpadEnter
    if (e.code === 'NumpadEnter' && atalhosContexto['Enter']) {
        e.preventDefault();
        const atalhoEnter = atalhosContexto['Enter'];
        console.log(`⚡ NumpadEnter - ${atalhoEnter.descricao}`);
        if (typeof anunciar !== 'undefined') {
            anunciar(atalhoEnter.descricao);
        }
        atalhoEnter.acao();
        return;
    }
    
    // Tecla M: Toggle Mute (integrado de audio.js)
    if ((e.key === 'm' || e.key === 'M') && !isTextField) {
        e.preventDefault();
        if (typeof toggleMute !== 'undefined') {
            toggleMute();
        }
    }
    
    // Tecla H: Ajuda
    if ((e.key === 'h' || e.key === 'H') && !isTextField) {
        e.preventDefault();
        anunciarAtalhosPagina();
    }
}

/**
 * Inicializa sistema de atalhos
 */
function inicializarAtalhos() {
    document.addEventListener('keydown', processarTecla);
    console.log('⌨️ Sistema de atalhos inicializado');
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.registrarAtalhos = registrarAtalhos;
    window.anunciarAtalhosPagina = anunciarAtalhosPagina;
    window.inicializarAtalhos = inicializarAtalhos;
}
