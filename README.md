# PythonOpenGLGame
Jogo OpenGL desenvolvido com Python

## Jogo
Você deve coletar as esferas de combustíveis espelhadas pelo mapa

## Câmera
 * A jogo possui duas visões (primeira pessoa, sendo está no veículo, e terceira pessoa, sendo essa fixa, em uma perspectiva semelhante a TopDown), que podem ser alternadas pressionado a tecla "Q"
 * Pressione "F" para alterar para tela cheia

## Jogador
O jogador controla um veículo, com os seguintes controles:
  * "W", "A", "S" e "D" movem a câmera de primeira pessoa para cima, esquerda, baixo e direita, respectivamente
  * Setas direcionais esquerda e direita rotacionam o veículo
  * Espaço liga a aceleração do veículo. Uma a aceleração é ligada o veículo para apenas se o comando for pressionado novamente ou sair da estrada
  * A quantidade de combustível no veículo do jogador
  * O combustível do veículo é consumido enquanto se movimenta
  * Sem combustível o veículo não pode se locomover

## Aviões
Há 3 aviões no sobrevoando o mapa, seus comportamentos consistem em:
* Suas trajetórias de voo são curvas de Bezier, desenhadas em amarelo céu mapa
* Os aviões realizam disparos de bolas de canhão
* Os disparos podem destruir prédios e inviabilizar estradas

## Detalhes de implementação

### Mapa
* O mapa utiliza o arquivo mapa.txt para ser criado
* O arquivo se organiza em uma matriz de números positivos e negativos, cada número representando um tile do mapa, sendo seus significados:
    * -3, rua com célula de combustível
    * -2, rua (espaço dirigível)
    * -1, piso vazio (espaço não dirigível)
    * 0, posição do jogador
    * Números positivos representam prédios, sendo seu valor o número de andares

## Ruas
* As ruas possuem texturas de asfalto

# Execução do Projeto
Este projeto requere Python 3 e a biblioteca além das bibliotecas adicionais PyOpenGl e numpy.
Será necessária a instalação de dois pacotes adicionais:

```sh
pip install PyOpenGl
pip install numpy
```

Para sistemas Windows pode ser necessária a instalação da biblioteca PyOpenGL pela  [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/), e baixar os arquivos ".whl" de PyOpengl e PyOpengl_accelerate" compatíveis com seu sistema e versão Python.

```sh
pip install PyOpenGL-sua-versão.whl
pip install PyOpenGL_accelerate-sua-versão.whl
```
