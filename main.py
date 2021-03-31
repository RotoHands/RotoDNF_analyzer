from RotoDNF import initCube
import asyncio

def main():
    # start_server = websockets.serve(initCube, "10.0.0.12", 5678)
    print("aaaaaa")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initCube())
    loop.run_forever()

if __name__ == '__main__':
    main()