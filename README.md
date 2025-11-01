# Sistema de Controle de Consumo de Insumos

Sistema completo para controle de consumo de insumos em unidades de diagnóstico, implementando estruturas de dados clássicas, algoritmos de busca e ordenação, além de otimização com Programação Dinâmica.

## 📋 Funcionalidades

### 1. Resolução 1 - Estruturas de Dados e Algoritmos Clássicos

#### 🔄 Fila (FIFO - First In, First Out)
**Contexto**: Registra o consumo diário de insumos em ordem cronológica.

**Implementação**:
- Estrutura baseada em lista Python
- Operações principais:
  - `enfileirar()`: Adiciona consumo no final (ordem cronológica)
  - `desenfileirar()`: Remove o consumo mais antigo (primeiro a entrar)
  - `ver_todos()`: Visualiza todos os registros na ordem de entrada

**Aplicação no problema**: 
A fila mantém o histórico de consumo na ordem temporal exata em que ocorreram. Isso é crucial para:
- Análise de tendências de consumo ao longo do tempo
- Relatórios cronológicos
- Processar consumos na ordem em que aconteceram (FIFO garante isso)

#### 📚 Pilha (LIFO - Last In, First Out)
**Contexto**: Permite consultar os consumos mais recentes primeiro, útil para análise de consumo atual.

**Implementação**:
- Estrutura baseada em lista Python
- Operações principais:
  - `empilhar()`: Adiciona consumo no topo
  - `desempilhar()`: Remove o consumo mais recente (último a entrar)
  - `topo()`: Consulta o consumo mais recente sem remover

**Aplicação no problema**:
A pilha é ideal para:
- Auditoria de consumos recentes
- Desfazer operações (se necessário)
- Análise dos últimos dias de consumo
- Verificação rápida do consumo mais recente

#### 🔍 Busca Sequencial
**Contexto**: Localiza todos os registros de um insumo específico.

**Implementação**:
- Percorre toda a lista elemento por elemento
- Compara o nome do insumo (case-insensitive)
- Retorna todas as ocorrências encontradas

**Complexidade**: O(n) - onde n é o número de registros

**Aplicação no problema**:
Útil quando:
- Os dados não estão ordenados
- Queremos todas as ocorrências de um insumo
- A lista é pequena (poucos registros)

**Vantagens**: Simples, funciona em qualquer situação, encontra todas as ocorrências

#### 🎯 Busca Binária
**Contexto**: Busca otimizada para listas ordenadas.

**Implementação**:
- Requer lista previamente ordenada por nome
- Divide a lista ao meio repetidamente
- Compara o elemento do meio e decide qual metade buscar
- Após encontrar, busca ocorrências adjacentes

**Complexidade**: O(log n) - muito mais rápido que busca sequencial

**Aplicação no problema**:
Ideal quando:
- Temos muitos registros
- Os dados podem ser mantidos ordenados
- Precisamos de busca rápida

**Vantagens**: Extremamente eficiente para grandes volumes de dados

#### 🔀 Merge Sort
**Contexto**: Ordena insumos por nome, quantidade ou validade.

**Implementação**:
- Algoritmo "Dividir e Conquistar"
- Divide a lista ao meio recursivamente
- Ordena cada metade
- Combina (merge) as metades ordenadas

**Complexidade**: O(n log n) - garantido em qualquer caso

**Aplicação no problema**:
- **Por nome**: Lista alfabética para facilitar localização
- **Por quantidade**: Identificar insumos mais/menos consumidos
- **Por validade**: Priorizar uso de insumos próximos ao vencimento

**Vantagens**: Desempenho consistente, estável (mantém ordem relativa)

#### ⚡ Quick Sort
**Contexto**: Ordenação rápida com pivô.

**Implementação**:
- Escolhe um pivô (elemento do meio)
- Particiona em: menores, iguais e maiores que o pivô
- Aplica recursivamente em cada partição

**Complexidade**: O(n log n) em média, O(n²) no pior caso

**Aplicação no problema**:
Mesmos critérios do Merge Sort:
- Nome, quantidade, validade

**Vantagens**: Geralmente mais rápido na prática, usa menos memória

### 2. Resolução 2 - Programação Dinâmica

#### 🎯 Formulação do Problema

**Objetivo**: Minimizar custos totais de gestão de estoque

**Estados**: 
- `dias[i]`: quantidade de insumos disponíveis no dia i
- `estoque[i]`: estoque disponível no início do dia i

**Decisões**: 
- Quanto pedir em cada dia (0 a capacidade_max)

**Função de Transição**:
```
estoque[i+1] = estoque[i] - consumo[i] + pedido[i]
```

**Função Objetivo** (Minimizar):
```
custo_total = Σ(custo_pedido + custo_armazenamento + custo_falta)
```

Onde:
- **custo_pedido**: R$ 100 fixo por pedido (quando pedido > 0)
- **custo_armazenamento**: R$ 1 por unidade/dia em estoque
- **custo_falta**: R$ 50 por unidade faltante

#### 🔄 Versão Recursiva com Memorização

**Implementação**:
```python
def recursivo(dia, estoque, memo):
    # Caso base: último dia
    if dia >= total_dias:
        return 0
    
    # Verifica cache
    if (dia, estoque) in memo:
        return memo[(dia, estoque)]
    
    # Tenta todas as possibilidades de pedido
    for pedido in possibilidades:
        custo_hoje = calcular_custo(estoque, consumo, pedido)
        custo_futuro = recursivo(dia+1, novo_estoque, memo)
        custo_total = custo_hoje + custo_futuro
        
        if custo_total < melhor_custo:
            melhor_custo = custo_total
    
    # Armazena no cache
    memo[(dia, estoque)] = melhor_custo
    return melhor_custo
```

**Características**:
- Top-down (começa do problema original)
- Usa memorização (cache) para evitar recálculos
- Mais intuitivo de entender

#### ⬆️ Versão Iterativa (Bottom-Up)

**Implementação**:
```python
def iterativo():
    # Tabela DP
    dp = [[None] * capacidade] * dias
    
    # Caso base: último dia
    for estoque in range(capacidade):
        dp[ultimo_dia][estoque] = 0
    
    # Preenche de trás para frente
    for dia in range(dias-1, -1, -1):
        for estoque in range(capacidade):
            for pedido in possibilidades:
                custo = calcular_custo(...)
                dp[dia][estoque] = min(dp[dia][estoque], custo)
    
    return dp[0][estoque_inicial]
```

**Características**:
- Bottom-up (começa dos subcasos)
- Preenche tabela sistematicamente
- Geralmente mais eficiente em memória

#### ✅ Garantia de Resultados Idênticos

Ambas as versões **produzem o mesmo resultado** porque:

1. **Mesma lógica**: Exploram todas as possibilidades de decisão
2. **Mesmos casos base**: Último dia tem custo 0
3. **Mesma transição**: Calculam custo de forma idêntica
4. **Otimalidade**: Ambas encontram o mínimo global

A diferença está apenas na **ordem de cálculo**:
- Recursiva: do problema original para subcasos
- Iterativa: dos subcasos para o problema original

## 🏗️ Estrutura do Código

```
app.py
├── Classes
│   ├── Insumo: Representa um insumo médico
│   ├── Fila: Implementação FIFO
│   ├── Pilha: Implementação LIFO
│   └── ProgramacaoDinamica: Otimização de estoque
│
├── Algoritmos
│   ├── busca_sequencial()
│   ├── busca_binaria()
│   ├── merge_sort()
│   └── quick_sort()
│
├── Menus Interativos
│   ├── menu_fila()
│   ├── menu_pilha()
│   ├── menu_busca_sequencial()
│   ├── menu_busca_binaria()
│   ├── menu_merge_sort()
│   ├── menu_quick_sort()
│   └── menu_programacao_dinamica()
│
└── Utilitários
    ├── gerar_dados_simulados()
    └── visualizar_dados()
```

## 💡 Conceitos Aplicados

### Estruturas de Dados
- **Fila**: Ordem cronológica (FIFO)
- **Pilha**: Ordem inversa (LIFO)
- **Lista**: Base para todas as estruturas

### Algoritmos de Busca
- **Sequencial**: O(n) - simples e funciona em qualquer caso
- **Binária**: O(log n) - eficiente para dados ordenados

### Algoritmos de Ordenação
- **Merge Sort**: O(n log n) - estável e consistente
- **Quick Sort**: O(n log n) médio - rápido na prática

### Programação Dinâmica
- **Memorização**: Cache de resultados (top-down)
- **Tabulação**: Preenchimento sistemático (bottom-up)
- **Otimização**: Encontra solução ótima

## 📊 Complexidade das Operações

| Operação | Complexidade | Descrição |
|----------|--------------|-----------|
| Fila - Enfileirar | O(1) | Adiciona no final |
| Fila - Desenfileirar | O(n) | Remove do início |
| Pilha - Empilhar | O(1) | Adiciona no topo |
| Pilha - Desempilhar | O(1) | Remove do topo |
| Busca Sequencial | O(n) | Percorre toda lista |
| Busca Binária | O(log n) | Divide pela metade |
| Merge Sort | O(n log n) | Divide e conquista |
| Quick Sort | O(n log n) médio | Particionamento |
| PD - Recursiva | O(dias × estoque × pedidos) | Com memorização |
| PD - Iterativa | O(dias × estoque × pedidos) | Bottom-up |

## 🎓 Aprendizados

1. **Fila vs Pilha**: Diferentes ordens de processamento para diferentes necessidades
2. **Busca**: Ordenação prévia pode acelerar drasticamente as buscas
3. **Ordenação**: Merge Sort é mais estável, Quick Sort é mais rápido
4. **Programação Dinâmica**: Decomposição em subproblemas + memorização = otimização
