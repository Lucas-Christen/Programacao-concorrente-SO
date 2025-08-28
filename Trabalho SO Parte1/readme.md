# 🏭 Cozinha Concorrente - Projeto Modular

## 📁 Estrutura de Arquivos

```
cozinha_concorrente/
│
├── main.py           # ← Aplicação principal (execute este!)
├── styles.py         # ← Estilos e cores
├── worker.py         # ← Classes de threading
├── components.py     # ← Componentes da UI
└── README.md         # ← Este arquivo
```

## 🚀 Como Executar

```bash
python main.py
```

## 📋 Descrição dos Módulos

### 🎨 `styles.py` - Estilos e Temas
- **`Cores`**: Paleta de cores centralizada
- **`Estilos`**: Estilos CSS organizados por componente
- **`EstilosEspecificos`**: Estilos para elementos únicos

**Vantagens da modularização:**
- ✅ Fácil mudança de tema (edite apenas `Cores`)
- ✅ Estilos organizados por componente
- ✅ Reutilização em outras partes do projeto

### 🔧 `worker.py` - Threading e Processamento
- **`WorkerSignals`**: Sinais para comunicação thread-safe
- **`Worker`**: Classe que executa tarefas em background
- **`TaskManager`**: Gerenciador de tarefas e geração de nomes

**Vantagens da modularização:**
- ✅ Lógica de threading isolada
- ✅ Fácil modificação dos tempos de simulação
- ✅ Geração de tarefas configurável

### 🎛️ `components.py` - Componentes Visuais
- **`PainelCozinheiro`**: Representação visual de um cozinheiro
- **`PainelConfiguracoes`**: Controles de configuração
- **`PainelControles`**: Botões principais
- **`PainelMetricas`**: Display de performance
- **`PainelLog`**: Log de execução
- **`PainelDicas`**: Dicas didáticas

**Vantagens da modularização:**
- ✅ Componentes reutilizáveis
- ✅ Fácil manutenção da UI
- ✅ Separação clara de responsabilidades

### 🏠 `main.py` - Aplicação Principal
- **`CozinhaSimulator`**: Janela principal
- Orquestra todos os componentes
- Gerencia a lógica de negócio
- Coordena execução sequencial vs concorrente

## 🎯 Benefícios da Modularização

### 1. **Manutenibilidade** 🔧
- Cada arquivo tem uma responsabilidade específica
- Mudanças são localizadas e controladas
- Fácil de debugar e testar

### 2. **Reutilização** ♻️
- Componentes podem ser usados em outros projetos
- Estilos centralizados evitam duplicação
- Workers podem ser adaptados para outras tarefas

### 3. **Escalabilidade** 📈
- Fácil adicionar novos tipos de cozinheiro
- Simples implementar novos temas visuais
- Componentes podem ser estendidos independentemente

### 4. **Colaboração** 👥
- Diferentes desenvolvedores podem trabalhar em módulos diferentes
- Conflitos de merge reduzidos
- Código mais organizado para revisão

## 🛠️ Como Modificar

### Mudar Cores/Tema:
```python
# Edite styles.py
class Cores:
    FUNDO_PRINCIPAL = "#SUA_COR_AQUI"  # Mude aqui!
```

### Adicionar Novo Tipo de Cozinheiro:
```python
# Edite components.py
class PainelChefEspecialista(PainelCozinheiro):
    def __init__(self):
        super().__init__("Chef Especialista", "👨‍🍳⭐")
```

### Modificar Tipos de Prato:
```python
# Edite worker.py
class TaskManager:
    PRATOS_DISPONIVEIS = [
        "🍕 Sua Pizza Customizada",
        # Adicione seus pratos aqui!
    ]
```

### Adicionar Nova Métrica:
```python
# Edite components.py -> PainelMetricas
def _setup_ui(self):
    # Adicione sua nova métrica aqui
    self.label_nova_metrica = QLabel("🆕 Nova Métrica: -")
```

## 📚 Conceitos Didáticos Demonstrados

1. **Threading vs Bloqueio de UI**
2. **Modularização de Código**
3. **Separação de Responsabilidades**
4. **Padrão Observer (Signals/Slots)**
5. **Gerenciamento de Estado**
6. **Interface Responsiva**

## 🎓 Exercícios Sugeridos

1. **Fácil**: Mude as cores do tema
2. **Médio**: Adicione um 4º cozinheiro
3. **Difícil**: Implemente diferentes velocidades por cozinheiro
4. **Avançado**: Adicione sistema de prioridade de pedidos

## 🐛 Troubleshooting

**Problema**: Interface não atualiza durante execução sequencial
- **Causa**: Comportamento esperado! É para demonstrar o bloqueio
- **Solução**: Use o modo concorrente

**Problema**: Cores não aparecem corretamente  
- **Causa**: Possível problema com aplicação de estilos
- **Solução**: Verifique se `setStyleSheet()` está sendo chamado

**Problema**: Workers não param corretamente
- **Causa**: Possível problema com mutex ou sinais
- **Solução**: Verifique as conexões de sinais em `main.py`