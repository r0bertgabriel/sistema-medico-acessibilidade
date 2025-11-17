"""
Exemplos de dados de hemogramas para testes e demonstrações
"""
from models.hemograma_data import DadosHemograma


def obter_exemplos_hemograma():
    """Retorna dicionário com exemplos de hemogramas"""
    
    return {
        "normal": DadosHemograma(
            nome_paciente="Juan Silva",
            idade=35,
            sexo="M",
            data_coleta="12/11/2025",
            hemacias=5.0,
            hemoglobina=15.0,
            hematocrito=45.0,
            vcm=90.0,
            hcm=30.0,
            chcm=34.0,
            rdw=13.0,
            leucocitos=7000,
            neutrofilos=4000,
            segmentados=3800,
            bastonetes=200,
            linfocitos=2000,
            monocitos=500,
            eosinofilos=200,
            basofilos=50,
            plaquetas=250000,
            observacoes="Hemograma de rotina."
        ),
        
        "anemia_microcitica": DadosHemograma(
            nome_paciente="María Santos",
            idade=42,
            sexo="F",
            data_coleta="12/11/2025",
            hemacias=3.5,
            hemoglobina=10.0,
            hematocrito=32.0,
            vcm=75.0,
            hcm=25.0,
            chcm=32.0,
            rdw=16.5,
            leucocitos=6500,
            neutrofilos=3500,
            linfocitos=2200,
            monocitos=450,
            eosinofilos=180,
            basofilos=40,
            plaquetas=280000,
            observacoes="Paciente refere fadiga e palidez há 3 meses."
        ),
        
        "leucocitose_neutrofilia": DadosHemograma(
            nome_paciente="Pedro Oliveira",
            idade=28,
            sexo="M",
            data_coleta="12/11/2025",
            hemacias=4.8,
            hemoglobina=14.5,
            hematocrito=43.0,
            vcm=88.0,
            hcm=29.0,
            chcm=33.5,
            rdw=12.8,
            leucocitos=15000,
            neutrofilos=11000,
            segmentados=10000,
            bastonetes=1000,
            linfocitos=2500,
            monocitos=800,
            eosinofilos=300,
            basofilos=60,
            plaquetas=320000,
            observacoes="Quadro febril há 2 dias, dor abdominal."
        ),
        
        "plaquetopenia": DadosHemograma(
            nome_paciente="Ana Costa",
            idade=55,
            sexo="F",
            data_coleta="12/11/2025",
            hemacias=4.2,
            hemoglobina=13.0,
            hematocrito=39.0,
            vcm=92.0,
            hcm=31.0,
            chcm=34.0,
            rdw=13.2,
            leucocitos=6800,
            neutrofilos=3800,
            linfocitos=2100,
            monocitos=520,
            eosinofilos=210,
            basofilos=45,
            plaquetas=95000,
            observacoes="Aparecimento de petéquias em membros inferiores."
        ),
        
        "anemia_macrocitica": DadosHemograma(
            nome_paciente="Carlos Ferreira",
            idade=68,
            sexo="M",
            data_coleta="12/11/2025",
            hemacias=3.2,
            hemoglobina=10.5,
            hematocrito=33.0,
            vcm=105.0,
            hcm=33.0,
            chcm=32.0,
            rdw=15.5,
            leucocitos=5500,
            neutrofilos=3000,
            linfocitos=1800,
            monocitos=400,
            eosinofilos=150,
            basofilos=30,
            plaquetas=180000,
            observacoes="Paciente vegetariano há 5 anos, queixa de cansaço."
        ),
        
        "eosinofilia": DadosHemograma(
            nome_paciente="Juliana Álvarez",
            idade=25,
            sexo="F",
            data_coleta="12/11/2025",
            hemacias=4.5,
            hemoglobina=13.5,
            hematocrito=40.0,
            vcm=89.0,
            hcm=30.0,
            chcm=33.5,
            rdw=12.5,
            leucocitos=9000,
            neutrofilos=4500,
            linfocitos=2000,
            monocitos=500,
            eosinofilos=1500,
            basofilos=50,
            plaquetas=240000,
            observacoes="História de rinite alérgica e dermatite atópica."
        ),
        
        "leucopenia": DadosHemograma(
            nome_paciente="Roberto Lima",
            idade=52,
            sexo="M",
            data_coleta="12/11/2025",
            hemacias=4.6,
            hemoglobina=14.0,
            hematocrito=42.0,
            vcm=91.0,
            hcm=30.5,
            chcm=33.5,
            rdw=13.0,
            leucocitos=3000,
            neutrofilos=1500,
            linfocitos=1000,
            monocitos=300,
            eosinofilos=100,
            basofilos=20,
            plaquetas=200000,
            observacoes="Em uso de quimioterapia para linfoma."
        ),
        
        "policitemia": DadosHemograma(
            nome_paciente="Fernando Souza",
            idade=60,
            sexo="M",
            data_coleta="12/11/2025",
            hemacias=6.5,
            hemoglobina=18.5,
            hematocrito=55.0,
            vcm=92.0,
            hcm=31.0,
            chcm=34.0,
            rdw=12.0,
            leucocitos=11000,
            neutrofilos=6500,
            linfocitos=2500,
            monocitos=800,
            eosinofilos=250,
            basofilos=70,
            plaquetas=480000,
            observacoes="Fumante há 30 anos, trabalha em alta altitude."
        )
    }


def obter_hemograma_por_nome(nome: str) -> DadosHemograma:
    """
    Retorna um hemograma específico pelo nome
    
    Args:
        nome: Nome do exemplo (normal, anemia, leucocitose, etc)
        
    Returns:
        Instância de DadosHemograma
    """
    exemplos = obter_exemplos_hemograma()
    return exemplos.get(nome, exemplos["normal"])
