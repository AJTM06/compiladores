#Como funcionaria
funcion factorial(x){
    si x=1 o x=0{
        retorna 1
    }
    sino{
        retorna (x*factorial(x-1))
    }
numero = 7
resultado = factorial(numero)
imprimir(resultado)
}