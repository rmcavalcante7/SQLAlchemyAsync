import asyncio


async def imprimir_numero(n, time_wait=1):
    print(f"Iniciando a contagem: {n}")
    await asyncio.sleep(time_wait)  # Simula uma operação assíncrona (espera 1 segundo)
    print(f"Contagem concluída: {n}")



async def main():
    # Chama as funções assíncronas, que serão executadas de forma assíncrona
    await imprimir_numero(1, time_wait=10)
    await imprimir_numero(2, time_wait=15)  # Aguarda a conclusão da função anterior
    await imprimir_numero(3, time_wait=20)  # Aguarda a conclusão da função anterior


async def mainTasks():
    # Cria tarefas assíncronas para imprimir os números em paralelo
    task1 = asyncio.create_task(imprimir_numero(4, time_wait=5))
    task2 = asyncio.create_task(imprimir_numero(5, time_wait=3))
    task3 = asyncio.create_task(imprimir_numero(6, time_wait=1))

    # Aguarda a conclusão de todas as tarefas
    await task1
    await task2
    await task3


async def mainGather():
    # Cria tarefas assíncronas para imprimir os números em paralelo
    await asyncio.gather(
        imprimir_numero(7, time_wait=5),
        imprimir_numero(8, time_wait=1),
        imprimir_numero(9, time_wait=3)
    )


async def run_all():
    print("Iniciando todos os mains...")
    await asyncio.gather(
        main(),
        mainTasks(),
        mainGather()
    )
    print("Todos os mains finalizados.")


if '__main__' == __name__:
    # # Executa o loop de eventos para rodar as tarefas assíncronas
    # print("1-Iniciando o loop de eventos")
    # asyncio.run(main())
    # print("1-Loop de eventos finalizado")
    #
    # # Executa o loop de eventos para rodar as tarefas assíncronas
    # print("\n\n2-Iniciando o loop de eventos")
    # asyncio.run(mainTasks())
    # print("2-Loop de eventos finalizado")
    #
    # # Executa o loop de eventos para rodar as tarefas assíncronas
    # print("\n\n3-Iniciando o loop de eventos")
    # asyncio.run(mainGather())
    # print("3-Loop de eventos finalizado")

    # Executa o loop de eventos para
    print("\n\n\n\n4-Iniciando o loop de eventos")
    asyncio.run(run_all())
    print("4-Loop de eventos finalizado")
