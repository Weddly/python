funcAvalicacao = (lambda x: x**2-3*x+4)

def gerarIndividuoStr(tm_bits):
    import random as rd
    val=''
    for _ in range(tm_bits):
        if rd.randint(1,10) <=5:
            val +='0'
        else:
            val +='1'
    return val

def gerarPopulacaoInicial(tm_pop, tm_bits):
    pop = []
    for _ in range (tm_pop):
        individuo = gerarIndividuoStr(tm_bits)
        pop.append(individuo)

    return pop

def converterBinarioPraDecimal(pop):
    pop_decimal = []
    for item in range(len(pop)-1):
        pop_decimal.append(int(pop[item], 2))
    return pop_decimal

def gerarfatorDeConversao(max_binario, max_faixa, min_faixa):
    fator = 0
    faixa = max_faixa-(min_faixa)
    fator = faixa/max_binario
    return fator

def converterPopParaFitness(fatorDeConversao, pop_decimal):
    valorAvaliado = [((fatorDeConversao*ind) - 10) for ind in pop_decimal]
    return valorAvaliado

def avaliarPopFitness(pop_inicial, fator_de_conversao, funcAvalicacao):
    pop_decimal = converterBinarioPraDecimal(pop_inicial)
    pop_fit = converterPopParaFitness(fator_de_conversao, pop_decimal)
    resultado_aval = [funcAvalicacao(ind) for ind in pop_fit]
    return resultado_aval

def definirMelhorDaPop(pop, resultado_fit):
    index_melhor_da_pop = 0
    i = 0
    while i < (len(pop) - 1):
        if resultado_fit[i] < resultado_fit[index_melhor_da_pop] :
            index_melhor_da_pop = i
        i += 1
    return index_melhor_da_pop

def realizarTorneio(resultado_fit):
    import random as rd
    index1 = rd.randint(0, (len(resultado_fit)-1))
    index2 = rd.randint(0, (len(resultado_fit)-1))
    if resultado_fit[index1] < resultado_fit[index2]:
        return index1
    else:
        return index2

def gerarMutacao(pop, taxa_mut, tm_pop, tm_bits):
    import random as rd
    cromossomo = 0
    gene = 0
    for _ in range(taxa_mut):
        cromossomo = rd.randint(1, (tm_pop-1))
        gene = rd.randint(0, (tm_bits-1))
        cromossomo_aleatorio = pop[cromossomo]
        gene_aleatorio = cromossomo_aleatorio[gene]
        if(int(gene_aleatorio) == 0):
            pop[cromossomo] = cromossomo_aleatorio[:gene] + '1' + cromossomo_aleatorio[gene + 1 :]
        else:
            pop[cromossomo] = cromossomo_aleatorio[:gene] + '0' + cromossomo_aleatorio[gene + 1 :]

def gerarCrossover(pai, mae, posicao_corte):
    corte = posicao_corte
    filhos = []
    if(corte == 0):
        filho1 = pai
        filho2 = mae
    else: 
        filho1 = pai[:corte] + mae[corte:]
        filho2 = mae[:corte] + pai[corte:]
    filhos.append(filho1)
    filhos.append(filho2)
    return filhos

tm_bits = 10
tm_pop = 10
max_binario = 1023
max_faixa = 10
min_faixa = -10
taxa_mut = 20
usaElitismo = True
qtd_geracoes = 1000
posicao_corte = 7

pop_inicial = []
nova_pop = []
pop_decimal = []
pop_fit = []
resultado_fit = []

fator_de_conversao = gerarfatorDeConversao(max_binario, max_faixa, min_faixa)
conta_geracao = 1

while conta_geracao <= qtd_geracoes: 
    print('Geracao: ', conta_geracao)
    if(len(pop_inicial) == 0):
        pop_inicial = gerarPopulacaoInicial(tm_pop, tm_bits)
    # print('Populacao inicial', pop_inicial)
    resultado_fit = avaliarPopFitness(pop_inicial, fator_de_conversao, funcAvalicacao)
    if usaElitismo == True:
        indexMelhor = definirMelhorDaPop(pop_inicial, resultado_fit)
        nova_pop.append(pop_inicial[indexMelhor])
        print('Melhor da populacao', int(nova_pop[0],2))
    while len(nova_pop) < tm_pop:
        index_mae = realizarTorneio(resultado_fit)
        index_pai = realizarTorneio(resultado_fit)
        if index_mae == index_pai:
            nova_pop.append(pop_inicial[index_mae])
        else:
            resultado_cross = gerarCrossover(pop_inicial[index_mae], pop_inicial[index_pai], posicao_corte)
            nova_pop.append(resultado_cross[0])
            if len(nova_pop) < tm_pop:
                nova_pop.append(resultado_cross[1])
    gerarMutacao(nova_pop, taxa_mut, tm_pop, tm_bits)
    pop_inicial = nova_pop
    nova_pop = []
    conta_geracao += 1

melhor_indice_final = definirMelhorDaPop(pop_inicial, resultado_fit)
binario_final = pop_inicial[melhor_indice_final]
decimal_final = [int(binario_final,2)]
fit_final = converterPopParaFitness(fator_de_conversao, decimal_final)
resultado_fit_final = resultado_fit[melhor_indice_final]



print('RESULTADO FINAL')
print('Valor binario:', binario_final)
print('Valor decimal:', decimal_final[0])
print('Valor de X:', fit_final[0])
print('Valor de y:', resultado_fit_final)