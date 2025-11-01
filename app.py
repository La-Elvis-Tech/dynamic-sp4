"""
Sistema de Controle de Consumo de Insumos - Unidades de Diagnóstico
Implementação de estruturas de dados e algoritmos clássicos
"""
import os
os.system("clear")
import random
from datetime import datetime, timedelta


class Insumo:
    """Classe para representar um insumo médico"""
    def __init__(self, nome, quantidade, data, validade_dias=30):
        self.nome = nome
        self.quantidade = quantidade
        self.data = data
        self.validade = data + timedelta(days=validade_dias)
    
    def __str__(self):
        return f"{self.data.strftime('%Y-%m-%d')} | {self.nome:20s} | Qtd: {self.quantidade:4d} | Validade: {self.validade.strftime('%Y-%m-%d')}"
    
    def __repr__(self):
        return self.__str__()


class Fila:
    """Implementação de Fila para registrar consumo em ordem cronológica"""
    def __init__(self):
        self.items = []
    
    def enfileirar(self, item):
        """Adiciona item no final da fila"""
        self.items.append(item)
    
    def desenfileirar(self):
        """Remove e retorna o primeiro item da fila"""
        if not self.esta_vazia():
            return self.items.pop(0)
        return None
    
    def esta_vazia(self):
        return len(self.items) == 0
    
    def tamanho(self):
        return len(self.items)
    
    def ver_todos(self):
        return self.items.copy()


class Pilha:
    """Implementação de Pilha para consultar consumos em ordem inversa"""
    def __init__(self):
        self.items = []
    
    def empilhar(self, item):
        """Adiciona item no topo da pilha"""
        self.items.append(item)
    
    def desempilhar(self):
        """Remove e retorna o item do topo"""
        if not self.esta_vazia():
            return self.items.pop()
        return None
    
    def topo(self):
        """Retorna o item do topo sem remover"""
        if not self.esta_vazia():
            return self.items[-1]
        return None
    
    def esta_vazia(self):
        return len(self.items) == 0
    
    def tamanho(self):
        return len(self.items)
    
    def ver_todos(self):
        return self.items.copy()


def busca_sequencial(lista, nome_insumo):
    """Busca sequencial por nome do insumo"""
    resultados = []
    for i, insumo in enumerate(lista):
        if insumo.nome.lower() == nome_insumo.lower():
            resultados.append((i, insumo))
    return resultados


def busca_binaria(lista_ordenada, nome_insumo):
    """Busca binária por nome do insumo (lista deve estar ordenada por nome)"""
    esquerda, direita = 0, len(lista_ordenada) - 1
    
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        nome_meio = lista_ordenada[meio].nome.lower()
        nome_busca = nome_insumo.lower()
        
        if nome_meio == nome_busca:
            resultados = [(meio, lista_ordenada[meio])]
            i = meio - 1
            while i >= 0 and lista_ordenada[i].nome.lower() == nome_busca:
                resultados.insert(0, (i, lista_ordenada[i]))
                i -= 1
            i = meio + 1
            while i < len(lista_ordenada) and lista_ordenada[i].nome.lower() == nome_busca:
                resultados.append((i, lista_ordenada[i]))
                i += 1
            return resultados
        elif nome_meio < nome_busca:
            esquerda = meio + 1
        else:
            direita = meio - 1
    
    return []


def merge_sort(lista, criterio='nome'):
    """
    Merge Sort - Divide e conquista
    Critérios: 'nome', 'quantidade', 'validade'
    """
    if len(lista) <= 1:
        return lista
    
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio], criterio)
    direita = merge_sort(lista[meio:], criterio)
    
    return merge(esquerda, direita, criterio)


def merge(esquerda, direita, criterio):
    """Combina duas listas ordenadas"""
    resultado = []
    i = j = 0
    
    while i < len(esquerda) and j < len(direita):
        if comparar(esquerda[i], direita[j], criterio):
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


def quick_sort(lista, criterio='nome'):
    """
    Quick Sort - Divide e conquista com pivô
    Critérios: 'nome', 'quantidade', 'validade'
    """
    if len(lista) <= 1:
        return lista
    
    pivo = lista[len(lista) // 2]
    menores = [x for x in lista if comparar(x, pivo, criterio) and x != pivo]
    iguais = [x for x in lista if not comparar(x, pivo, criterio) and not comparar(pivo, x, criterio)]
    maiores = [x for x in lista if comparar(pivo, x, criterio) and x != pivo]
    
    return quick_sort(menores, criterio) + iguais + quick_sort(maiores, criterio)


def comparar(insumo1, insumo2, criterio):
    """Função auxiliar para comparar insumos por diferentes critérios"""
    if criterio == 'nome':
        return insumo1.nome.lower() < insumo2.nome.lower()
    elif criterio == 'quantidade':
        return insumo1.quantidade < insumo2.quantidade
    elif criterio == 'validade':
        return insumo1.validade < insumo2.validade
    return False


class ProgramacaoDinamica:
    """
    Solução de otimização de estoque usando Programação Dinâmica
    
    Problema: Minimizar desperdício e garantir disponibilidade de insumos
    
    Estados: dias[i] = quantidade de insumos disponíveis no dia i
    Decisão: quantidade a pedir em cada dia
    Transição: estoque[i+1] = estoque[i] - consumo[i] + pedido[i]
    Objetivo: minimizar custo total (pedidos + armazenamento + falta)
    """
    
    def __init__(self, consumo_diario, custo_pedido=100, custo_armazenamento=1, custo_falta=50):
        self.consumo = consumo_diario
        self.dias = len(consumo_diario)
        self.custo_pedido = custo_pedido
        self.custo_armazenamento = custo_armazenamento
        self.custo_falta = custo_falta
        self.capacidade_max = max(consumo_diario) * 3
    
    def calcular_custo(self, estoque, consumo, pedido):
        """Calcula custo total de uma decisão"""
        custo = 0
        
        if pedido > 0:
            custo += self.custo_pedido
        
        estoque_final = estoque - consumo + pedido
        
        if estoque_final > 0:
            custo += estoque_final * self.custo_armazenamento
        
        if estoque_final < 0:
            custo += abs(estoque_final) * self.custo_falta
            estoque_final = 0
        
        return custo, estoque_final
    
    def recursivo(self, dia=0, estoque=0, memo=None):
        """Versão recursiva com memorização"""
        if memo is None:
            memo = {}
        
        if dia >= self.dias:
            return 0, []
        
        if (dia, estoque) in memo:
            return memo[(dia, estoque)]
        
        melhor_custo = float('inf')
        melhor_decisao = []
        
        consumo_hoje = self.consumo[dia]
        for pedido in range(0, self.capacidade_max + 1, 10):
            custo_hoje, novo_estoque = self.calcular_custo(estoque, consumo_hoje, pedido)
            
            if novo_estoque > self.capacidade_max:
                continue
            
            custo_futuro, decisoes_futuras = self.recursivo(dia + 1, novo_estoque, memo)
            custo_total = custo_hoje + custo_futuro
            
            if custo_total < melhor_custo:
                melhor_custo = custo_total
                melhor_decisao = [pedido] + decisoes_futuras
        
        memo[(dia, estoque)] = (melhor_custo, melhor_decisao)
        return melhor_custo, melhor_decisao
    
    def iterativo(self, estoque_inicial=0):
        """Versão iterativa (bottom-up)"""
        dp = [[None for _ in range(self.capacidade_max + 1)] for _ in range(self.dias + 1)]
        
        for estoque in range(self.capacidade_max + 1):
            dp[self.dias][estoque] = (0, 0)
        
        for dia in range(self.dias - 1, -1, -1):
            consumo_hoje = self.consumo[dia]
            for estoque in range(self.capacidade_max + 1):
                melhor_custo = float('inf')
                melhor_pedido = 0
                
                for pedido in range(0, self.capacidade_max + 1, 10):
                    custo_hoje, novo_estoque = self.calcular_custo(estoque, consumo_hoje, pedido)
                    
                    if novo_estoque > self.capacidade_max:
                        continue
                    
                    custo_futuro = dp[dia + 1][novo_estoque][0]
                    custo_total = custo_hoje + custo_futuro
                    
                    if custo_total < melhor_custo:
                        melhor_custo = custo_total
                        melhor_pedido = pedido
                
                dp[dia][estoque] = (melhor_custo, melhor_pedido)
        
        decisoes = []
        estoque = estoque_inicial
        custo_total = dp[0][estoque][0]
        
        for dia in range(self.dias):
            pedido = dp[dia][estoque][1]
            decisoes.append(pedido)
            _, estoque = self.calcular_custo(estoque, self.consumo[dia], pedido)
        
        return custo_total, decisoes


def gerar_dados_simulados(num_registros=20):
    """Gera dados simulados de consumo de insumos"""
    insumos_tipos = [
        "Reagente PCR",
        "Seringa 5ml",
        "Luva Descartável",
        "Álcool 70%",
        "Máscara N95",
        "Swab Nasofaríngeo",
        "Tubo de Coleta",
        "Agulha 25G",
        "Gaze Estéril"
    ]
    
    dados = []
    data_inicio = datetime.now() - timedelta(days=num_registros)
    
    for i in range(num_registros):
        nome = random.choice(insumos_tipos)
        quantidade = random.randint(5, 200)
        data = data_inicio + timedelta(days=i)
        validade_dias = random.randint(15, 60)
        
        insumo = Insumo(nome, quantidade, data, validade_dias)
        dados.append(insumo)
    
    return dados


def limpar_tela():
    """Simula limpeza de tela"""
    print("\n" * 2)


def exibir_menu_principal():
    print("=" * 70)
    print(" SISTEMA DE CONTROLE DE CONSUMO DE INSUMOS ".center(70))
    print("=" * 70)
    print("\nMENU PRINCIPAL\n")
    print("1 - Fila (Registrar consumo em ordem cronológica)")
    print("2 - Pilha (Consultar consumos em ordem inversa)")
    print("3 - Busca Sequencial")
    print("4 - Busca Binária")
    print("5 - Ordenação com Merge Sort")
    print("6 - Ordenação com Quick Sort")
    print("7 - Programação Dinâmica (Otimização de Estoque)")
    print("8 - Gerar novos dados simulados")
    print("9 - Visualizar todos os dados")
    print("0 - Sair")
    print("\n" + "=" * 70)


def menu_fila(dados):
    """Menu para operações com Fila"""
    fila = Fila()
    
    for insumo in dados:
        fila.enfileirar(insumo)
    
    while True:
        limpar_tela()
        print("=" * 70)
        print(" FILA - Consumo Cronológico (FIFO) ".center(70))
        print("=" * 70)
        print(f"\nItens na fila: {fila.tamanho()}\n")
        print("1 - Visualizar fila completa")
        print("2 - Desenfileirar (remover primeiro)")
        print("3 - Adicionar novo consumo")
        print("0 - Voltar")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n" + "=" * 70)
            print(" FILA COMPLETA ".center(70))
            print("=" * 70)
            items = fila.ver_todos()
            if items:
                for i, item in enumerate(items, 1):
                    print(f"{i:2d}. {item}")
            else:
                print("Fila vazia!")
            input("\n[Pressione ENTER para continuar]")
        
        elif opcao == "2":
            item = fila.desenfileirar()
            if item:
                print(f"\nItem removido: {item}")
            else:
                print("\nFila vazia!")
            input("\n[Pressione ENTER para continuar]")
        
        elif opcao == "3":
            print("\n" + "=" * 70)
            print(" ADICIONAR NOVO CONSUMO ".center(70))
            print("=" * 70)
            nome = input("Nome do insumo: ").strip()
            try:
                qtd = int(input("Quantidade: ").strip())
                val_dias = int(input("Validade (dias): ").strip())
                novo = Insumo(nome, qtd, datetime.now(), val_dias)
                fila.enfileirar(novo)
                print(f"\nAdicionado: {novo}")
            except ValueError:
                print("\nValores inválidos!")
            input("\n[Pressione ENTER para continuar]")
        
        elif opcao == "0":
            break


def menu_pilha(dados):
    """Menu para operações com Pilha"""
    pilha = Pilha()
    
    for insumo in dados:
        pilha.empilhar(insumo)
    
    while True:
        limpar_tela()
        print("=" * 70)
        print(" PILHA - Consulta Inversa (LIFO) ".center(70))
        print("=" * 70)
        print(f"\nItens na pilha: {pilha.tamanho()}\n")
        print("1 - Visualizar pilha completa")
        print("2 - Ver topo")
        print("3 - Desempilhar (remover topo)")
        print("4 - Adicionar no topo")
        print("0 - Voltar")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n" + "=" * 70)
            print(" PILHA COMPLETA (topo no final) ".center(70))
            print("=" * 70)
            items = pilha.ver_todos()
            if items:
                for i, item in enumerate(items, 1):
                    print(f"{i:2d}. {item}")
            else:
                print("Pilha vazia!")
            input("\n[Pressione ENTER para continuar]")
        
        elif opcao == "2":
            item = pilha.topo()
            if item:
                print(f"\nTopo: {item}")
            else:
                print("\nPilha vazia!")
            input("\n[Pressione ENTER para continuar]")
        
        elif opcao == "3":
            item = pilha.desempilhar()
            if item:
                print(f"\nItem removido: {item}")
            else:
                print("\nPilha vazia!")
            input("\n[Pressione ENTER para continuar]")
        
        elif opcao == "4":
            print("\n" + "=" * 70)
            print(" ADICIONAR NO TOPO ".center(70))
            print("=" * 70)
            nome = input("Nome do insumo: ").strip()
            try:
                qtd = int(input("Quantidade: ").strip())
                val_dias = int(input("Validade (dias): ").strip())
                novo = Insumo(nome, qtd, datetime.now(), val_dias)
                pilha.empilhar(novo)
                print(f"\nAdicionado: {novo}")
            except ValueError:
                print("\nValores inválidos!")
            input("\n[Pressione ENTER para continuar]")
        
        elif opcao == "0":
            break


def menu_busca_sequencial(dados):
    """Menu para busca sequencial"""
    limpar_tela()
    print("=" * 70)
    print(" BUSCA SEQUENCIAL ".center(70))
    print("=" * 70)
    print("\nBusca por nome do insumo (percorre toda a lista)\n")
    
    nome = input("Digite o nome do insumo para buscar: ").strip()
    
    resultados = busca_sequencial(dados, nome)
    
    print("\n" + "=" * 70)
    print(f" RESULTADOS ({len(resultados)} encontrado(s)) ".center(70))
    print("=" * 70)
    
    if resultados:
        for idx, insumo in resultados:
            print(f"Posição {idx}: {insumo}")
    else:
        print("Nenhum resultado encontrado!")
    
    input("\n[Pressione ENTER para continuar]")


def menu_busca_binaria(dados):
    """Menu para busca binária"""
    limpar_tela()
    print("=" * 70)
    print(" BUSCA BINÁRIA ".center(70))
    print("=" * 70)
    print("\nBusca otimizada (requer lista ordenada por nome)\n")
    
    dados_ordenados = merge_sort(dados.copy(), 'nome')
    
    print("Ordenando dados por nome...")
    nome = input("Digite o nome do insumo para buscar: ").strip()
    
    resultados = busca_binaria(dados_ordenados, nome)
    
    print("\n" + "=" * 70)
    print(f" RESULTADOS ({len(resultados)} encontrado(s)) ".center(70))
    print("=" * 70)
    
    if resultados:
        for idx, insumo in resultados:
            print(f"Posição {idx}: {insumo}")
    else:
        print("Nenhum resultado encontrado!")
    
    input("\n[Pressione ENTER para continuar]")


def menu_merge_sort(dados):
    """Menu para ordenação com Merge Sort"""
    limpar_tela()
    print("=" * 70)
    print(" MERGE SORT ".center(70))
    print("=" * 70)
    print("\nEscolha o critério de ordenação:\n")
    print("1 - Por nome")
    print("2 - Por quantidade")
    print("3 - Por validade")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    criterios = {'1': 'nome', '2': 'quantidade', '3': 'validade'}
    criterio = criterios.get(opcao, 'nome')
    
    print(f"\nOrdenando por {criterio}...")
    dados_ordenados = merge_sort(dados.copy(), criterio)
    
    print("\n" + "=" * 70)
    print(f" DADOS ORDENADOS POR {criterio.upper()} ".center(70))
    print("=" * 70)
    
    for i, insumo in enumerate(dados_ordenados, 1):
        print(f"{i:2d}. {insumo}")
    
    input("\n[Pressione ENTER para continuar]")


def menu_quick_sort(dados):
    """Menu para ordenação com Quick Sort"""
    limpar_tela()
    print("=" * 70)
    print(" QUICK SORT ".center(70))
    print("=" * 70)
    print("\nEscolha o critério de ordenação:\n")
    print("1 - Por nome")
    print("2 - Por quantidade")
    print("3 - Por validade")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    criterios = {'1': 'nome', '2': 'quantidade', '3': 'validade'}
    criterio = criterios.get(opcao, 'nome')
    
    print(f"\nOrdenando por {criterio}...")
    dados_ordenados = quick_sort(dados.copy(), criterio)
    
    print("\n" + "=" * 70)
    print(f" DADOS ORDENADOS POR {criterio.upper()} ".center(70))
    print("=" * 70)
    
    for i, insumo in enumerate(dados_ordenados, 1):
        print(f"{i:2d}. {insumo}")
    
    input("\n[Pressione ENTER para continuar]")


def menu_programacao_dinamica():
    """Menu para Programação Dinâmica"""
    limpar_tela()
    print("=" * 70)
    print(" PROGRAMAÇÃO DINÂMICA - Otimização de Estoque ".center(70))
    print("=" * 70)
    print("\nProblema: Minimizar custos de pedido, armazenamento e falta\n")
    
    dias = 10
    consumo_diario = [random.randint(20, 100) for _ in range(dias)]
    
    print("Consumo diário simulado:")
    for i, consumo in enumerate(consumo_diario, 1):
        print(f"  Dia {i}: {consumo} unidades")
    
    print("\nParâmetros:")
    print(f"  - Custo de pedido: R$ 100 (fixo)")
    print(f"  - Custo de armazenamento: R$ 1 por unidade/dia")
    print(f"  - Custo de falta: R$ 50 por unidade faltante")
    
    input("\n[Pressione ENTER para calcular soluções]")
    
    pd = ProgramacaoDinamica(consumo_diario)
    
    print("\n" + "=" * 70)
    print(" SOLUÇÃO RECURSIVA (com memorização) ".center(70))
    print("=" * 70)
    custo_rec, decisoes_rec = pd.recursivo()
    print(f"\nCusto total: R$ {custo_rec:.2f}")
    print("\nDecisões de pedido por dia:")
    for i, pedido in enumerate(decisoes_rec, 1):
        print(f"  Dia {i}: pedir {pedido} unidades")
    
    input("\n[Pressione ENTER para ver solução iterativa]")
    
    print("\n" + "=" * 70)
    print(" SOLUÇÃO ITERATIVA (bottom-up) ".center(70))
    print("=" * 70)
    custo_iter, decisoes_iter = pd.iterativo()
    print(f"\nCusto total: R$ {custo_iter:.2f}")
    print("\nDecisões de pedido por dia:")
    for i, pedido in enumerate(decisoes_iter, 1):
        print(f"  Dia {i}: pedir {pedido} unidades")
    
    print("\n" + "=" * 70)
    print(" COMPARAÇÃO ".center(70))
    print("=" * 70)
    print(f"Ambas as soluções produziram o mesmo resultado: {custo_rec == custo_iter}")
    print(f"Diferença: R$ {abs(custo_rec - custo_iter):.2f}")
    
    input("\n[Pressione ENTER para continuar]")


def visualizar_dados(dados):
    """Visualiza todos os dados"""
    limpar_tela()
    print("=" * 70)
    print(" TODOS OS REGISTROS DE CONSUMO ".center(70))
    print("=" * 70)
    print(f"\nTotal de registros: {len(dados)}\n")
    
    for i, insumo in enumerate(dados, 1):
        print(f"{i:2d}. {insumo}")
    
    input("\n[Pressione ENTER para continuar]")


def main():
    """Função principal do programa"""
    dados = gerar_dados_simulados(20)
    
    while True:
        limpar_tela()
        exibir_menu_principal()
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            menu_fila(dados)
        elif opcao == "2":
            menu_pilha(dados)
        elif opcao == "3":
            menu_busca_sequencial(dados)
        elif opcao == "4":
            menu_busca_binaria(dados)
        elif opcao == "5":
            menu_merge_sort(dados)
        elif opcao == "6":
            menu_quick_sort(dados)
        elif opcao == "7":
            menu_programacao_dinamica()
        elif opcao == "8":
            num = input("\nQuantos registros gerar? (padrão 20): ").strip()
            try:
                num = int(num) if num else 20
                dados = gerar_dados_simulados(num)
                print(f"\n{num} registros gerados com sucesso!")
            except ValueError:
                print("\nValor inválido, gerando 20 registros...")
                dados = gerar_dados_simulados(20)
            input("\n[Pressione ENTER para continuar]")
        elif opcao == "9":
            visualizar_dados(dados)
        elif opcao == "0":
            print("\n" + "=" * 70)
            print(" Encerrando sistema... Até logo! ".center(70))
            print("=" * 70 + "\n")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
            input("\n[Pressione ENTER para continuar]")


if __name__ == "__main__":
    main()
