/**
 * Sistema de controle de áudio e mute
 */

// Estado global de áudio
// Carrega estado de mute do localStorage (persiste entre páginas)
let audioMutado = localStorage.getItem('audioMutado') === 'true';
let audioLaudoPausado = null;
let filaAnuncios = [];
let reproduzindo = false;
let audioAtual = null;

/**
 * Pausa todos os áudios de laudo da página
 */
function pausarAudiosLaudo() {
    const audiosLaudo = document.querySelectorAll('audio[id*="laudo"]');
    audiosLaudo.forEach(audio => {
        if (!audio.paused) {
            console.log('⏸️ Pausando áudio de laudo:', audio.id);
            audioLaudoPausado = audio;
            audio.pause();
        }
    });
}

/**
 * Retoma o áudio do laudo que estava pausado
 */
function retomarAudioLaudo() {
    if (audioLaudoPausado && audioLaudoPausado.paused) {
        console.log('▶️ Retomando áudio de laudo');
        audioLaudoPausado.play().catch(e => {
            console.error('Erro ao retomar áudio:', e);
        });
        audioLaudoPausado = null;
    }
}

/**
 * Toggle mute/unmute
 */
function toggleMute() {
    audioMutado = !audioMutado;
    
    // Salva estado no localStorage para persistir entre páginas
    localStorage.setItem('audioMutado', audioMutado);
    
    const muteBtn = document.getElementById('mute-btn');
    if (!muteBtn) return;
    
    if (audioMutado) {
        console.log('🔇 Áudio MUTADO (persistente em todas as páginas)');
        muteBtn.textContent = '🔇';
        muteBtn.classList.add('mutado');
        muteBtn.setAttribute('aria-label', 'Desmutar áudio');
        
        // Para todos os áudios
        if (audioAtual) {
            audioAtual.pause();
            audioAtual = null;
        }
        
        // Limpa fila
        filaAnuncios = [];
        reproduzindo = false;
        
        // Pausa áudio do laudo
        pausarAudiosLaudo();
        
        // Anúncio visual apenas (não gera áudio pois está mutado)
        console.log('💬 Áudio mutado');
    } else {
        console.log('🔊 Áudio ATIVO (persistente em todas as páginas)');
        muteBtn.textContent = '🔊';
        muteBtn.classList.remove('mutado');
        muteBtn.setAttribute('aria-label', 'Mutar áudio');
        
        // Retoma áudio do laudo se houver
        retomarAudioLaudo();
        
        console.log('💬 Áudio ativado');
    }
}

/**
 * Reproduz o próximo áudio da fila
 */
async function reproduzirProximo() {
    if (filaAnuncios.length === 0) {
        reproduzindo = false;
        return;
    }
    
    reproduzindo = true;
    const texto = filaAnuncios.shift();
    
    try {
        // Para e limpa áudio anterior se existir (previne memory leak)
        if (audioAtual) {
            audioAtual.pause();
            audioAtual.onended = null;
            audioAtual.onerror = null;
            audioAtual = null;
        }
        
        // Chama o backend para gerar áudio
        const response = await fetch('/api/anunciar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ texto: texto })
        });
        
        const data = await response.json();
        
        if (data.success) {
            audioAtual = new Audio(data.audio_url);
            audioAtual.playbackRate = 1.0;
            
            audioAtual.onended = function() {
                console.log('✅ Áudio finalizado');
                audioAtual = null;
                reproduzirProximo();
            };
            
            audioAtual.onerror = function() {
                console.error('❌ Erro ao reproduzir áudio');
                audioAtual = null;
                reproduzirProximo();
            };
            
            await audioAtual.play();
            console.log('▶️ Reproduzindo áudio...');
        } else {
            console.error('❌ Erro ao gerar áudio:', data.error);
            reproduzirProximo();
        }
    } catch (error) {
        console.error('❌ Erro na requisição:', error);
        reproduzirProximo();
    }
}

/**
 * Anuncia texto usando TTS (com suporte a prioridade e mute)
 */
function anunciar(texto, prioridade = false) {
    if (audioMutado) {
        console.log('🔇 MUTADO - Anúncio ignorado:', texto);
        return;
    }
    
    console.log('🔊 Anunciando:', texto, prioridade ? '(PRIORIDADE)' : '');
    
    // Pausa áudios de laudo
    pausarAudiosLaudo();
    
    // Se é prioridade, interrompe tudo
    if (prioridade) {
        filaAnuncios = [];
        
        if (audioAtual) {
            console.log('⏹️ Interrompendo áudio anterior (prioridade)');
            audioAtual.pause();
            audioAtual.currentTime = 0;
            audioAtual = null;
        }
        
        reproduzindo = false;
    }
    
    // Atualiza região ARIA
    const anunciador = document.querySelector('[role="alert"]');
    if (anunciador) {
        anunciador.textContent = '';
        setTimeout(() => {
            anunciador.textContent = texto;
        }, 100);
    }
    
    // Adiciona à fila
    filaAnuncios.push(texto);
    
    if (!reproduzindo) {
        reproduzirProximo();
    }
}

/**
 * Inicializa controles de áudio
 */
function inicializarControlesAudio() {
    // Botão de mute
    const muteBtn = document.getElementById('mute-btn');
    if (muteBtn) {
        muteBtn.addEventListener('click', toggleMute);
        
        // Aplica estado salvo do localStorage ao carregar a página
        if (audioMutado) {
            muteBtn.textContent = '🔇';
            muteBtn.classList.add('mutado');
            muteBtn.setAttribute('aria-label', 'Desmutar áudio');
            console.log('🔇 Áudio iniciado como MUTADO (estado persistido)');
        } else {
            muteBtn.textContent = '🔊';
            muteBtn.classList.remove('mutado');
            muteBtn.setAttribute('aria-label', 'Mutar áudio');
            console.log('🔊 Áudio iniciado como ATIVO');
        }
    }
    
    // Nota: Atalho M para mute movido para keyboard.js para evitar listener duplicado
    
    console.log('✅ Controles de áudio inicializados');
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.anunciar = anunciar;
    window.toggleMute = toggleMute;
    window.pausarAudiosLaudo = pausarAudiosLaudo;
    window.inicializarControlesAudio = inicializarControlesAudio;
}
