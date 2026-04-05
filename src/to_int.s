    .section .text
    .globl  to_int    # exportamos el símbolo para que gcc lo pueda enlazar
    .type   to_int, @function



to_int:
    # ------------------ PRÓLOGO ------------------
    # Preparamos el propio stack frame de la función
    pushq   %rbp             # Guardamos el puntero base del "caller" (main)
    movq    %rsp, %rbp       # Adoptamos el puntero base actual para nosotros

    # ------------------ MAPA DE LA PILA (Stack Frame) ------------------
    # Visto desde %rbp este es el panorama:
    # 16(%rbp) -> 9no parámetro que mandó C (a)
    #  8(%rbp) -> Dirección de retorno automático de la instrucción CALL
    #  0(%rbp) -> Valor original de %rbp (puesto por el pushq arriba)

    # ------------------ CUERPO ------------------
    # Leemos directamente de la memoria de la pila, es decir del 'stackframe', ignorando los registros
    movss       16(%rbp), %xmm0     # Ponemos el argumento 'a' en %xmm0
    cvttss2si   %xmm0, %rax         # convertir a int (32 bits)

    # ------------------ EPÍLOGO ------------------
    # Restauramos la pila para no romper el programa al volver al main
    popq    %rbp
    ret                      # Regresamos a C. Como manda la norma, el resultado ya está en %rax.

    .size   to_int, .-to_int
