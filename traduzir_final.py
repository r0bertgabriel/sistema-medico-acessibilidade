#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

# Dicionário completo de traduções
TRADUCOES = {
    # Frases completas
    "ECG de 12 derivações em repouso, ritmo sinusal estável, sem alterações significativas": "ECG de 12 derivaciones en reposo, ritmo sinusal estable, sin alteraciones significativas",
    "Precede cada complexo QRS, morfologia normal": "Precede cada complejo QRS, morfología normal",
    "Duração do QRS": "Duración del QRS",
    "morfologia normal": "morfología normal",
    "Eletrocardiograma dentro dos limites de normalidade para adulto com ritmo sinusal": "Electrocardiograma dentro de los límites de normalidad para adulto con ritmo sinusal",
    "Não evidenciados sinais de sobrecarga atrial ou ventricular, bloqueios de ramo, isquemia ou arritmia persistente": "No se evidencian signos de sobrecarga auricular o ventricular, bloqueos de rama, isquemia o arritmia persistente",
    "Gerar laudo do ECG normal": "Generar informe del ECG normal",
    "ECG com bloqueio de ramo direito incompleto e alterações secundárias da repolarização": "ECG con bloqueo de rama derecha incompleto y alteraciones secundarias de la repolarización",
    "ECG compatível com bloqueio de ramo direito": "ECG compatible con bloqueo de rama derecha",
    "incompleto": "incompleto",
    "Em paciente sem sintomas e sem achados estruturais relevantes, costuma ter bom prognóstico": "En paciente sin síntomas y sin hallazgos estructurales relevantes, suele tener buen pronóstico",
    "Sugere-se correlação clínica e, se indicado": "Se sugiere correlación clínica y, si indicado",
    "sopro, história pulmonar ou cardíaca": "soplo, historia pulmonar o cardíaca",
    "exame de eco ou investigação adicional": "examen de eco o investigación adicional",
    
    # Termos individuais
    "parâmetros": "parámetros",
    "alterações": "alteraciones",
    "sem ": "sin ",
    "Sem ": "Sin ",
    " normal": " normal",
    "normais": "normales",
    "sugestivas": "sugestivas",
    "morfologia": "morfología",
    "Conclusão": "Conclusión",
    "Descrição": "Descripción",
    "disponíveis": "disponibles",
    "caracteres especiais": "caracteres especiales",
    "Áudio otimizado sem caracteres especiais": "Audio optimizado sin caracteres especiales",
    "O laudo é convertido em áudio otimizado": "El informe se convierte en audio optimizado",
    "Página de resultados carregada": "Página de resultados cargada",
    "Três exemplos disponíveis": "Tres ejemplos disponibles",
    "Pressione barra para ajuda completa": "Presione barra espaciadora para ayuda completa",
    "ajuda completa": "ayuda completa",
}

def traduzir_arquivo(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    for pt, es in TRADUCOES.items():
        conteudo = conteudo.replace(pt, es)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"✅ {caminho}")

# Traduzir arquivos
traduzir_arquivo("templates/resultados.html")
traduzir_arquivo("templates/analise.html")
traduzir_arquivo("templates/analise_imagem.html")
traduzir_arquivo("templates/hemograma.html")
print("✅ Tradução final concluída!")
