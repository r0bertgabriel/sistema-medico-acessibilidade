/**
 * Sistema de acessibilidade e anúncios automáticos
 */

/**
 * Obtém o label de um elemento de formulário
 */
function obterLabel(elemento) {
    // Label por ID
    if (elemento.id) {
        const label = document.querySelector(`label[for="${elemento.id}"]`);
        if (label) return label.textContent.trim();
    }
    
    // Label como parent
    const labelParent = elemento.closest('label');
    if (labelParent) {
        return labelParent.textContent.trim();
    }
    
    // aria-label
    if (elemento.getAttribute('aria-label')) {
        return elemento.getAttribute('aria-label');
    }
    
    // aria-labelledby
    const labelledby = elemento.getAttribute('aria-labelledby');
    if (labelledby) {
        const labelElement = document.getElementById(labelledby);
        if (labelElement) return labelElement.textContent.trim();
    }
    
    // placeholder
    if (elemento.placeholder) {
        return elemento.placeholder;
    }
    
    // name ou title
    return elemento.name || elemento.title || 'sin etiqueta';
}

/**
 * Gera anúncio para elemento focado
 */
function gerarAnuncioFoco(elemento) {
    let anuncio = '';
    
    console.log('👁️ Foco em:', elemento.tagName, elemento.type, elemento.id || elemento.name);
    
    // Links
    if (elemento.tagName === 'A') {
        const ariaLabel = elemento.getAttribute('aria-label');
        const texto = elemento.textContent.trim();
        anuncio = 'Enlace: ' + (ariaLabel || texto);
    }
    
    // Botões
    else if (elemento.tagName === 'BUTTON') {
        const ariaLabel = elemento.getAttribute('aria-label');
        const texto = elemento.textContent.trim();
        const tipo = elemento.type === 'submit' ? 'Botón de envío' : 'Botón';
        anuncio = tipo + ': ' + (ariaLabel || texto);
    }
    
    // Campos de entrada
    else if (elemento.tagName === 'INPUT') {
        const labelTexto = obterLabel(elemento);
        const tipo = elemento.type;
        
        if (tipo === 'text' || tipo === 'number' || tipo === 'email' || tipo === 'tel') {
            anuncio = `Campo: ${labelTexto}`;
            if (elemento.required) anuncio += ' - obligatorio';
            const valor = elemento.value;
            if (valor) anuncio += ` - valor actual: ${valor}`;
        } else if (tipo === 'checkbox') {
            const estado = elemento.checked ? 'marcado' : 'desmarcado';
            anuncio = `Casilla de verificación: ${labelTexto} - ${estado}`;
        } else if (tipo === 'radio') {
            const estado = elemento.checked ? 'seleccionado' : 'no seleccionado';
            anuncio = `Opción: ${labelTexto} - ${estado}`;
        } else if (tipo === 'submit') {
            anuncio = `Botón de envío: ${elemento.value || labelTexto}`;
        }
    }
    
    // Áreas de texto
    else if (elemento.tagName === 'TEXTAREA') {
        const labelTexto = obterLabel(elemento);
        anuncio = `Área de texto: ${labelTexto}`;
        if (elemento.required) anuncio += ' - obligatorio';
    }
    
    // Select
    else if (elemento.tagName === 'SELECT') {
        const labelTexto = obterLabel(elemento);
        const opcaoSelecionada = elemento.options[elemento.selectedIndex];
        anuncio = `Lista de selección: ${labelTexto}`;
        if (opcaoSelecionada) {
            anuncio += ` - seleccionado: ${opcaoSelecionada.text}`;
        }
    }
    
    return anuncio;
}

/**
 * Monitora foco em elementos
 */
function monitorarFoco() {
    document.addEventListener('focus', function(e) {
        const elemento = e.target;
        
        // Ignora se não for elemento válido
        if (!elemento || !elemento.tagName) {
            return;
        }
        
        const anuncio = gerarAnuncioFoco(elemento);
        
        if (anuncio && typeof anunciar !== 'undefined') {
            // Usa prioridade para interromper áudio anterior
            anunciar(anuncio, true);
        }
    }, true); // capture=true para pegar TODOS os eventos
}

/**
 * Cria região ARIA live para screen readers
 */
function criarRegiaoARIA() {
    const anunciador = document.createElement('div');
    anunciador.setAttribute('role', 'alert');
    anunciador.setAttribute('aria-live', 'assertive');
    anunciador.setAttribute('aria-atomic', 'true');
    anunciador.className = 'sr-only';
    anunciador.style.position = 'absolute';
    anunciador.style.left = '-10000px';
    anunciador.style.width = '1px';
    anunciador.style.height = '1px';
    anunciador.style.overflow = 'hidden';
    anunciador.style.clip = 'rect(1px, 1px, 1px, 1px)';
    document.body.appendChild(anunciador);
    
    console.log('✅ Região ARIA criada');
}

/**
 * Inicializa sistema de acessibilidade
 */
function inicializarAcessibilidade() {
    criarRegiaoARIA();
    monitorarFoco();
    console.log('✅ Sistema de acessibilidade inicializado');
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.obterLabel = obterLabel;
    window.gerarAnuncioFoco = gerarAnuncioFoco;
    window.inicializarAcessibilidade = inicializarAcessibilidade;
}
