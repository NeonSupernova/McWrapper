import logging
from McRapper import ServerWrapper, events


mcw = ServerWrapper("/Users/novapy/Downloads/mcrapper/serverv/minecraft_server.1.20.4.jar")


@mcw.events.on(events.SystemEvents.EXEC_START)
async def start(ctx):
    print(f"{ctx.time} SERVER HAS STARTED")
    return True


try:
    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
    logging.info("Starting server.jar...")

    mcw.start()

    logging.info("Server.jar has exited.")

except Exception as e:
    logging.warning(f"An error occurred: {str(e)}")
