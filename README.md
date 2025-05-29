# Visualizador do Algoritmo Bresenham

Um programa simples para ver como funciona o algoritmo de Bresenham que transforma linhas matemáticas em pixels na tela.

## O que faz

Este programa mostra visualmente como o computador desenha linhas na tela usando o algoritmo de Bresenham. Quando você quer desenhar uma linha do ponto A ao ponto B, o algoritmo de Bresenham calcula quais quadradinhos (pixels) devem ser pintados para formar essa linha de forma mais eficiente que o DDA.

O programa te deixa:
- Escolher dois pontos (início e fim da linha)
- Ver quais pixels o algoritmo de Bresenham escolheu (em azul)
- Comparar com a linha matemática perfeita (em vermelho tracejado)
- Ver as coordenadas de cada quadradinho da grade
- A grade se adapta automaticamente ao tamanho das coordenadas

## Como usar

1. **Instalar Python**: Você precisa ter Python instalado no seu computador
2. **Baixar o arquivo**: Pegue o arquivo `Bresenham.py`
3. **Executar**: Abra o terminal/prompt e digite:
   ```
   python Bresenham.py
   ```
4. **Usar o programa**:
   - Digite as coordenadas do ponto inicial (X e Y)
   - Digite as coordenadas do ponto final (X e Y)
   - Clique em "Executar Algoritmo Bresenham"
   - Veja o resultado na grade

## Exemplo

Se você colocar:
- Ponto inicial: (-3, -2)
- Ponto final: (3, 2)

O programa vai mostrar todos os quadradinhos que o algoritmo escolheu para formar a linha entre esses dois pontos.

## Características especiais

- **Grade adaptável**: Se você usar coordenadas grandes (como 15, 20), a grade aumenta automaticamente
- **Barras de rolagem**: Para grades muito grandes, aparecem barras de rolagem para navegar
- **Aviso inteligente**: O programa pergunta se você quer continuar quando as coordenadas são muito grandes

## Para que serve

Este programa é útil para:
- Estudantes de computação gráfica
- Quem quer entender como o computador desenha linhas
- Professores explicando rasterização
- Curiosos sobre algoritmos gráficos
- Comparar diferenças entre algoritmos DDA e Bresenham

## Requisitos

- Python 3.6 ou mais novo
- Tkinter (já vem com o Python na maioria dos casos)

Se der erro de "tkinter não encontrado", no Linux você pode instalar com:
```
sudo apt-get install python3-tk
```

## Sobre o algoritmo

O algoritmo de Bresenham é uma versão mais eficiente do DDA para desenhar linhas. Ele funciona usando apenas números inteiros (sem decimais), o que o torna mais rápido e preciso. É um dos algoritmos mais importantes em computação gráfica.

## Diferença do DDA

- **Bresenham**: Usa apenas inteiros, mais rápido, mais preciso
- **DDA**: Usa decimais, mais simples de entender, menos eficiente

---

Programa feito para fins educacionais. Use à vontade!
