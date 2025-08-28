# -*- coding: utf-8 -*-
"""
components.py - Componentes visuais reutilizáveis da aplicação
"""

import time
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, 
    QGroupBox, QTextEdit, QSpinBox, QGridLayout, QPushButton
)
from PySide6.QtCore import QTimer
from styles import EstilosEspecificos

class PainelCozinheiro(QFrame):
    """Painel visual que representa um cozinheiro individual"""
    
    def __init__(self, nome, emoji="👨‍🍳"):
        super().__init__()
        self.setObjectName("PainelCozinheiro")
        self.setFrameShape(QFrame.StyledPanel)
        self.tarefas_concluidas = 0
        
        self._setup_ui(nome, emoji)
        self.resetar()

    def _setup_ui(self, nome, emoji):
        """Configura a interface do painel"""
        layout = QVBoxLayout()
        
        # Header do cozinheiro
        self.nome_label = QLabel(f"<center><span style='font-size: 24px;'>{emoji}</span><br><b>{nome}</b></center>")
        
        # Status
        self.status_label = QLabel("<center>😴 Aguardando pedido...</center>")
        
        # Barra de progresso
        self.progresso_bar = QProgressBar()
        self.progresso_bar.setStyleSheet("QProgressBar { height: 30px; }")
        
        # Labels de informação
        self.tempo_label = QLabel("<center>-</center>")
        self.tempo_label.setStyleSheet("color: #495057; font-size: 11px;")
        
        self.contador_label = QLabel("<center>Tarefas: 0</center>")
        self.contador_label.setStyleSheet("color: #495057; font-size: 11px; font-weight: bold;")
        
        # Adicionar widgets ao layout
        for widget in [self.nome_label, self.status_label, self.progresso_bar, 
                      self.tempo_label, self.contador_label]:
            layout.addWidget(widget)
        
        self.setLayout(layout)

    def iniciar_tarefa(self, nome_tarefa):
        """Inicia uma nova tarefa no painel"""
        self.status_label.setText(f"<center>🔥 <b>{nome_tarefa}</b></center>")
        self.status_label.setStyleSheet("color: #28a745; padding: 5px;")
        self.progresso_bar.setValue(0)
        self.tempo_label.setText("<center>⏱️ Trabalhando...</center>")
        self.setProperty("status", "trabalhando")
        self.style().unpolish(self)
        self.style().polish(self)

    def set_progresso(self, valor):
        """Atualiza o progresso da tarefa"""
        self.progresso_bar.setValue(valor)

    def tarefa_concluida(self, tempo_decorrido):
        """Marca uma tarefa como concluída"""
        self.tarefas_concluidas += 1
        self.contador_label.setText(f"<center>Tarefas: {self.tarefas_concluidas}</center>")
        self.tempo_label.setText(f"<center>⏱️ {tempo_decorrido:.1f}s</center>")

    def resetar(self):
        """Reseta o painel para estado inicial"""
        self.status_label.setText("<center>😴 Aguardando pedido...</center>")
        self.status_label.setStyleSheet("color: #6c757d; padding: 5px;")
        self.progresso_bar.setValue(0)
        self.tempo_label.setText("<center>-</center>")
        self.setProperty("status", "aguardando")
        self.style().unpolish(self)
        self.style().polish(self)

    def reset_contador(self):
        """Reseta apenas o contador de tarefas"""
        self.tarefas_concluidas = 0
        self.contador_label.setText("<center>Tarefas: 0</center>")

class PainelConfiguracoes(QGroupBox):
    """Painel com configurações da simulação"""
    
    def __init__(self):
        super().__init__("⚙️ Configurações")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QGridLayout(self)
        
        # Número de pedidos
        layout.addWidget(QLabel("Número de pedidos:"), 0, 0)
        self.spin_pedidos = QSpinBox()
        self.spin_pedidos.setRange(5, 50)
        self.spin_pedidos.setValue(10)
        layout.addWidget(self.spin_pedidos, 0, 1)
        
        # Tempo base
        layout.addWidget(QLabel("Tempo base (segundos):"), 1, 0)
        self.spin_tempo = QSpinBox()
        self.spin_tempo.setRange(1, 5)
        self.spin_tempo.setValue(2)
        layout.addWidget(self.spin_tempo, 1, 1)
    
    def get_num_pedidos(self):
        return self.spin_pedidos.value()
    
    def get_tempo_base(self):
        return self.spin_tempo.value()

class PainelControles(QGroupBox):
    """Painel com botões de controle"""
    
    def __init__(self):
        super().__init__("🎮 Controles")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        
        self.botao_sequencial = QPushButton("🔴 EXECUTAR SEQUENCIAL\n(Trava a Interface)")
        self.botao_sequencial.setObjectName("sequencial")
        
        self.botao_concorrente = QPushButton("🟢 EXECUTAR CONCORRENTE\n(Interface Livre)")
        self.botao_concorrente.setObjectName("concorrente")
        
        layout.addWidget(self.botao_sequencial)
        layout.addWidget(self.botao_concorrente)
    
    def conectar_eventos(self, callback_sequencial, callback_concorrente):
        """Conecta os callbacks dos botões"""
        self.botao_sequencial.clicked.connect(callback_sequencial)
        self.botao_concorrente.clicked.connect(callback_concorrente)
    
    def habilitar_botoes(self, habilitado=True):
        """Habilita ou desabilita os botões"""
        self.botao_sequencial.setEnabled(habilitado)
        self.botao_concorrente.setEnabled(habilitado)

class PainelMetricas(QGroupBox):
    """Painel com métricas de performance"""
    
    def __init__(self):
        super().__init__("📊 Métricas de Performance")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.label_tempo_total = QLabel("⏱️ Tempo Total: -")
        self.label_throughput = QLabel("🚀 Throughput: -")
        self.label_eficiencia = QLabel("⚡ Eficiência: -")
        
        for label in [self.label_tempo_total, self.label_throughput, self.label_eficiencia]:
            label.setStyleSheet(EstilosEspecificos.METRICAS_LABEL)
            layout.addWidget(label)
    
    def atualizar_metricas(self, tempo_total, pedidos_processados, modo):
        """Atualiza as métricas exibidas"""
        throughput = pedidos_processados / tempo_total if tempo_total > 0 else 0
        
        self.label_tempo_total.setText(f"⏱️ Tempo Total: {tempo_total:.1f}s")
        self.label_throughput.setText(f"🚀 Throughput: {throughput:.1f} pedidos/s")
        
        if modo == "CONCORRENTE":
            eficiencia = "🟢 Excelente (Interface livre!)"
        else:
            eficiencia = "🔴 Ruim (Interface travada!)"
        self.label_eficiencia.setText(f"⚡ Eficiência: {eficiencia}")

class PainelLog(QGroupBox):
    """Painel com log de execução"""
    
    def __init__(self):
        super().__init__("📝 Log de Execução")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.texto_log = QTextEdit()
        self.texto_log.setMaximumHeight(300)
        layout.addWidget(self.texto_log)
        
        self.botao_limpar = QPushButton("🗑️ Limpar Log")
        self.botao_limpar.setStyleSheet(EstilosEspecificos.BOTAO_LIMPAR_LOG)
        self.botao_limpar.clicked.connect(self.limpar_log)
        layout.addWidget(self.botao_limpar)
    
    def adicionar_mensagem(self, mensagem):
        """Adiciona uma mensagem ao log com timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        self.texto_log.append(f"[{timestamp}] {mensagem}")
    
    def limpar_log(self):
        """Limpa o conteúdo do log"""
        self.texto_log.clear()

class PainelDicas(QGroupBox):
    """Painel com dicas didáticas"""
    
    def __init__(self):
        super().__init__("💡 Dicas Didáticas")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        dicas_texto = QTextEdit()
        dicas_texto.setMaximumHeight(200)
        dicas_texto.setReadOnly(True)
        dicas_texto.setHtml(EstilosEspecificos.get_dicas_html())
        
        layout.addWidget(dicas_texto)