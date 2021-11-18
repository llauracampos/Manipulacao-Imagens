# -*- coding: utf-8 -*-
"""
Projeto 1 - Introdução ao Processamento Digital de Imagens
Autores: Laura Campos, Joison Oliveira e Wendson Carlos

"""
import numpy as np
import pandas as pd
import cv2
import copy
from tqdm import tqdm
import collections.abc
from numpy import asarray
import matplotlib.pyplot as plt
import array as ar
import timeit
import time

#############################################################################
#                          DEFINIÇÃO DAS FUNÇÕES                            #
#############################################################################

def leitura_mask(filtro):
    mask = []
    arquivo = open (filtro, 'r')
    array = [[float(num) for num in line.split(',')] for line in arquivo]

    m = array[0][0]
    n = array[1][0]
    mask = array[2:]
    
    return m, n, mask


def crie_matriz(n_linhas, n_colunas, valor):

    matriz = [] 

    for i in range(int(n_linhas)):
        linha = []
        for j in range(int(n_colunas)):
            linha += [valor]
        matriz += [linha]

    return matriz


def yiq_to_rgb(imagem_yiq, imagem_original):
    
    x, w, z = imagem_original.shape
    
    blue, green, red = cv2.split(imagem_original)
    zeros = np.zeros(blue.shape, np.uint8)
    matriz_resultante = cv2.merge((zeros,zeros,zeros))    
        
    for j in tqdm(range(int(x))):
        for k in range(int(w)): 
            y = imagem_yiq[j, k, 2]
            i = imagem_yiq[j, k, 1]
            q = imagem_yiq[j, k, 0]
            
            r = 1.00*y + 0.956*i + 0.621*q
            g = 1.00*y - 0.272*i - 0.647*q
            b = 1.00*y - 1.106*i + 1.703*q
            
            if r < 0.0:
                r = 0.0
            if g < 0.0:
                g = 0.0
            if b < 0.0:
                b = 0.0
            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b > 255:
                b = 255
    
            matriz_resultante[j, k, 2] = r
            matriz_resultante[j, k, 1] = g
            matriz_resultante[j, k, 0] = b
            
    return matriz_resultante


def correlacao_comum(m, n, img, img_corr, mascara):

    blue, green, red = cv2.split(img)
    zeros = np.zeros(blue.shape, np.uint8)
    img_corr = cv2.merge((zeros,zeros,zeros))
    
    tam1 = int(m)
    tam2 = int(n)

    metadei = (m)/2
    metadej = (n)/2
    
    canal_b = crie_matriz(tam1,tam2,0)
    canal_g = crie_matriz(tam1,tam2,0)
    canal_r = crie_matriz(tam1,tam2,0)
    
    mult = (tam1)*(tam2)
    
    for x in tqdm(range(img.shape[0])):
        for y in range(img.shape[1]):
            res_b = 0
            res_g = 0
            res_r = 0
            for i in range(int(m)):
                mi1 = int(metadei) - i
                mi2 = i - int(metadei)
                for j in range(int(n)):
                    mj1 = int(metadej) - j
                    mj2 = j - int(metadej)
                    
                    if i <= metadei:
                        if j <= metadej:
                            try:
                                canal_b[i][j] = img[x-mi1][y-mj1][0]
                                canal_g[i][j] = img[x-mi1][y-mj1][1] 
                                canal_r[i][j] = img[x-mi1][y-mj1][2]
                            except:
                                continue
                        if j > metadej:
                            try:
                                canal_b[i][j] = img[x-mi1][y+mj2][0]
                                canal_g[i][j] = img[x-mi1][y+mj2][1] 
                                canal_r[i][j] = img[x-mi1][y+mj2][2]
                            except: 
                                continue
                            
                    if i > metadei:
                        if j <= metadej:
                            try:
                                canal_b[i][j] = img[x-mi2][y-mj1][0]
                                canal_g[i][j] = img[x-mi2][y-mj1][1] 
                                canal_r[i][j] = img[x-mi2][y-mj1][2]
                            except: 
                                continue
                        if j > metadej:
                            try:
                                canal_b[i][j] = img[x-mi2][y+mj2][0]
                                canal_g[i][j] = img[x-mi2][y+mj2][1] 
                                canal_r[i][j] = img[x-mi2][y+mj2][2]
                            except: 
                                continue
                            
                            
                    res_b += canal_b[i][j]*mascara[i][j]
                    res_g += canal_g[i][j]*mascara[i][j]
                    res_r += canal_r[i][j]*mascara[i][j]
                                
                                
                    img_corr[x][y][0] = abs(int(res_b))
                    img_corr[x][y][1] = abs(int(res_g))
                    img_corr[x][y][2] = abs(int(res_r))
            
    return img_corr


def mediana(m, n, yiq, img_medi, mascara):
    
    tam1 = int(m)
    tam2 = int(n)

    metadei = (m)/2
    metadej = (n)/2
    
    mult = (tam1)*(tam2)
    metade_mult = mult/2
    
    canal_y = crie_matriz(tam1,tam2,0) 
    
    for x in tqdm(range(yiq2.shape[0])):
        linha = []
        for y in range(yiq2.shape[1]):
            res_y = 0
            mediana_y = []
    
            for i in range(int(m)):
                mi1 = int(metadei) - i
                mi2 = i - int(metadei)
                for j in range(int(n)):
                    mj1 = int(metadej) - j
                    mj2 = j - int(metadej)
                    
                    if i <= metadei:
                        if j <= metadej:
                            try:
                                canal_y[i][j] = yiq[x-mi1][y-mj1][2]
                            except:
                                continue
                        if j > metadej:
                            try:
                                canal_y[i][j] = yiq[x-mi1][y+mj2][2]
                            except: 
                                continue
                            
                    if i > metadei:
                        if j <= metadej:
                            try:
                                canal_y[i][j] = yiq[x-mi2][y-mj1][2]
                            except: 
                                continue
                        if j > metadej:
                            try:
                                canal_y[i][j] = yiq[x-mi2][y+mj2][2]
                            except: 
                                continue
                            
                         
                    mediana_y.append(canal_y[i][j])
            
           
            res_y = sorted(mediana_y)
            indice = int(metade_mult) + 1
            med_y = res_y[indice]
            img_medi[x][y][2] = med_y
            
            
    return img_medi


def correlacao_em_y(m, n, yiq, img_corr_y, mascara):
 
    tam1 = int(m)
    tam2 = int(n)

    metadei = (m)/2
    metadej = (n)/2
    
    canal_y = crie_matriz(tam1,tam2,0)
    
    for x in tqdm(range(yiq.shape[0])):
        for y in range(yiq.shape[1]):
            res_y = 0

            for i in range(int(m)):
                mi1 = int(metadei) - i
                mi2 = i - int(metadei)
                for j in range(int(n)):
                    mj1 = int(metadej) - j
                    mj2 = j - int(metadej)
                    
                    if i <= metadei:
                        if j <= metadej:
                            try:
                                canal_y[i][j] = yiq[x-mi1][y-mj1][2]
                            except:
                                continue
                        if j > metadej:
                            try:
                                canal_y[i][j] = yiq[x-mi1][y+mj2][2]
                            except: 
                                continue
                            
                    if i > metadei:
                        if j <= metadej:
                            try:
                                canal_y[i][j] = yiq[x-mi2][y-mj1][2]
                            except: 
                                continue
                        if j > metadej:
                            try:
                                canal_y[i][j] = yiq[x-mi2][y+mj2][2]
                            except: 
                                continue
                            
                         
                    res_y += canal_y[i][j]*mascara[i][j]
                               
                    img_corr_y[x][y][2] = res_y
            
    return img_corr_y


def gradiente(img, img_v, img_h):

    blue, green, red = cv2.split(img)
    zeros = np.zeros(blue.shape, np.uint8)
    gradiente = cv2.merge((zeros,zeros,zeros))

    for j in range(img.shape[0]):
        for k in range(img.shape[1]): 
            gradiente[j][k][0] = np.absolute(img_v[j][k][0] + img_h[j][k][0])
            gradiente[j][k][1] = np.absolute(img_v[j][k][1] + img_h[j][k][1])
            gradiente[j][k][2] = np.absolute(img_v[j][k][2] + img_h[j][k][2])

    return gradiente

#############################################################################
#               IMPORTAÇÃO DA IMAGEM E CONFIGURAÇÕES INICIAIS               #
#############################################################################


# Definições da Imagem

img = cv2.imread('./imagens/Woman.png')
img_corr = cv2.imread('Woman.png')
img_mediana = cv2.imread('Woman.png')

x, w, z = img.shape

blue, green, red = cv2.split(img)
zeros = np.zeros(blue.shape, np.uint8)
matrizrgb = cv2.merge((zeros,zeros,zeros))
neg = cv2.merge((zeros,zeros,zeros))
negy = cv2.merge((zeros,zeros,zeros))

yiq = []
yiq_m = []

#############################################################################
#                             Questão 1 - RGB-YIQ                           #
#############################################################################

# RGB to YIQ

for j in range(int(x)):
    linha = []
    for k in range(int(w)): 
        r = img[j, k, 2]
        g = img[j, k, 1]
        b = img[j, k, 0]
        
        y = 0.299*r + 0.587*g + 0.114*b
        i = 0.596*r - 0.274*g - 0.322*b
        q = 0.211*r - 0.523*g + 0.312*b      
        
        coluna = [q, i, y]
        linha += [coluna]
    yiq += [linha]
    

yiq_m = yiq
yiq_m1 = yiq
yiq_m2 = yiq
yiq_m3 = yiq
yiq2 = np.array(yiq)
yiq_med = np.array(yiq_m)
yiq_med1 = np.array(yiq_m1)
yiq_med2 = np.array(yiq_m2)
yiq_med3 = np.array(yiq_m3)


#cv2.imshow('RGB para YIQ', yiq2)
cv2.imwrite("rgb-to-yiq.png", yiq2)

# YIQ to RGB
        
rgb = yiq_to_rgb(yiq2, img)     
cv2.imwrite("yig-to-rgb.png", rgb)
#cv2.imshow('YIQ para RGB', rgb)


#############################################################################
#                            Questão 2 - Negativo                           #
#############################################################################

# Negativo no RGB

for j in range(x):   
    for k in range(w):
        r = 255 - img[j, k, 2]
        g = 255 - img[j, k, 1]
        b = 255 - img[j, k, 0] 
        
        neg[j, k, 2] = r
        neg[j, k, 1] = g
        neg[j, k, 0] = b

#cv2.imshow('Negativo', neg)
cv2.imwrite("negativo-rgb.png", neg)

# Negativo na banda Y

negy = yiq2

for j in range(x): 
    linha = []
    for k in range(w):
        y = 255 - yiq2[j, k, 2]       
        negy[j, k, 2] = y
     
#cv2.imshow('Negativo na banda Y', negy)
cv2.imwrite("negative_y.png", negy) 

# RGB convertido do negativo da banda Y

rgb_negy = yiq_to_rgb(negy, img)
cv2.imshow('negative_rgb', rgb_negy)
#cv2.imshow('Conversao do negativo na banda Y para RGB', rgb_negy)

'''
#############################################################################
#                            Questão 3 - Filtros                            #
#############################################################################

# Filtro Média
m_med, n_med, mask_media = leitura_mask('./filtros/media_9x9.txt')
img_media = correlacao_comum(m_med, n_med,img, img_corr, mask_media)
cv2.imwrite("filtro_media.png", img_media)

# Filtro Prewitt
m_h,n_h,mask_prewitt_h = leitura_mask('./filtros/prewitt_horizontal_3x3.txt')
m_v,n_v,mask_prewitt_v = leitura_mask('./filtros/prewitt_vertical_3x3.txt')

img_prewitt_v = correlacao_comum(m_h,n_h,img, img_corr, mask_prewitt_v)
img_prewitt_h = correlacao_comum(m_v,n_v,img_prewitt_v, img_corr, mask_prewitt_h)
img_prewitt = gradiente(img, img_prewitt_v, img_prewitt_h)

cv2.imwrite("filtro_prewitt.png", img_prewitt)

# Filtro Emboss
m_emb,n_emb,mask_emboss = leitura_mask('./filtros/emboss.txt')
img_emboss = correlacao_comum(m_emb,n_emb,img, img_corr, mask_emboss)
cv2.imwrite("filtro_emboss.png", img_emboss)

#############################################################################
#                    Questão 4 - Filtro Média na Banda Y                    #
#############################################################################

# Filtro Média na Banda Y 21x21

m_21x21, n_21x21, mask_21x21 = leitura_mask('./filtros/Filtro_21x21.txt')

t_21x21_c = time.process_time()
img_21x21 = correlacao_em_y(m_21x21, n_21x21, yiq_med1, yiq_m1, mask_21x21)
t_21x21_t = time.process_time()

tempo_21x21 = t_21x21_t - t_21x21_c
print("\n Tempo de processamento da mácara 21x21: ", tempo_21x21)

img_21_quadrado = np.array(img_21x21)
#cv2.imshow('Filtro media na Banda Y - 21x21',img_21_quadrado)
cv2.imwrite("filtro_media_Y_21x21.png", img_21_quadrado)

filtro_21x21_matriz = yiq_to_rgb(img_21_quadrado, img) 
#cv2.imshow('Filtro media na Banda Y - 21x21 - para RGB',filtro_21x21_matriz)
cv2.imwrite("filtro_media_RGB_21x21.png", filtro_21x21_matriz)

# Filtro Média na Banda Y 1x21

m_1x21, n_1x21, mask_1x21 = leitura_mask('./filtros/Filtro_1x21.txt')

t_1x21_c = time.process_time()
img_1x21 = correlacao_em_y(m_1x21, n_1x21, yiq_med2, yiq_m2, mask_1x21)
t_1x21_t = time.process_time()

tempo_1x21 = t_1x21_t - t_1x21_c
print("\n Tempo de processamento da mácara 1x21: ", tempo_1x21)

img_1_21 = np.array(img_1x21)
#cv2.imshow('Filtro media na Banda Y - 1x21',img_1_21)
cv2.imwrite("filtro_media_Y_1x21.png", img_1_21)

filtro_1x21_matriz =yiq_to_rgb(img_1_21, img) 
#cv2.imshow('Filtro media na Banda Y - 1x21 - para RGB', filtro_1x21_matriz)
cv2.imwrite("filtro_media_RGB_1x21.png", filtro_1x21_matriz)

# Filtro Média na Banda Y 21x1

m_21x1, n_21x1, mask_21x1 = leitura_mask('./filtros/Filtro_21x1.txt')     

t_21x1_c = time.process_time()
img_21x1 = correlacao_em_y(m_21x1, n_21x1, yiq_med3, yiq_m3, mask_21x1)
t_21x1_t = time.process_time()

tempo_21x1 = t_21x1_t - t_21x1_c
print("\n Tempo de processamento da mácara 21x1: ", tempo_21x1)

img_21_1 = np.array(img_21x1)
#cv2.imshow('Filtro media na Banda Y - 21x1',img_21_1)
cv2.imwrite("filtro_media_Y_21x1.png", img_21_1)

filtro_21x1_matriz =yiq_to_rgb(img_21_1, img) 
#cv2.imshow('Filtro media na Banda Y - 21x1 - para RGB', filtro_21x1_matriz)
cv2.imwrite("filtro_media_RGB_21x1.png", filtro_21x1_matriz)

#############################################################################
#                       Questão 5 - Mediana na banda Y                      #
#############################################################################

# Filtro Mediana na Banda Y

m_median, n_median, mask_median = leitura_mask('./filtros/mediana_9x9.txt')
img_mediana = mediana(m_median, n_median,yiq_med, yiq_m, mask_median)
img_med = np.array(img_mediana)
#cv2.imshow('Filtro mediana na banda Y',img_med)
cv2.imwrite("filtro_mediana_Y.png", img_med)
 
# Conversão do resultado do filtro para RGB
   
mediana_matriz =yiq_to_rgb(img_med, img) 
#cv2.imshow('Filtro mediana convertido para RGB', mediana_matriz)
cv2.imwrite("filtro_mediana_Y_RGB.png", mediana_matriz)

#############################################################################
#                            Questão 6 - CORRELAÇÃO                         #
#############################################################################

#Fazendo leitura das imagens
template = cv2.imread('./imagens/Woman_eye.png')
woman = cv2.imread('./imagens/Woman.png') 

#Determinando o tamanho do template
height, width, channels = template.shape  

#Declarando o tipo de metodo que será utilizado pelo openCV, no caso correlação normalizada
method = eval('cv2.TM_CCORR_NORMED') 

# Aplicando matchTemplate que indica onde o template aparece na imagem
res = cv2.matchTemplate(woman, template, method)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_right = max_loc
bottom_right = (top_right[0] + width, top_right[1] + height)

woman = cv2.cvtColor(woman, cv2.COLOR_BGR2GRAY)

#Plotando o gráfico
cv2.rectangle(woman,top_right, bottom_right, 255, 2)
plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(woman,cmap = 'gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle('Correlação normalizada')
plt.show()
'''