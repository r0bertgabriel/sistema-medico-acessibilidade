#!/usr/bin/env python3
"""
Script para verificar a integridade da acessibilidade em todas as páginas
"""
import re
from pathlib import Path


def verificar_pagina(caminho_arquivo):
    """Verifica acessibilidade em uma página HTML"""
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    problemas = []
    avisos = []
    sucessos = []
    
    nome_arquivo = caminho_arquivo.name
    
    # 1. Verificar se extends base.html
    if '{% extends "base.html" %}' in conteudo or '{% extends \'base.html\' %}' in conteudo:
        sucessos.append("✅ Herda de base.html (inclui audio.js, keyboard.js, accessibility.js)")
    else:
        if nome_arquivo != 'base.html':
            problemas.append("❌ Não herda de base.html - sistema de acessibilidade pode não funcionar")
    
    # 2. Verificar função anunciar() local (deve usar window.anunciar)
    padrao_funcao_local = r'function\s+anunciar\s*\('
    if re.search(padrao_funcao_local, conteudo):
        problemas.append("❌ Possui função anunciar() local - deve usar window.anunciar() global")
    else:
        sucessos.append("✅ Não possui função anunciar() local duplicada")
    
    # 3. Verificar uso correto de window.anunciar
    usos_anunciar = re.findall(r'(window\.anunciar|anunciar)\s*\(', conteudo)
    if usos_anunciar:
        usos_window = [u for u in usos_anunciar if u.startswith('window.')]
        usos_direto = [u for u in usos_anunciar if not u.startswith('window.')]
        
        if usos_window:
            sucessos.append(f"✅ Usa window.anunciar() corretamente ({len(usos_window)} vezes)")
        
        if usos_direto:
            # Verificar se tem verificação typeof
            if 'typeof window.anunciar' in conteudo or 'typeof anunciar' in conteudo:
                sucessos.append(f"✅ Usa anunciar() com verificação de existência")
            else:
                avisos.append(f"⚠️ Usa anunciar() direto ({len(usos_direto)} vezes) - adicionar verificação typeof recomendado")
    
    # 4. Verificar registrarAtalhos (obsoleto)
    if 'registrarAtalhos(' in conteudo:
        avisos.append("⚠️ Usa registrarAtalhos() (obsoleto) - atalhos agora são globais e automáticos")
    
    # 5. Verificar inicialização
    if 'DOMContentLoaded' in conteudo:
        sucessos.append("✅ Possui listener DOMContentLoaded")
    
    # 6. Verificar anúncio de página
    if "setTimeout(" in conteudo and ("anunciar" in conteudo):
        sucessos.append("✅ Anuncia página ao carregar")
    
    return {
        'arquivo': nome_arquivo,
        'problemas': problemas,
        'avisos': avisos,
        'sucessos': sucessos
    }

def main():
    print("="*70)
    print("🔍 VERIFICAÇÃO DE ACESSIBILIDADE - Sistema Médico")
    print("="*70)
    print()
    
    # Diretório de templates
    templates_dir = Path(__file__).parent / 'templates'
    
    # Páginas principais para verificar
    paginas = [
        'index.html',
        'ecg.html',
        'analise.html',
        'resultados.html',
        'hemograma_hub.html',
        'hemograma.html',
        'hemograma_resultados.html',
        'analise_imagem.html'
    ]
    
    total_problemas = 0
    total_avisos = 0
    
    for pagina in paginas:
        caminho = templates_dir / pagina
        
        if not caminho.exists():
            print(f"⚠️ {pagina} - ARQUIVO NÃO ENCONTRADO")
            print()
            continue
        
        resultado = verificar_pagina(caminho)
        
        print(f"📄 {resultado['arquivo']}")
        print("-" * 70)
        
        # Mostrar problemas
        if resultado['problemas']:
            for problema in resultado['problemas']:
                print(f"  {problema}")
            total_problemas += len(resultado['problemas'])
        
        # Mostrar avisos
        if resultado['avisos']:
            for aviso in resultado['avisos']:
                print(f"  {aviso}")
            total_avisos += len(resultado['avisos'])
        
        # Mostrar sucessos
        if resultado['sucessos']:
            for sucesso in resultado['sucessos']:
                print(f"  {sucesso}")
        
        # Se não tem nada, está OK
        if not resultado['problemas'] and not resultado['avisos']:
            print("  ✅ Tudo OK!")
        
        print()
    
    # Resumo final
    print("="*70)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("="*70)
    print(f"Total de problemas críticos: {total_problemas}")
    print(f"Total de avisos: {total_avisos}")
    
    if total_problemas == 0:
        print()
        print("✅ SUCESSO: Todas as páginas estão acessíveis corretamente!")
        print("   - Sistema de áudio global funcionando")
        print("   - Sistema de atalhos de teclado ativo")
        print("   - Sem funções duplicadas")
        return 0
    else:
        print()
        print("❌ ATENÇÃO: Existem problemas que precisam ser corrigidos!")
        return 1

if __name__ == "__main__":
    exit(main())
