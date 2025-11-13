/**/**/**

 * Sistema de atalhos de teclado - APENAS caracteres numéricos e matemáticos

 * Atalhos permitidos: 0-9, /, *, -, +, . * Sistema de atalhos de teclado - APENAS caracteres numéricos e matemáticos * Sistema de atalhos de teclado com suporte a numpad

 */

 * Atalhos permitidos: 0-9, /, *, -, +, . */

// Estado global

let atalhosContexto = {}; */

let modoMenu = false;

let ultimoAnuncio = '';// Mapeamento de atalhos por contexto (página)



// ===== ATALHOS GLOBAIS =====// Mapeamento de atalhos por contexto (página)let atalhosContexto = {};

// Estes atalhos funcionam em TODAS as páginas

const ATALHOS_GLOBAIS = {let atalhosContexto = {};let modoMenu = false;

    '-': { descricao: 'Menu de navegação', acao: ativarModoMenu },

    '/': { descricao: 'Ajuda - Listar todos os atalhos', acao: listarAtalhos },let modoMenu = false;

    '*': { descricao: 'Repetir último anúncio', acao: repetirUltimoAnuncio },

    '+': { descricao: 'Mutar ou desmutar áudio', acao: toggleMuteAtalho }let ultimoAnuncio = '';// Atalhos do modo menu (tecla -)

};

const atalhosMenu = {

// Atalhos do modo menu (tecla -)

const atalhosMenu = {// ===== ATALHOS GLOBAIS =====    '1': { descricao: 'Voltar para Página Inicial', acao: () => window.location.href = '/' },

    '1': { descricao: 'Voltar para Página Inicial', acao: () => window.location.href = '/' },

    '2': { descricao: 'Ir para Módulo ECG', acao: () => window.location.href = '/ecg' },// Estes atalhos funcionam em TODAS as páginas    '2': { descricao: 'Ir para Módulo ECG', acao: () => window.location.href = '/ecg' },

    '3': { descricao: 'Ir para Módulo Hemograma', acao: () => window.location.href = '/hemograma' },

    '0': { descricao: 'Cancelar menu', acao: cancelarMenu }    '3': { descricao: 'Ir para Módulo Hemograma', acao: () => window.location.href = '/hemograma' }

};

const ATALHOS_GLOBAIS = {};

/**

 * Traduz teclas do numpad para seu equivalente numérico    '-': { descricao: 'Menu de navegação', acao: ativarModoMenu },

 */

function traduzirNumpad(code) {    '/': { descricao: 'Ajuda - Listar todos os atalhos', acao: listarAtalhos },/**

    const mapeamento = {

        'Numpad0': '0', 'Numpad1': '1', 'Numpad2': '2', 'Numpad3': '3',    '*': { descricao: 'Repetir último anúncio', acao: repetirUltimoAnuncio }, * Registra atalhos para a página atual

        'Numpad4': '4', 'Numpad5': '5', 'Numpad6': '6', 'Numpad7': '7',

        'Numpad8': '8', 'Numpad9': '9',    '+': { descricao: 'Mutar ou desmutar áudio', acao: toggleMuteAtalho } */

        'NumpadDivide': '/', 'NumpadMultiply': '*',

        'NumpadSubtract': '-', 'NumpadAdd': '+',};function registrarAtalhos(atalhos) {

        'NumpadDecimal': '.'

    };    atalhosContexto = atalhos;

    return mapeamento[code] || null;

}// Atalhos do modo menu (tecla -)    console.log('📋 Atalhos registrados:', Object.keys(atalhos));



/**const atalhosMenu = {}

 * Verifica se a tecla pressionada é permitida

 */    '1': { descricao: 'Voltar para Página Inicial', acao: () => window.location.href = '/' },

function isTeclaPermitida(key) {

    const permitidas = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',     '2': { descricao: 'Ir para Módulo ECG', acao: () => window.location.href = '/ecg' },/**

                        '/', '*', '-', '+', '.'];

    return permitidas.includes(key);    '3': { descricao: 'Ir para Módulo Hemograma', acao: () => window.location.href = '/hemograma' }, * Anuncia os atalhos disponíveis na página

}

    '0': { descricao: 'Cancelar menu', acao: () => { modoMenu = false; anunciar('Menu cancelado'); } } */

/**

 * Registra atalhos contextuais para a página atual};function anunciarAtalhosPagina() {

 */

function registrarAtalhos(atalhos) {    let mensagem = 'Atalhos disponíveis: ';

    atalhosContexto = atalhos;

    console.log('📋 Atalhos registrados:', Object.keys(atalhos));/**    const atalhos = [];

}

 * Registra atalhos para a página atual    

/**

 * Salva o último anúncio para poder repetir com * */    for (const [tecla, config] of Object.entries(atalhosContexto)) {

 */

function salvarUltimoAnuncio(texto) {function registrarAtalhos(atalhos) {        if (tecla !== 'Enter') { // Não anunciar Enter separadamente

    ultimoAnuncio = texto;

}    atalhosContexto = atalhos;            atalhos.push(`${tecla}: ${config.descricao}`);



/**    console.log('📋 Atalhos registrados:', Object.keys(atalhos));        }

 * Ativa o modo menu de navegação

 */}    }

function ativarModoMenu() {

    modoMenu = true;    

    const opcoes = [];

    for (const [tecla, config] of Object.entries(atalhosMenu)) {/**    mensagem += atalhos.join(', ');

        opcoes.push(`Tecla ${tecla}: ${config.descricao}`);

    } * Ativa modo menu de navegação    mensagem += '. Pressione menos para menu de navegação, H para ajuda.';

    const mensagem = 'Menu de navegação. ' + opcoes.join('. ');

     */    

    if (typeof anunciar !== 'undefined') {

        anunciar(mensagem);function ativarModoMenu() {    if (typeof anunciar !== 'undefined') {

    }

}    if (!modoMenu) {        anunciar(mensagem);



/**        modoMenu = true;    }

 * Cancela o modo menu

 */        console.log('📋 Modo Menu ativado');}

function cancelarMenu() {

    modoMenu = false;        

    if (typeof anunciar !== 'undefined') {

        anunciar('Menu cancelado');        let mensagem = 'Menu de navegação ativado. Pressione: ';/**

    }

}        const opcoes = []; * Detecta se a tecla é do numpad



/**        for (const [tecla, config] of Object.entries(atalhosMenu)) { */

 * Lista todos os atalhos disponíveis

 */            opcoes.push(`${tecla} para ${config.descricao}`);function isNumpadKey(code) {

function listarAtalhos() {

    let mensagem = 'Atalhos disponíveis. ';        }    const numpadKeys = [

    

    // Atalhos globais        mensagem += opcoes.join(', ');        'Numpad0', 'Numpad1', 'Numpad2', 'Numpad3', 'Numpad4',

    mensagem += 'Atalhos globais: ';

    for (const [tecla, config] of Object.entries(ATALHOS_GLOBAIS)) {                'Numpad5', 'Numpad6', 'Numpad7', 'Numpad8', 'Numpad9',

        mensagem += `Tecla ${tecla}: ${config.descricao}. `;

    }        if (typeof anunciar !== 'undefined') {        'NumpadSubtract', 'NumpadEnter', 'NumLock'

    

    // Atalhos contextuais (se houver)            anunciar(mensagem);    ];

    if (Object.keys(atalhosContexto).length > 0) {

        mensagem += 'Atalhos desta página: ';        }    return numpadKeys.includes(code);

        for (const [tecla, config] of Object.entries(atalhosContexto)) {

            mensagem += `Tecla ${tecla}: ${config.descricao}. `;    }}

        }

    }}

    

    if (typeof anunciar !== 'undefined') {/**

        anunciar(mensagem, true);

    }/** * Converte código do numpad para tecla

}

 * Lista todos os atalhos disponíveis (/ para ajuda) */

/**

 * Repete o último anúncio de áudio */function numpadToKey(code) {

 */

function repetirUltimoAnuncio() {function listarAtalhos() {    if (code.startsWith('Numpad')) {

    if (ultimoAnuncio) {

        if (typeof anunciar !== 'undefined') {    let mensagem = 'Atalhos disponíveis. ';        return code.replace('Numpad', '');

            anunciar(ultimoAnuncio);

        }        }

    } else {

        if (typeof anunciar !== 'undefined') {    // Atalhos globais    return null;

            anunciar('Nenhum anúncio anterior para repetir');

        }    mensagem += 'Globais: ';}

    }

}    const globais = [];



/**    for (const [tecla, config] of Object.entries(ATALHOS_GLOBAIS)) {/**

 * Alterna entre mutar e desmutar

 */        globais.push(`${tecla} para ${config.descricao}`); * Processa evento de teclado

function toggleMuteAtalho() {

    if (typeof toggleMute !== 'undefined') {    } */

        toggleMute();

    }    mensagem += globais.join(', ') + '. ';function processarTecla(e) {

}

        // Ignora em campos de texto (exceto para alguns atalhos especiais)

/**

 * Processa a tecla pressionada    // Atalhos da página    const isTextField = e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA';

 */

function processarTecla(e) {    if (Object.keys(atalhosContexto).length > 0) {    

    // Traduzir numpad

    let tecla = e.key;        mensagem += 'Atalhos desta página: ';    // Detecta se é numpad

    if (e.code && e.code.startsWith('Numpad')) {

        const traduzida = traduzirNumpad(e.code);        const contextuais = [];    const isNumpad = isNumpadKey(e.code);

        if (traduzida) {

            tecla = traduzida;        for (const [tecla, config] of Object.entries(atalhosContexto)) {    let tecla = isNumpad ? numpadToKey(e.code) : e.key;

        }

    }            contextuais.push(`${tecla} para ${config.descricao}`);    

    

    // Verificar se é uma tecla permitida        }    console.log('⌨️ Tecla:', e.key, 'Code:', e.code, 'Numpad:', isNumpad, 'Tecla processada:', tecla);

    if (!isTeclaPermitida(tecla)) {

        return; // Ignora teclas não permitidas        mensagem += contextuais.join(', ');    

    }

        }    // Modo Menu (tecla -)

    // Verificar se está em campo de texto

    const isTextField = e.target.tagName === 'INPUT' ||         if ((e.key === '-' || e.code === 'NumpadSubtract') && !isTextField) {

                       e.target.tagName === 'TEXTAREA' ||

                       e.target.isContentEditable;    if (typeof anunciar !== 'undefined') {        e.preventDefault();

    

    // Em campos de texto, permitir apenas atalhos globais        anunciar(mensagem);        

    if (isTextField && !ATALHOS_GLOBAIS[tecla]) {

        return;    }        if (!modoMenu) {

    }

    }            modoMenu = true;

    console.log('🔑 Tecla pressionada:', tecla, 'Modo menu:', modoMenu);

                console.log('📋 Modo Menu ativado');

    // MODO MENU ATIVO

    if (modoMenu) {/**            

        e.preventDefault();

         * Repete o último anúncio (* para repetir)            let mensagem = 'Menu de navegação: ';

        if (atalhosMenu[tecla]) {

            const config = atalhosMenu[tecla]; */            const opcoes = [];

            console.log('🎯 Executando ação do menu:', config.descricao);

            config.acao();function repetirUltimoAnuncio() {            for (const [tecla, config] of Object.entries(atalhosMenu)) {

            

            // Cancelar menu após execução (exceto se for cancelar)    if (ultimoAnuncio) {                opcoes.push(`${tecla} para ${config.descricao}`);

            if (tecla !== '0') {

                modoMenu = false;        console.log('🔁 Repetindo último anúncio:', ultimoAnuncio);            }

            }

        } else {        if (typeof anunciar !== 'undefined') {            mensagem += opcoes.join(', ') + '. Pressione Escape para cancelar.';

            if (typeof anunciar !== 'undefined') {

                anunciar(`Opção ${tecla} não disponível no menu`);            anunciar(ultimoAnuncio, true);            

            }

        }        }            if (typeof anunciar !== 'undefined') {

        return;

    }    } else {                anunciar(mensagem);

    

    // ATALHOS GLOBAIS (fora de campos de texto ou dentro com tecla global)        console.log('❌ Nenhum anúncio anterior');            }

    if (ATALHOS_GLOBAIS[tecla] && !isTextField) {

        e.preventDefault();        if (typeof anunciar !== 'undefined') {        }

        const config = ATALHOS_GLOBAIS[tecla];

        console.log('🌍 Executando atalho global:', config.descricao);            anunciar('Nenhum anúncio anterior para repetir');        return;

        config.acao();

        return;        }    }

    }

        }    

    // ATALHOS CONTEXTUAIS (da página atual)

    if (atalhosContexto[tecla] && !isTextField) {}    // Se está em modo menu

        e.preventDefault();

        const config = atalhosContexto[tecla];    if (modoMenu) {

        console.log('📄 Executando atalho contextual:', config.descricao);

        /**        if (isNumpad && tecla && /^[0-9]$/.test(tecla)) {

        if (typeof anunciar !== 'undefined') {

            anunciar(config.descricao); * Salva o último anúncio (para repetir com *)            const atalho = atalhosMenu[tecla];

        }

         */            if (atalho) {

        config.acao();

        return;function salvarUltimoAnuncio(texto) {                e.preventDefault();

    }

}    ultimoAnuncio = texto;                console.log(`📋 Menu: ${tecla} - ${atalho.descricao}`);



/**}                if (typeof anunciar !== 'undefined') {

 * Inicializa o sistema de atalhos

 */                    anunciar(atalho.descricao);

function inicializarAtalhos() {

    console.log('⌨️ Inicializando sistema de atalhos de teclado');/**                }

    console.log('📋 Atalhos globais disponíveis:', Object.keys(ATALHOS_GLOBAIS));

     * Toggle mute (+ para mutar/desmutar)                atalho.acao();

    // Registrar listener para todas as teclas

    document.addEventListener('keydown', processarTecla); */                modoMenu = false;

    

    console.log('✅ Sistema de atalhos inicializado');function toggleMuteAtalho() {            }

}

    // Esta função é definida em audio.js        } else if (e.key === 'Escape') {

// Expor funções globalmente

window.registrarAtalhos = registrarAtalhos;    if (typeof window.toggleMute !== 'undefined') {            e.preventDefault();

window.salvarUltimoAnuncio = salvarUltimoAnuncio;

window.inicializarAtalhos = inicializarAtalhos;        window.toggleMute();            modoMenu = false;



console.log('✅ Módulo keyboard.js carregado');    } else {            if (typeof anunciar !== 'undefined') {


        console.warn('⚠️ Função toggleMute não encontrada');                anunciar('Menu cancelado');

        if (typeof anunciar !== 'undefined') {            }

            anunciar('Função de mute não disponível');            console.log('❌ Modo Menu desativado');

        }        }

    }        return;

}    }

    

/**    // Atalhos contextuais - Prioridade numpad numérico

 * Detecta se a tecla é do numpad    if (isNumpad && tecla && /^[0-9]$/.test(tecla) && !isTextField) {

 */        const atalho = atalhosContexto[tecla];

function isNumpadKey(code) {        if (atalho) {

    const numpadKeys = [            e.preventDefault();

        'Numpad0', 'Numpad1', 'Numpad2', 'Numpad3', 'Numpad4',            console.log(`⚡ Atalho Numpad: ${tecla} - ${atalho.descricao}`);

        'Numpad5', 'Numpad6', 'Numpad7', 'Numpad8', 'Numpad9',            if (typeof anunciar !== 'undefined') {

        'NumpadDivide', 'NumpadMultiply', 'NumpadSubtract',                 anunciar(atalho.descricao);

        'NumpadAdd', 'NumpadDecimal'            }

    ];            atalho.acao();

    return numpadKeys.includes(code);            return;

}        }

    }

/**    

 * Converte código do numpad para tecla    // Atalhos com letras (teclado principal)

 */    if (!isTextField) {

function numpadToKey(code) {        const atalho = atalhosContexto[e.key.toLowerCase()];

    const mapa = {        if (atalho && /^[a-z]$/i.test(e.key)) {

        'Numpad0': '0', 'Numpad1': '1', 'Numpad2': '2', 'Numpad3': '3', 'Numpad4': '4',            e.preventDefault();

        'Numpad5': '5', 'Numpad6': '6', 'Numpad7': '7', 'Numpad8': '8', 'Numpad9': '9',            console.log(`⚡ Atalho letra: ${e.key} - ${atalho.descricao}`);

        'NumpadDivide': '/',            if (typeof anunciar !== 'undefined') {

        'NumpadMultiply': '*',                anunciar(atalho.descricao);

        'NumpadSubtract': '-',            }

        'NumpadAdd': '+',            atalho.acao();

        'NumpadDecimal': '.'            return;

    };        }

    return mapa[code] || null;    }

}    

    // NumpadEnter

/**    if (e.code === 'NumpadEnter' && atalhosContexto['Enter']) {

 * Verifica se a tecla é permitida (apenas 0-9, /, *, -, +, .)        e.preventDefault();

 */        const atalhoEnter = atalhosContexto['Enter'];

function isTeclaPermitida(tecla) {        console.log(`⚡ NumpadEnter - ${atalhoEnter.descricao}`);

    return /^[0-9\/\*\-\+\.]$/.test(tecla);        if (typeof anunciar !== 'undefined') {

}            anunciar(atalhoEnter.descricao);

        }

/**        atalhoEnter.acao();

 * Processa evento de teclado        return;

 */    }

function processarTecla(e) {    

    // Ignora em campos de texto (exceto para alguns atalhos especiais)    // Tecla M: Toggle Mute (integrado de audio.js)

    const isTextField = e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA';    if ((e.key === 'm' || e.key === 'M') && !isTextField) {

            e.preventDefault();

    // Detecta se é numpad        if (typeof toggleMute !== 'undefined') {

    const isNumpad = isNumpadKey(e.code);            toggleMute();

    let tecla = isNumpad ? numpadToKey(e.code) : e.key;        }

        }

    // Ignora teclas não permitidas    

    if (!isTeclaPermitida(tecla)) {    // Tecla H: Ajuda

        return;    if ((e.key === 'h' || e.key === 'H') && !isTextField) {

    }        e.preventDefault();

            anunciarAtalhosPagina();

    console.log('⌨️ Tecla:', e.key, 'Code:', e.code, 'Numpad:', isNumpad, 'Tecla processada:', tecla);    }

    }

    // ===== MODO MENU (após pressionar -) =====

    if (modoMenu && !isTextField) {/**

        const atalhoMenu = atalhosMenu[tecla]; * Inicializa sistema de atalhos

        if (atalhoMenu) { */

            e.preventDefault();function inicializarAtalhos() {

            console.log(`📋 Menu: ${tecla} - ${atalhoMenu.descricao}`);    document.addEventListener('keydown', processarTecla);

            if (typeof anunciar !== 'undefined') {    console.log('⌨️ Sistema de atalhos inicializado');

                anunciar(atalhoMenu.descricao);}

            }

            atalhoMenu.acao();// Exportar para uso global

            modoMenu = false;if (typeof window !== 'undefined') {

            return;    window.registrarAtalhos = registrarAtalhos;

        }    window.anunciarAtalhosPagina = anunciarAtalhosPagina;

    }    window.inicializarAtalhos = inicializarAtalhos;

    }

    // ===== ATALHOS GLOBAIS =====
    if (!isTextField) {
        const atalhoGlobal = ATALHOS_GLOBAIS[tecla];
        if (atalhoGlobal) {
            e.preventDefault();
            console.log(`🌐 Atalho global: ${tecla} - ${atalhoGlobal.descricao}`);
            
            // Não anuncia o próprio atalho se for repetir (*)
            if (tecla !== '*') {
                if (typeof anunciar !== 'undefined') {
                    anunciar(atalhoGlobal.descricao);
                }
            }
            
            atalhoGlobal.acao();
            return;
        }
    }
    
    // ===== ATALHOS CONTEXTUAIS (da página) =====
    if (!isTextField) {
        const atalhoContexto = atalhosContexto[tecla];
        if (atalhoContexto) {
            e.preventDefault();
            console.log(`⚡ Atalho contextual: ${tecla} - ${atalhoContexto.descricao}`);
            if (typeof anunciar !== 'undefined') {
                anunciar(atalhoContexto.descricao);
            }
            atalhoContexto.acao();
            return;
        }
    }
    
    // Se chegou aqui em modo menu e não encontrou atalho
    if (modoMenu && !isTextField) {
        e.preventDefault();
        if (typeof anunciar !== 'undefined') {
            anunciar('Opção inválida. Pressione 0 para cancelar ou barra para ajuda');
        }
    }
}

/**
 * Inicializa sistema de atalhos
 */
function inicializarAtalhos() {
    document.addEventListener('keydown', processarTecla);
    console.log('⌨️ Sistema de atalhos inicializado');
    console.log('📋 Atalhos globais:', Object.keys(ATALHOS_GLOBAIS));
}

/**
 * Anuncia os atalhos disponíveis na página (compatibilidade)
 */
function anunciarAtalhosPagina() {
    listarAtalhos();
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.registrarAtalhos = registrarAtalhos;
    window.anunciarAtalhosPagina = anunciarAtalhosPagina;
    window.inicializarAtalhos = inicializarAtalhos;
    window.salvarUltimoAnuncio = salvarUltimoAnuncio;
    window.listarAtalhos = listarAtalhos;
}
