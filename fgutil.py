#!/usr/bin/env python3

#
# Data: 28/12/2021
# Programador: Luciano Silagi
# v0.1

import os, csv, sys, time, argparse
from datetime import datetime

# Tratamento de parametros e argumentos fornecidos na linha de comnando
parser = argparse.ArgumentParser(usage = './%(prog)s -i [arq_host.csv]-r [arq_rede.csv] -g [arq_grupo] -o [arq_fgscript] -s [caractere separador CSV]',
                                description = 'Gera script para automatizar a configuração de objetos para o Firewall Fortigate',
                                epilog = '')


parser.add_argument('-i', dest = 'hostfile', required = False, default = 'hosts.csv', help = 'especifique o nome do arquivo .csv que contêm as informações para objetos de host. Se não especficiadp, assume o padrão - hosts.csv')

parser.add_argument('-r', dest = 'netfile', required = False, default = 'redes.csv', help = 'especifique o nome do arquivo .csv que contêm as informações para objetos de rede. Se não especificado, assume o padrão - redes.csv')

parser.add_argument('-g', dest = 'grpfile', required = False, default = 'grupos.csv', help = 'especifique o nome do arquivo .csv que contêm as informações para objetos de grupo. Se não especificado, assume o padrão - grupos.csv')

parser.add_argument('-o', dest = 'conffile', required = False, default = 'fgscript.txt', help = 'especifique o nome do arquivo que deve armazenar o script do Firewall Fortigate. Se não especificado, assume o padrão - fgscript.txt')

parser.add_argument('-s',dest = 'csep', required = False, default = ",", help = 'especifique o caractere utilizado como separador de campos no arquivo.csv. Se não especificado, assume o caratere padrão ,')

arg = parser.parse_args()

# Nao foi fornecido nenhum paramtro na linha de comando? Então imprime o help
#if len(sys.argv) == 1:
#    parser.print_help()
#    sys.exit(1)

# Define nome, versão e autor deste script
scNome = sys.argv[0][2:8]
scVersao = 'v0.1'
scAutor = 'Lupas'

# Guarda o valor fornecido pelos parametros na linha de comando
hostCSV = arg.hostfile
redeCSV = arg.netfile
grupoCSV = arg.grpfile
conf = arg.conffile
sepCSV = arg.csep

# Guarda o valor da data e hora atual
dateTime = datetime.now()
tStampconf = dateTime.strftime("%d/%m/%Y - %H:%M:%S")

# Abre arquvivos CSV para leitura e extração de dados
with open(hostCSV, 'r') as hfile, open(redeCSV, 'r') as rfile, open(grupoCSV, 'r') as gfile, open(conf, 'w') as cfile:
    hostDados = csv.reader(hfile, delimiter = sepCSV)
    next(hostDados, None)

    redeDados = csv.reader(rfile, delimiter = sepCSV)
    next(redeDados, None)
    
    grupoDados = csv.reader(gfile, delimiter = sepCSV)
    next(grupoDados, None)

    
    # Escreve o cabecalho no arquibo de conf, incluindo nome do script, versão, data e hora que o arquivo foi gerado e nome do autor
    cfile.write('# Arquivo gerado por {} {} em {}'.format(scNome, scVersao, tStampconf))
    cfile.write('\n# Desenvolvido por {}'.format(scAutor))


    # Salva os dados do arquivo hosts.csv em variaveis
    for campo in hostDados:
        hnome = campo[0]
        hipmasc = campo[1]
        hcor = campo[2]
        hcoment = campo[3]


        # Escreve as linhas de codigo do script referente a criação de objetos de host no arquivo conf   
        cfile.write('\n\nconfig firewall address')

        if hnome:
            cfile.write('\nedit {}'.format(hnome))
        
        if hipmasc:
            cfile.write('\nset subnet {}/32'.format(hipmasc))
        
        if hcor:
            cfile.write('\nset color {}'.format(hcor))
            
        if hcoment:
            cfile.write('\nset comment \"{}\"'.format(hcoment))
            cfile.write('\nend')
        
        else:
            cfile.write('\nset comment \"Criado por {} {}\"'.format(scNome,scVersao))
            cfile.write('\nend')


    # Salva os dados do arquivo redes.csv em variáveis:
    for campo in redeDados:
        cnome = campo[0]
        cipmasc = campo[1]
        ccor = campo[2]
        ccoment = campo[3]
        

        # Escreve as linhas de codigo do script referente a criação de objetos de rede no arquivo conf   
        cfile.write('\n\nconfig firewall address')

        if cnome:
            cfile.write('\nedit {}'.format(cnome))
        
        if cipmasc:
            cfile.write('\nset subnet {}'.format(cipmasc))
        
        if ccor:
            cfile.write('\nset color {}'.format(ccor))
            
        if ccoment:
            cfile.write('\nset comment \"{}\"'.format(ccoment))
            cfile.write('\nend')
        
        else:
            cfile.write('\nset comment \"Criado por {} {}\"'.format(scNome,scVersao))
            cfile.write('\nend')
    cfile.write('\n')
                
        
    # Salva os dados do arquivo gruoo.csv em variáveis:
    for campo in grupoDados: 
        gnome = campo[0]
        gcoment = campo[1]
        membro1 = campo[2]
        membro2 = campo[3]
        membro3 = campo[4]
        membro4 = campo[5]
        membro5 = campo[6]
        

        # Escreve as linhas de codigo do script referente a criação de objetos de grupo no arquivo conf   
        cfile.write('\nconfig firewall addgrp')

        if gnome:
            cfile.write('\nedit {}'.format(gnome))

        if gcoment: 
            cfile.write('\nset comment \"{}\"'.format(gcoment))
        
        else:
            cfile.write('\nset comment \"Criado por {} {}\"'.format(scNome,scVersao))

        if membro1:
            cfile.write('\nset member \"{}\"'.format(membro1))
        
        if membro2:
            cfile.write('\nset member \"{}\"'.format(membro2))
        
        if membro3:
            cfile.write('\nset member \"{}\"'.format(membro3))
        
        if membro4:
            cfile.write('\nset member \"{}\"'.format(membro4))
        
        if membro5:
            cfile.write('\nset member \"{}\"'.format(membro5))
        
        cfile.write('\nend')
        cfile.write('\n')
    
    cfile.write('\n')
