#Como funcionaria
funcion fibonacci(x){
    si x = 0{
        retorna 0
    }
    si x = 1{
        retorna 1
    }
    sino {
        fibo = fibonacci(x-1) + fibonacci(x-2)
        retorna fibo
    }
imprimir(fibonacci(4))
}