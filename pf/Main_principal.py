import puntos_resueltos_B as prB

while True:
    respuesta = input("Si desea realizar todos los calculos al mismo tiempo responda si, sino responda no:")
    if respuesta == "si":
        prB.ejecutar_todo_B()

    elif respuesta == 'no':
        prB.menu()
    else: 
        print('respuesta invalida')
    continuar = input('Desea continuar en el progranma?\n')
    if continuar == 'si':
        continue
    elif continuar =='no':
        break
    else:
        print("respuesta invalida")
        break