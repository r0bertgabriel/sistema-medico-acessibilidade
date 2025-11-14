"""
Casos prontos de ECG para análise por imagem
Cada caso contém a imagem e o laudo correspondente
"""

CASOS_PRONTOS = {
    'arritmia_sinusal': {
        'nome': 'Arritmia Sinusal',
        'imagem_exemplo': 'arritmia_sinusal.png',
        'laudo_completo': """\
LAUDO DE ELETROCARDIOGRAMA

1. RITMO E FREQUÊNCIA
Ritmo sinusal com ondas P positivas em D2, D3 e aVF, uma P para cada QRS.
Frequência cardíaca: aproximadamente 85 batimentos por minuto, regular.

2. INTERVALOS
Intervalo PR: normal, aproximadamente 0,16 segundos.
QRS: estreito, aproximadamente 0,08 segundos.
QTc: normal, aproximadamente 0,42 segundos.

3. EIXO ELÉTRICO
Eixo do QRS ligeiramente desviado para a esquerda, entre menos 15 e menos 20 graus.

4. MORFOLOGIA DOS COMPLEXOS
Derivações precordiais V1 a V3: complexos RSR prime, com ondas R prime altas e S profundas, sugerindo padrão de bloqueio incompleto de ramo direito.
Derivações V4 a V6: ondas R amplas, progressão normal.

5. SEGMENTO ST E ONDA T
Leve infradesnivelamento do segmento ST em V2 a V3, associado a ondas T invertidas nessas derivações.
Isso sugere sobrecarga ventricular direita ou alterações secundárias de repolarização por bloqueio incompleto de ramo direito.
Nas derivações inferiores e laterais, ST e T normais.

6. CONCLUSÃO INTERPRETATIVA
Ritmo sinusal.
Frequência 85 batimentos por minuto.
Bloqueio incompleto do ramo direito.
Alterações secundárias da repolarização com T invertida em V1 a V3.
Sem sinais de isquemia aguda, necrose ou sobrecarga importante.

CONCLUSÃO FINAL
Eletrocardiograma com ritmo sinusal, frequência cardíaca normal, bloqueio incompleto do ramo direito e alterações secundárias da repolarização ventricular. Ausência de sinais de isquemia ou infarto agudo do miocárdio.

INFORMAÇÕES ADICIONAIS SOBRE ARRITMIA SINUSAL
Ondas P sinusais normais, positivas nas derivações 1 e 2, com morfologia constante, embora com aparência sugestiva de aumento do átrio esquerdo.
O intervalo PR é constante, sem evidência de bloqueio AV.
O intervalo PP varia amplamente, de 1,04 segundos, frequência cardíaca de aproximadamente 57 batimentos por minuto, até 0,60 segundos, frequência cardíaca de aproximadamente 100 batimentos por minuto. Uma variabilidade de mais de 400 milissegundos.
Para ritmos irregulares como este, a frequência ventricular é melhor estimada multiplicando-se o número total de complexos na tira de ritmo por 6, resultando em uma frequência geral de 72 batimentos por minuto.
""",
        'laudo_audio': """Laudo de eletrocardiograma. Ritmo sinusal com ondas P positivas em D2, D3 e aVF. Frequência cardíaca: 85 batimentos por minuto. Intervalo PR normal, aproximadamente 0,16 segundos. QRS estreito, 0,08 segundos. QTc normal. Eixo do QRS levemente desviado para esquerda. Derivações V1 a V3: padrão de bloqueio incompleto de ramo direito. Leve infradesnivelamento do segmento ST em V2 a V3, com ondas T invertidas. Sugere sobrecarga ventricular direita ou alterações secundárias de repolarização. Conclusão: Ritmo sinusal, frequência normal, bloqueio incompleto do ramo direito, alterações secundárias da repolarização. Sem sinais de isquemia aguda ou infarto. Informações adicionais: Intervalo PP varia de 1,04 a 0,60 segundos, variabilidade de mais de 400 milissegundos. Frequência geral estimada em 72 batimentos por minuto.""",
        'diagnostico': 'Arritmia Sinusal com Bloqueio Incompleto de Ramo Direito',
        'gravidade': 'Baixa',
        'principais_achados': [
            'Ritmo sinusal regular',
            'Bloqueio incompleto de ramo direito',
            'Alterações de repolarização em V1-V3',
            'Variabilidade do intervalo PP'
        ]
    }
}


def obter_caso_por_nome(nome_arquivo):
    """
    Identifica o caso baseado no nome do arquivo
    """
    nome_lower = nome_arquivo.lower()
    
    # Tentar identificar pelo nome do arquivo
    if 'arritmia' in nome_lower or 'sinusal' in nome_lower:
        return CASOS_PRONTOS['arritmia_sinusal']
    
    # Retornar caso padrão
    return CASOS_PRONTOS['arritmia_sinusal']


def processar_laudo_para_audio(laudo_completo):
    """
    Remove caracteres desnecessários do laudo para áudio (emojis, símbolos especiais)
    Mantém apenas o texto essencial
    """
    import re
    
    # Remove emojis e símbolos especiais
    laudo_limpo = re.sub(r'[^\w\s\.,;:()\-áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]', '', laudo_completo)
    
    # Remove linhas com apenas símbolos ou vazias
    linhas = [linha.strip() for linha in laudo_limpo.split('\n') if linha.strip()]
    
    # Remove marcadores de seção desnecessários
    laudo_limpo = '\n'.join(linhas)
    
    # Remove múltiplos espaços
    laudo_limpo = re.sub(r'\s+', ' ', laudo_limpo)
    
    # Remove linhas separadoras
    laudo_limpo = re.sub(r'-{3,}', '', laudo_limpo)
    
    return laudo_limpo.strip()
