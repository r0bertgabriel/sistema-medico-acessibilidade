#!/usr/bin/env python3
"""
Script de teste para verificar as rotas de hemograma
"""
import json

import requests

BASE_URL = "http://localhost:5000"

def testar_exemplo_hemograma(tipo):
    """Testa obtenção de exemplo de hemograma"""
    print(f"\n{'='*60}")
    print(f"🔍 Testando exemplo: {tipo}")
    print(f"{'='*60}")
    
    try:
        # 1. Obter exemplo
        url = f"{BASE_URL}/api/hemograma/exemplo/{tipo}"
        print(f"📡 GET {url}")
        response = requests.get(url, timeout=5)
        
        print(f"Status: {response.status_code}")
        data = response.json()
        
        if data.get('success'):
            print("✅ Exemplo obtido com sucesso!")
            exemplo = data['exemplo']
            print(f"   Paciente: {exemplo['paciente']['nome']}")
            print(f"   Idade: {exemplo['paciente']['idade']}")
            print(f"   Sexo: {exemplo['paciente']['sexo']}")
            
            # 2. Analisar exemplo
            print(f"\n📊 Analisando exemplo...")
            url_analise = f"{BASE_URL}/api/analisar_hemograma"
            response_analise = requests.post(
                url_analise, 
                json=exemplo,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            print(f"Status: {response_analise.status_code}")
            resultado = response_analise.json()
            
            if resultado.get('success'):
                print("✅ Análise concluída!")
                print(f"   Áudio: {resultado.get('audio_url', 'N/A')}")
                print(f"   Alterações: {len(resultado.get('alteracoes', []))}")
                print(f"   Flags: {resultado.get('flags', [])}")
                
                # Mostrar primeiras linhas do laudo
                laudo = resultado.get('laudo', '')
                linhas = laudo.split('\n')[:5]
                print(f"\n📋 Primeiras linhas do laudo:")
                for linha in linhas:
                    print(f"   {linha}")
                
                return True
            else:
                print(f"❌ Erro na análise: {resultado.get('error')}")
                return False
        else:
            print(f"❌ Erro ao obter exemplo: {data.get('error')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar ao servidor!")
        print("   Verifique se o servidor está rodando em http://localhost:5000")
        return False
    except requests.exceptions.Timeout:
        print("❌ ERRO: Timeout na requisição!")
        return False
    except Exception as e:
        print(f"❌ ERRO: {type(e).__name__}: {e}")
        return False


def main():
    print("="*60)
    print("🧪 TESTE DE ROTAS DE HEMOGRAMA")
    print("="*60)
    
    # Verificar se servidor está rodando
    try:
        response = requests.get(BASE_URL, timeout=2)
        print(f"✅ Servidor está rodando!")
    except:
        print(f"❌ Servidor não está rodando em {BASE_URL}")
        print("   Execute: python app.py")
        return
    
    # Testar diferentes tipos
    tipos = ['normal', 'anemia', 'leucocitose', 'plaquetopenia']
    resultados = {}
    
    for tipo in tipos:
        sucesso = testar_exemplo_hemograma(tipo)
        resultados[tipo] = sucesso
    
    # Resumo
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*60}")
    
    for tipo, sucesso in resultados.items():
        status = "✅" if sucesso else "❌"
        print(f"{status} {tipo}")
    
    total = len(resultados)
    sucessos = sum(1 for s in resultados.values() if s)
    print(f"\n🎯 Total: {sucessos}/{total} testes bem-sucedidos")


if __name__ == "__main__":
    main()
