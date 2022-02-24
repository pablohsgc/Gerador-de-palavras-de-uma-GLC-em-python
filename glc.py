#coding: utf-8
import sys 
import json


#Metodo para ler o arquivo e retornar um dicionario json
def ler_json(nome_arquivo):
	with open(nome_arquivo,'r',encoding='utf8') as f:
		return json.load(f)

#Metodo utilizado para contar a quantidade de simbolos em uma palavra
def conta_simbolos(palavra,simbolos): 
	quantidade_de_simbolos = 0

	for caractere in palavra:
		if caractere in simbolos:
			quantidade_de_simbolos = quantidade_de_simbolos + 1

	return quantidade_de_simbolos

#Metodo que verifica se uma palavra contem variaveis
def nao_contem_variavel(palavra,variaveis):
	for caractere in palavra:
		if caractere in variaveis:
			return False
	return True

#Metodo que formara as palavras
def forma_palavras(variaveis,simbolos,regras,variavel_de_partida,tamanho):
	lista_de_trabalho = list()
	palavras_formadas = list()
	lista_de_ocorrencias = list()

	#Adiciona a lista apenas regras que partem da variavel de partida
	for tupla_regra in regras:
		if tupla_regra[0] == variavel_de_partida:
			lista_de_trabalho.append(tupla_regra[1]) 
			lista_de_ocorrencias.append(tupla_regra[1])


	while len(lista_de_trabalho) > 0:
		#print(lista_de_trabalho)# comentario para debugar erro
		#retira a primeira regra de formacao de palavras da lista
		regra_aux = lista_de_trabalho.pop(0)

		for tupla_regra in regras: # percorre as regras com suas respectivas variaveis
			#Retira a variavel e a regra
			variavel = tupla_regra[0]
			regra = tupla_regra[1]
					
			#Susbtitui a primeira ocorrencia onde a regra pode ser substituida
			palavra = regra_aux.replace(variavel,regra,1) 

			if conta_simbolos(palavra,simbolos) <= tamanho:
				if nao_contem_variavel(palavra,variaveis) and (palavra not in palavras_formadas):
					palavras_formadas.append(palavra)

				elif palavra not in lista_de_ocorrencias: # se a palavra nunca foi adicionada na lista, e contem variavel
					lista_de_trabalho.append(palavra) 
					lista_de_ocorrencias.append(palavra)
				
				if conta_simbolos(palavra,simbolos) > tamanho:
					print("quantidade de simbolos maior que tamanho:",conta_simbolos(palavra,simbolos))

	return palavras_formadas

#Metodo que remove todos os lambdas de uma palavra
def remove_lambdas(lista_de_palavras,simbolo_Lambda):
	retorno = list()

	for palavra in lista_de_palavras:
		nova_palavra = palavra.replace(simbolo_Lambda,"")
		if nova_palavra not in retorno:
			retorno.append(nova_palavra)

	return retorno

def glc():
	#le os valores da linha de comando
	if len(sys.argv) < 3:
		print("Usar: python [GLC] [Tamanho máximo]")
		exit(1)

	nome = sys.argv[1]
	tamanho = int(sys.argv[2])
	
	#le o json
	dados = ler_json(nome)

	#inicializa as variaveis
	variaveis = dados['glc'][0]
	simbolos = dados['glc'][1]
	regras = dados['glc'][2]
	variavel_de_partida = dados['glc'][3]

	#chamada do metodo para formar palavras
	palavras_formadas = forma_palavras(variaveis,simbolos,regras,variavel_de_partida,tamanho)
	
	#laco para impressao de todas as palavras
	for palavra in remove_lambdas(palavras_formadas,"#"):
		if len(palavra) > tamanho:
			continue

		if palavra != "":
			print(palavra)
		else:
			print("#")

#chamada do metodo glc
glc()
