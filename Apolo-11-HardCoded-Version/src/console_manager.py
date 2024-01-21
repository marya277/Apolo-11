import keyboard

def menu_inicio():
    print("Presiona 'I' para iniciar o 'Q' para salir.")
    intentos = 0

    while True:
        try:
            key_pressed = keyboard.read_event(suppress=True).name
            if key_pressed.lower() == 'i':
                print("Iniciando programa...")
                break
            elif key_pressed.lower() == 'q':
                print("Saliendo del programa.")
                exit(0)
            else:
                intentos += 1
                print("Tecla incorrecta. Intenta de nuevo.")
        except KeyboardInterrupt:
            print("\nInterrupción detectada. Saliendo del programa.")
            exit(0)

        if intentos >= 5:
            print("Demasiados intentos incorrectos. Saliendo del sistema.")
            exit(0)
