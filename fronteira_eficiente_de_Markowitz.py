# -*- coding: utf-8 -*-
"""Trabalho 1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mjWxpqgE5hDmfRtRNET49lcZ4ym4-wcS
"""

# Instalando o pacote de financias e incluindo pacotes para calculos posteriores

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')

# Escolhendo 3 ações do portifólio de investimentos

acoes = ['VALE3.SA', 'HYPE3.SA', 'EQTL3.SA']

ydata = yf.download(acoes, '2015-01-01', '2019-12-31', '1d');
dados = ydata["Adj Close"]

# Definindo variáveis

dados = dados *100 / dados.iloc[0]
dados_chg = dados.pct_change()
dados_chg = dados_chg.fillna(0)
ret_acc = (dados.iloc[-1] / dados.iloc[0])-1
ret_aa = ((dados.iloc[-1]/dados.iloc[0])**(1/5))-1
vol_aa = dados_chg.std()*np.sqrt(252)

# Criando uma definição para calcular a relatividade e volatividade entre ativos

def calc_ret_vol(ativos, ativos_chg, port_pesos):
  port = ativos.dot(port_pesos)
  port_chg =port.pct_change()
  port_chg = port_chg.fillna(0)
  ret = ((port.iloc[-1]/port.iloc[0])**(1/5))-1
  vol = port_chg.std()*np.sqrt(252)
  return ret, vol

# Encontrando a menor relatividade entre 2 ativos: EQTL3 e HYPE3
points = []
min_vol_ret = [100, 0] #[vol, ret]
port_pesos = [0, 0, 0]
for w in range(0, 101, 5):
  ret, vol = calc_ret_vol(dados, dados_chg, [w/100,(1-w/100), 0])
  print(f"Aloc:{round(w/100, 2):.2f} {round(1-(w/100),2):.2f} Ret:{round(ret, 3):.3f} Vol:{round(vol, 3):.3f}")
  points.append([ret, vol])
  if vol < min_vol_ret[0]:
    min_vol_ret[0] = vol
    min_vol_ret[1] = ret
    port_pesos[0] = w/100
    port_pesos[1] = 1-w/100

# Criando o gráfico da Fronteira eficiente (2 ativos)

lp = np.array(points).T
plt.scatter(lp[[1][:]],lp[[0][:]]);
plt.ylabel("Retorno");
plt.xlabel("Volatilidade");

plt.scatter(vol_aa['EQTL3.SA'], ret_aa['EQTL3.SA'], color='red');
plt.text(vol_aa['EQTL3.SA'], ret_aa['EQTL3.SA'], 'EQTL3');

plt.scatter(vol_aa['HYPE3.SA'], ret_aa['HYPE3.SA'], color='red');
plt.text(vol_aa['HYPE3.SA'], ret_aa['HYPE3.SA'], 'HYPE3');

plt.scatter(min_vol_ret[0], min_vol_ret[1], color='green');
plt.text(min_vol_ret[0], min_vol_ret[1], 'Min. Vol.');

# Criando a variável portifólio com 2 ativos

dados['PORT1'] = dados.dot(port_pesos)
dados_chg = dados.pct_change()
dados_chg = dados_chg.fillna(0)

# Definindo o cálculo do Drawdown
ddown = pd.DataFrame()

for ativo in dados.columns:
  list = []
  for ind in range(dados.count()[0]):
    list.append((dados[ativo].iloc[ind]/dados[ativo].iloc[:ind+1].max()-1)*100)
  ddown[ativo]=list

ddown['Data']=dados.index.values
ddown.set_index(keys = 'Data', inplace = True)

# Gráfico de Drawdown para: EQTL3.SA, HYPE3.SA, PORT1 (Portifólio com 2 ativos)

ddown[['EQTL3.SA', 'HYPE3.SA', 'PORT1']].plot(figsize = (15,5));

# Rentabilidade e Volatilidade para: EQTL3.SA, HYPE3.SA, PORT1 (Portifólio com 2 ativos)

ret_aa = ((dados.iloc[-1]/dados.iloc[0])**(1/5))-1
print("Rentabilidade anual:")
print(ret_aa[['EQTL3.SA','HYPE3.SA','PORT1']])
vol_aa = dados_chg.std()*np.sqrt(252)
print("Volatilidade anual:")
print(vol_aa[['EQTL3.SA','HYPE3.SA','PORT1']])

# Encontrando a menor relatividade entre 3 ativos: EQTL3, HYPE3 e VALE3

points = []
min_vol_ret = [100, 0]
port_pesos = [0, 0, 0, 0]
for w1 in range(0, 101, 5):
  for w2 in range(0, 101-w1, 5):
    ret, vol = calc_ret_vol(dados, dados_chg, [w1/100, w2/100, (1-w1/100-w2/100), 0])
    print("Aloc:", round(w1/100, 2), round(w2/100, 2), round(1-w1/100-w2/100, 2), "Ret:", round(ret, 3), "Vol:", round(vol, 3))
    print(f"Aloc:{round(w1/100, 2):.2f} {round(w2/100, 2):.2f} {round(1-w1/100-w2/100, 2):.2f} Ret:{round(ret, 3):.3f} Vol:{round(vol, 3):.3f}")
    points.append([ret, vol])
    if vol < min_vol_ret[0]:
      min_vol_ret[0] = vol
      min_vol_ret[1] = ret
      port_pesos[0] = w1/100
      port_pesos[1] = w2/100
      port_pesos[2] = 1-w1/100-w2/100

# Criando o gráfico da Fronteira eficiente (3 ativos)

lp = np.array(points).T
plt.scatter(lp[[1][:]],lp[[0][:]]);
plt.ylabel("Retorno");
plt.xlabel("Volatilidade");

plt.scatter(vol_aa['EQTL3.SA'], ret_aa['EQTL3.SA'], color='red');
plt.text(vol_aa['EQTL3.SA'], ret_aa['EQTL3.SA'], 'EQTL3');

plt.scatter(vol_aa['HYPE3.SA'], ret_aa['HYPE3.SA'], color='red');
plt.text(vol_aa['HYPE3.SA'], ret_aa['HYPE3.SA'], 'HYPE3');

plt.scatter(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], color='red');
plt.text(vol_aa['VALE3.SA'], ret_aa['VALE3.SA'], 'VALE3');

plt.scatter(min_vol_ret[0], min_vol_ret[1], color='green');
plt.text(min_vol_ret[0], min_vol_ret[1], 'Min. Vol.');

# Criando a variável portifólio com 3 ativos

dados['PORT2'] = dados.dot(port_pesos)
dados_chg = (dados - dados.shift(1)) / dados.shift(1)
dados_chg = dados_chg.fillna(0)

# Rentabilidade e Volatilidade para: EQTL3.SA, HYPE3.SA, VALE3.SA, PORT2 (Portifólio com 3 ativos)

ret_aa = ((dados.iloc[-1]/dados.iloc[0])**(1/5))-1
print("Rentabilidade anual:")
print(ret_aa[['EQTL3.SA','HYPE3.SA','VALE3.SA','PORT2']])
vol_aa = dados_chg.std()*np.sqrt(252)
print("Volatilidade anual:")
print(vol_aa[['EQTL3.SA','HYPE3.SA','VALE3.SA','PORT2']])

#Calculo Drawdown

ddown = pd.DataFrame()

for ativo in dados.columns:
  list = []
  for ind in range(dados.count()[0]):
    list.append((dados[ativo].iloc[ind]/dados[ativo].iloc[:ind+1].max()-1)*100)
  ddown[ativo]=list

ddown['Data']=dados.index.values
ddown.set_index(keys = 'Data', inplace = True)

# Gráfico de Drawdown para: EQTL3.SA, HYPE3.SA, VALE3.SA, PORT2 (Portifólio com 3 ativos)

ddown[['EQTL3.SA','HYPE3.SA','VALE3.SA','PORT2']].plot(figsize = (15,5));