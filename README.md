# PythonOpenGLGame
Jogo OpenGL desenvolvido com Python

## Jogo
Você deve coletar as esferas de combustiveis espelhadas pelo mapa

## Camera
 * A jogo possui duas visões (primeira pessoa, sendo esta no veiculo, e terceira pessoa, sendo essa fixa, em uma perspectiva semelhante a TopDown), que podem ser alternadas pressionado a tecla "Q"
 * Pressione "F" para alterar para tela cheia

## Jogador
O jogador controla um veiculo, com os seguintes controles:
  * "W", "A", "S" e "D" movem a camera de primeira pessoa para cima, esquerda, baixo e direita, respectivamente
  * Setas direcionais esquera e direita rotacionam o veiculo
  * Espaço liga a aceleração do veiculo. Uma a aceleração é ligada o veiculo para apenas se o comando for pressionado novamente ou sair da estrada
  * A quantidade de combustivel no veiculo do jogador
  * O combustivel do veiculo é consumido enquanto se movimenta
  * Sem combustivel o veiculo não pode se locomover

## Aviões
Há 3 haviões no sobrevoando o mapa, seus comportamentos consistem em:
* Suas trajetorias de voo são curvas de Bezier, desenhadas em amarelo céu mapa
* Os aviões realizam disparos de bolas de canhão
* Os disparos podem destruir prédios e inviabilizar estradas

## Detalhes de implementação

### Mapa
* O mapa utiliza o arquivo mapa.txt para ser criado
* O arquivo se organiza em uma matriz de numeros positivos e negativos, cada numero representando um tile do mapa,sendo seus siguinificados:
    * -3, rua com célula de combustivel
    * -2, rua (espaço pilotavel)
    * -1, piso vazio (espaço não pilotavel)
    * 0, posição do jogador
    * Numeros positivos representam prédios, sendo seu valor o numero de andares

## Ruas
* As ruas possuem texturas de asfalto

# Execução do Projeto
Este projeto requere Python 3 e a biblioteca além das bibliotecas adicionais PyOpenGl e numpy.
Será necessaria a intalação de dois pacotes adicionais:

```sh
pip install PyOpenGl
pip install numpy
```

Para sistemas Windows pode ser necessária a instalação da biblioteca PyOpenGL pela  [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/), e baixar os arquivos ".whl" de PyOpengl e PyOpengl_accelerate" compativeis com seu sistema e versão Python.

```sh
pip install PyOpenGL-sua-versão.whl
pip install PyOpenGL_accelerate-sua-versão.whl
```
