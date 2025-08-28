# -*- coding: utf-8 -*-
"""
main.py - Aplicação principal modular
"""

import sys
import time
import random
from collections import deque

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QSplitter
)
from PySide6.QtCore import QThreadPool, QMutex
from PySide6.QtGui import QFont

# Imports dos módulos locais
from styles import Estilos, EstilosEspecificos
from worker import Worker, TaskManager
from components import (
    PainelCozinheiro, PainelConfiguracoes, PainelControles,
    PainelMetricas, PainelLog, PainelDicas
)

class CozinhaSimulator(QMainWindow):
    """
    Aplicação principal - Simulador de Cozinha Concorrente vs Sequencial
    """
    
    def __init__(self):
        super().__init__()
        self.thread_pool = QThreadPool()
        self.mutex = QMutex()
        self.timer_inicio = None
        self.fila_de_tarefas = deque()
        
        self._setup_window()
        self._setup_ui()
        self._conectar_eventos()
        self._carregar_tarefas_inicial()

    def _setup_window(self):
        """Configurações básicas da janela"""
        self.setWindowTitle("🏭 Cozinha Concorrente vs Sequencial - Demonstração Didática")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(Estilos.get_complete_stylesheet())

    def _setup_ui(self):
        """Configura a interface do usuário"""
        # Widget principal com splitter
        splitter_principal = QSplitter()
        
        # Lado esquerdo - Visualização
        widget_esquerdo = self._criar_lado_esquerdo()
        splitter_principal.addWidget(widget_esquerdo)
        
        # Lado direito - Métricas e logs
        widget_direito = self._criar_lado_direito()
        splitter_principal.addWidget(widget_direito)
        
        splitter_principal.setSizes([700, 500])
        self.setCentralWidget(splitter_principal)

    def _criar_lado_esquerdo(self):
        """Cria o painel esquerdo com visualização"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Título e explicação
        self._adicionar_cabecalho(layout)
        
        # Painéis dos cozinheiros
        self._adicionar_paineis_cozinheiros(layout)
        
        # Configurações
        self.painel_config = PainelConfiguracoes()
        layout.addWidget(self.painel_config)
        
        # Controles
        self.painel_controles = PainelControles()
        layout.addWidget(self.painel_controles)
        
        # Fila de pedidos
        self._adicionar_fila_pedidos(layout)
        
        return widget

    def _criar_lado_direito(self):
        """Cria o painel direito com métricas e logs"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Métricas
        self.painel_metricas = PainelMetricas()
        layout.addWidget(self.painel_metricas)
        
        # Log
        self.painel_log = PainelLog()
        layout.addWidget(self.painel_log)
        
        # Dicas
        self.painel_dicas = PainelDicas()
        layout.addWidget(self.painel_dicas)
        
        return widget

    def _adicionar_cabecalho(self, layout):
        """Adiciona título e explicação"""
        titulo = QLabel("<center><h2>🏭 Simulação de Cozinha Industrial</h2></center>")
        titulo.setStyleSheet(EstilosEspecificos.TITULO_PRINCIPAL)
        layout.addWidget(titulo)
        
        explicacao = QLabel("""
        <center><b>🎯 Objetivo:</b> Comparar execução SEQUENCIAL (1 cozinheiro) vs CONCORRENTE (3 cozinheiros)<br>
        <b>🔴 Sequencial:</b> Um cozinheiro faz tudo sozinho (Interface trava!)<br>
        <b>🟢 Concorrente:</b> Três cozinheiros trabalham juntos (Interface livre!)
        </center>
        """)
        explicacao.setStyleSheet(EstilosEspecificos.EXPLICACAO_BOX)
        layout.addWidget(explicacao)

    def _adicionar_paineis_cozinheiros(self, layout):
        """Adiciona os painéis dos cozinheiros"""
        from PySide6.QtWidgets import QGroupBox
        
        cozinheiros_group = QGroupBox("👥 Equipe de Cozinheiros")
        layout_cozinheiros = QHBoxLayout(cozinheiros_group)
        
        self.cozinheiros = [
            PainelCozinheiro("Chef Principal", "👨‍🍳"),
            PainelCozinheiro("Sous Chef", "👩‍🍳"), 
            PainelCozinheiro("Cozinheiro Jr", "🧑‍🍳")
        ]
        
        for cozinheiro in self.cozinheiros:
            layout_cozinheiros.addWidget(cozinheiro)
        
        layout.addWidget(cozinheiros_group)

    def _adicionar_fila_pedidos(self, layout):
        """Adiciona a fila de pedidos"""
        from PySide6.QtWidgets import QGroupBox
        
        fila_group = QGroupBox("📋 Fila de Pedidos")
        layout_fila = QVBoxLayout(fila_group)
        
        self.lista_tarefas = QListWidget()
        self.lista_tarefas.setMaximumHeight(150)
        layout_fila.addWidget(self.lista_tarefas)
        
        layout.addWidget(fila_group)

    def _conectar_eventos(self):
        """Conecta os eventos da interface"""
        self.painel_controles.conectar_eventos(
            self.executar_sequencial,
            self.executar_concorrente
        )
        
        # Conecta o limpar log para resetar contadores também
        self.painel_log.botao_limpar.clicked.disconnect()
        self.painel_log.botao_limpar.clicked.connect(self._limpar_tudo)

    def _limpar_tudo(self):
        """Limpa log e reseta contadores dos cozinheiros"""
        self.painel_log.limpar_log()
        for cozinheiro in self.cozinheiros:
            cozinheiro.reset_contador()

    def _carregar_tarefas_inicial(self):
        """Carrega as tarefas iniciais na interface"""
        self._carregar_tarefas()

    def _carregar_tarefas(self):
        """Carrega tarefas na fila baseado nas configurações"""
        self.lista_tarefas.clear()
        self.fila_de_tarefas.clear()
        
        num_pedidos = self.painel_config.get_num_pedidos()
        tarefas = TaskManager.gerar_lista_tarefas(num_pedidos)
        
        for tarefa in tarefas:
            self.lista_tarefas.addItem(tarefa)
            self.fila_de_tarefas.append(tarefa)

    def _preparar_execucao(self, modo):
        """Prepara a interface para início da execução"""
        self.painel_controles.habilitar_botoes(False)
        self._carregar_tarefas()
        
        for cozinheiro in self.cozinheiros:
            cozinheiro.resetar()
            
        self.painel_log.adicionar_mensagem(f"🚀 INICIANDO MODO {modo}")
        self.painel_log.adicionar_mensagem(f"📋 {self.painel_config.get_num_pedidos()} pedidos na fila")

    def _finalizar_execucao(self, modo, pedidos_processados):
        """Finaliza a execução e atualiza métricas"""
        tempo_total = time.time() - self.timer_inicio
        
        self.painel_controles.habilitar_botoes(True)
        
        # Atualizar métricas
        self.painel_metricas.atualizar_metricas(tempo_total, pedidos_processados, modo)
        
        # Log final
        throughput = pedidos_processados / tempo_total if tempo_total > 0 else 0
        self.painel_log.adicionar_mensagem(f"🏁 {modo} FINALIZADO!")
        self.painel_log.adicionar_mensagem(f"📊 {pedidos_processados} pedidos em {tempo_total:.1f}s")
        self.painel_log.adicionar_mensagem(f"🚀 Throughput: {throughput:.1f} pedidos/segundo")
        self.painel_log.adicionar_mensagem("─" * 50)

    # ==================== EXECUÇÃO SEQUENCIAL ====================
    
    def executar_sequencial(self):
        """Executa as tarefas de forma sequencial (bloqueia a UI)"""
        self._preparar_execucao("SEQUENCIAL")
        self.timer_inicio = time.time()
        
        cozinheiro_painel = self.cozinheiros[0]  # Apenas o primeiro trabalha
        pedidos_processados = 0
        
        while self.fila_de_tarefas:
            nome_tarefa = self.fila_de_tarefas.popleft()
            self.lista_tarefas.takeItem(0)
            
            self.painel_log.adicionar_mensagem(f"👨‍🍳 Chef Principal iniciou: {nome_tarefa}")
            cozinheiro_painel.iniciar_tarefa(nome_tarefa)
            
            # Simula o trabalho (BLOQUEIA A UI!)
            tempo_tarefa = self.painel_config.get_tempo_base() + random.uniform(0.5, 1.5)
            inicio_tarefa = time.time()
            
            for prog in range(101):
                time.sleep(tempo_tarefa / 100)
                cozinheiro_painel.set_progresso(prog)
                QApplication.processEvents()  # Mínimo processamento
            
            tempo_real = time.time() - inicio_tarefa
            cozinheiro_painel.tarefa_concluida(tempo_real)
            cozinheiro_painel.resetar()
            pedidos_processados += 1
            
            self.painel_log.adicionar_mensagem(f"✅ Concluído: {nome_tarefa} ({tempo_real:.1f}s)")
        
        self._finalizar_execucao("SEQUENCIAL", pedidos_processados)

    # ==================== EXECUÇÃO CONCORRENTE ====================
    
    def executar_concorrente(self):
        """Executa as tarefas de forma concorrente (UI livre)"""
        self._preparar_execucao("CONCORRENTE")
        self.timer_inicio = time.time()
        
        # Inicia despachando para todos os cozinheiros
        for id_cozinheiro in range(len(self.cozinheiros)):
            self._despachar_proxima_tarefa(id_cozinheiro)

    def _despachar_proxima_tarefa(self, id_cozinheiro):
        """Despacha a próxima tarefa para um cozinheiro específico"""
        self.mutex.lock()
        
        if not self.fila_de_tarefas:
            self.mutex.unlock()
            if self.thread_pool.activeThreadCount() == 0:
                self._finalizar_execucao("CONCORRENTE", self.painel_config.get_num_pedidos())
            return

        nome_tarefa = self.fila_de_tarefas.popleft()
        self.mutex.unlock()
        
        self.lista_tarefas.takeItem(0)
        self.painel_log.adicionar_mensagem(f"👨‍🍳 Cozinheiro {id_cozinheiro+1} iniciou: {nome_tarefa}")

        # Criar e configurar worker
        worker = Worker(id_cozinheiro, nome_tarefa, self.painel_config.get_tempo_base())
        painel_cozinheiro = self.cozinheiros[id_cozinheiro]

        # Conectar sinais
        worker.sinais.iniciado.connect(painel_cozinheiro.iniciar_tarefa)
        worker.sinais.progresso.connect(painel_cozinheiro.set_progresso)
        worker.sinais.tempo_decorrido.connect(painel_cozinheiro.tarefa_concluida)
        worker.sinais.concluido.connect(self._tarefa_concluida)
        
        self.thread_pool.start(worker)

    def _tarefa_concluida(self, id_cozinheiro, nome_tarefa):
        """Callback chamado quando uma tarefa é concluída"""
        self.painel_log.adicionar_mensagem(f"✅ Cozinheiro {id_cozinheiro+1} concluiu: {nome_tarefa}")
        self.cozinheiros[id_cozinheiro].resetar()
        self._despachar_proxima_tarefa(id_cozinheiro)

# ==================== APLICAÇÃO PRINCIPAL ====================

def main():
    """Função principal da aplicação"""
    app = QApplication(sys.argv)
    
    # Configurar fonte global
    fonte = QFont("Arial", 10)
    app.setFont(fonte)
    
    # Criar e mostrar janela
    window = CozinhaSimulator()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())