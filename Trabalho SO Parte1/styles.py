# -*- coding: utf-8 -*-
"""
styles.py - Estilos e temas visuais da aplicação
"""

# Cores do tema personalizado
class Cores:
    # Cores principais do tema
    BACKGROUND = "#2d2d2d"
    TEXT = "#ecf0f1"
    PRIMARY = "#ff0808"
    SECONDARY = "#fd9494"
    ACCENT = "#ffbb00"
    
    # Cores derivadas para componentes específicos
    FUNDO_PRINCIPAL = BACKGROUND
    TEXTO_PRINCIPAL = TEXT
    PAINEL_NORMAL = "#3d3d3d"  # Um pouco mais claro que o background
    PAINEL_TRABALHANDO = ACCENT  # Amarelo para indicar trabalho
    PAINEL_AGUARDANDO = "#4d4d4d"  # Cinza mais claro
    
    BOTAO_SEQUENCIAL = PRIMARY
    BOTAO_SEQUENCIAL_HOVER = "#e60707"  # Primary mais escuro
    BOTAO_CONCORRENTE = ACCENT
    BOTAO_CONCORRENTE_HOVER = "#e6a800"  # Accent mais escuro
    BOTAO_DESABILITADO = "#5d5d5d"
    
    PROGRESSO_BAR = SECONDARY
    FUNDO_BRANCO = "#f5f5f5"  # Branco suave
    TEXTO_ESCURO = "#1d1d1d"
    ESPECIAL = SECONDARY  # Para elementos especiais

# Estilos CSS organizados por componente
class Estilos:
    
    @staticmethod
    def get_main_style():
        return f"""
        QMainWindow, QWidget {{
            background-color: {Cores.FUNDO_PRINCIPAL};
            color: {Cores.TEXTO_PRINCIPAL};
        }}
        QLabel {{
            color: {Cores.TEXTO_PRINCIPAL};
        }}
        """
    
    @staticmethod
    def get_painel_cozinheiro_style():
        return f"""
        QFrame#PainelCozinheiro {{
            border: 3px solid {Cores.PAINEL_NORMAL};
            border-radius: 12px;
            background-color: {Cores.PAINEL_NORMAL};
            margin: 5px;
            padding: 15px;
            color: {Cores.TEXTO_PRINCIPAL};
        }}
        QFrame#PainelCozinheiro[status="trabalhando"] {{
            border: 3px solid {Cores.ACCENT};
            background-color: {Cores.PAINEL_TRABALHANDO};
            color: {Cores.BACKGROUND};
        }}
        QFrame#PainelCozinheiro[status="aguardando"] {{
            border: 3px solid {Cores.BOTAO_DESABILITADO};
            background-color: {Cores.PAINEL_AGUARDANDO};
            color: {Cores.TEXT};
        }}
        """
    
    @staticmethod
    def get_button_style():
        return f"""
        QPushButton {{
            font-size: 14px;
            font-weight: bold;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 15px 20px;
            min-height: 25px;
        }}
        QPushButton#sequencial {{
            background-color: {Cores.BOTAO_SEQUENCIAL};
            border: 2px solid {Cores.BOTAO_SEQUENCIAL_HOVER};
        }}
        QPushButton#sequencial:hover {{
            background-color: {Cores.BOTAO_SEQUENCIAL_HOVER};
        }}
        QPushButton#concorrente {{
            background-color: {Cores.BOTAO_CONCORRENTE};
            border: 2px solid {Cores.BOTAO_CONCORRENTE_HOVER};
        }}
        QPushButton#concorrente:hover {{
            background-color: {Cores.BOTAO_CONCORRENTE_HOVER};
        }}
        QPushButton:disabled {{
            background-color: {Cores.BOTAO_DESABILITADO};
            color: {Cores.SECONDARY};
            border: 2px solid {Cores.PAINEL_AGUARDANDO};
        }}
        """
    
    @staticmethod
    def get_list_and_progress_style():
        return f"""
        QListWidget {{
            font-size: 13px;
            border: 2px solid {Cores.PAINEL_NORMAL};
            border-radius: 8px;
            background-color: {Cores.FUNDO_BRANCO};
            color: {Cores.TEXTO_ESCURO};
            alternate-background-color: {Cores.SECONDARY};
        }}
        QProgressBar {{
            border: 2px solid {Cores.PAINEL_NORMAL};
            border-radius: 6px;
            text-align: center;
            font-weight: bold;
            color: {Cores.TEXTO_ESCURO};
            height: 30px;
            background-color: {Cores.FUNDO_BRANCO};
        }}
        QProgressBar::chunk {{
            background-color: {Cores.PROGRESSO_BAR};
            border-radius: 4px;
            margin: 1px;
        }}
        """
    
    @staticmethod
    def get_group_and_input_style():
        return f"""
        QGroupBox {{
            font-weight: bold;
            font-size: 15px;
            color: {Cores.TEXTO_PRINCIPAL};
            border: 2px solid {Cores.PAINEL_NORMAL};
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 20px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 10px 0 10px;
            background-color: {Cores.FUNDO_PRINCIPAL};
            color: {Cores.TEXTO_PRINCIPAL};
        }}
        QTextEdit {{
            border: 2px solid {Cores.PAINEL_NORMAL};
            border-radius: 8px;
            background-color: {Cores.FUNDO_BRANCO};
            color: {Cores.TEXTO_ESCURO};
            font-family: "Consolas", "Monaco", monospace;
            font-size: 12px;
        }}
        QSpinBox {{
            background-color: {Cores.FUNDO_BRANCO};
            color: {Cores.TEXTO_ESCURO};
            border: 2px solid {Cores.PAINEL_NORMAL};
            border-radius: 5px;
            padding: 5px;
            font-size: 13px;
        }}
        """
    
    @staticmethod
    def get_complete_stylesheet():
        """Retorna o stylesheet completo combinando todos os estilos"""
        return (
            Estilos.get_main_style() + 
            Estilos.get_painel_cozinheiro_style() + 
            Estilos.get_button_style() + 
            Estilos.get_list_and_progress_style() + 
            Estilos.get_group_and_input_style()
        )

# Estilos específicos para componentes individuais
class EstilosEspecificos:
    
    TITULO_PRINCIPAL = f"color: {Cores.TEXTO_PRINCIPAL}; margin: 10px; font-weight: bold;"
    
    EXPLICACAO_BOX = f"""
    background-color: {Cores.PAINEL_NORMAL}; 
    border: 2px solid {Cores.TEXTO_PRINCIPAL}; 
    border-radius: 8px; 
    padding: 15px; 
    margin: 5px; 
    color: {Cores.TEXTO_PRINCIPAL};
    """
    
    METRICAS_LABEL = f"""
    font-size: 14px; 
    padding: 8px; 
    background-color: {Cores.PAINEL_NORMAL}; 
    color: {Cores.TEXTO_PRINCIPAL}; 
    border: 2px solid {Cores.TEXTO_PRINCIPAL}; 
    border-radius: 6px; 
    margin: 3px; 
    font-weight: bold;
    """
    
    BOTAO_LIMPAR_LOG = f"""
    background-color: {Cores.ESPECIAL}; 
    color: {Cores.BACKGROUND}; 
    padding: 8px; 
    border-radius: 5px;
    font-weight: bold;
    """
    
    @staticmethod
    def get_dicas_html():
        return f"""
        <b style='color: {Cores.PRIMARY};'>🔴 Modo Sequencial:</b><br>
        • Tente mover a janela durante execução<br>
        • Note que TUDO trava<br>
        • Apenas 1 cozinheiro trabalha<br><br>
        
        <b style='color: {Cores.ACCENT};'>🟢 Modo Concorrente:</b><br>
        • Interface permanece responsiva<br>
        • 3 cozinheiros trabalham juntos<br>
        • Muito mais rápido!<br><br>
        
        <b style='color: {Cores.SECONDARY};'>🎯 Lição:</b> NUNCA bloqueie a UI!
        """