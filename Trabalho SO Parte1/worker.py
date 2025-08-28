# -*- coding: utf-8 -*-
"""
worker.py - Classes responsáveis pelo threading e processamento
"""

import time
import random
from PySide6.QtCore import QObject, QRunnable, Signal, Slot

class WorkerSignals(QObject):
    """Sinais emitidos pelo Worker para comunicação com a UI"""
    iniciado = Signal(str)
    progresso = Signal(int)
    concluido = Signal(int, str)
    tempo_decorrido = Signal(float)

class Worker(QRunnable):
    """
    Worker que executa tarefas em background sem bloquear a UI
    """
    
    def __init__(self, id_cozinheiro, nome_tarefa, tempo_base=2.0):
        super().__init__()
        self.id_cozinheiro = id_cozinheiro
        self.nome_tarefa = nome_tarefa
        self.tempo_base = tempo_base
        self.sinais = WorkerSignals()

    @Slot()
    def run(self):
        """Executa a tarefa simulada"""
        inicio = time.time()
        self.sinais.iniciado.emit(self.nome_tarefa)
        
        # Simula trabalho com tempo mais realista
        tempo_total = self.tempo_base + random.uniform(0.5, 1.5)
        passos = 100
        
        for i in range(passos + 1):
            time.sleep(tempo_total / passos)
            self.sinais.progresso.emit(i)
        
        tempo_decorrido = time.time() - inicio
        self.sinais.tempo_decorrido.emit(tempo_decorrido)
        self.sinais.concluido.emit(self.id_cozinheiro, self.nome_tarefa)

class TaskManager:
    """Gerenciador de tarefas com diferentes pratos"""
    
    PRATOS_DISPONIVEIS = [
        "🍝 Spaghetti Carbonara", 
        "🍕 Pizza Margherita", 
        "🥘 Risotto", 
        "🍖 Bife Grelhado", 
        "🐟 Salmão Grelhado", 
        "🍲 Ensopado", 
        "🥗 Salada Caesar", 
        "🍜 Ramen", 
        "🧀 Lasanha", 
        "🍤 Camarão"
    ]
    
    @staticmethod
    def gerar_nome_tarefa(numero_mesa):
        """Gera um nome de tarefa realista"""
        prato = random.choice(TaskManager.PRATOS_DISPONIVEIS)
        return f"Mesa {numero_mesa:02d}: {prato}"
    
    @staticmethod
    def gerar_lista_tarefas(num_pedidos):
        """Gera uma lista de tarefas para a fila"""
        return [
            TaskManager.gerar_nome_tarefa(i + 1) 
            for i in range(num_pedidos)
        ]