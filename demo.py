import asyncio
import time
from logging import *
from sys import stdout, argv

# set up logging so it'll show what function messages coming from
log = getLogger("demo")
log.addHandler(StreamHandler(stdout))
log.setLevel(DEBUG)
log.handlers[0].setFormatter(
        Formatter("[%(module)s::%(funcName)s] %(message)s")
)


async def thisblocks():
    """This function is async, so the loop can run it, but it "blocks" IE it does stuff that hogs the game loop"""
    log.debug("in func")
    time.sleep(5)
    log.debug("done!")


async def thisdoesnt():
    """This function properly awaits and uses an async sleep function"""
    log.debug("in func")
    await asyncio.sleep( 5)
    # waits the 5 seconds just like thisblocks, but this time we signal the event loop with await, so it knows it can go do other stuff
    log.debug("done!")


async def justprints():
    """Literally just prints """
    log.debug("HEY")


def main():
    """ Note how the second run does'nt block, so HEY can get printed while we wait for the function to finish """
    loop = asyncio.get_event_loop()
    log.debug("Running 2  async functions: thisblocks then justprints")
    loop.create_task(thisblocks())
    loop.create_task(justprints())
    loop.run_forever()

def main2():
    log.debug("---\nRunninng 2 async functions: thisdoesnt then justprints")
    loop = asyncio.get_event_loop()
    loop.create_task(thisdoesnt())
    loop.create_task(justprints())
    loop.run_forever()

if argv[1] == "1":
    main()
elif argv[1] == "2":
    main2()
else:
    main()
