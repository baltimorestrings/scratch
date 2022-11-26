# Quick async demo

### code

removed all details other than the funcs for the MD, look at the .py or runnable code:
```python
async def thisblocks():
    """This function is async, so the loop can run it, but it "blocks" IE it does stuff that hogs the game loop"""
    log.debug("in func")
    time.sleep(5)
    log.debug("done!")

async def thisdoesnt():
    """This function properly awaits and uses an async sleep function"""
    log.debug("in func")
    await asyncio.sleep( 5)  # waits the 5 seconds just like thisblocks, but this time we signal the event loop with await, so it knows it can go do other stuff
    log.debug("done!")

async def justprints():
    """Literally just prints """
    log.debug("HEY")
```

So we have three async functions, one just prints HEY

The other two wait 5 seconds then print done! - but they wait different ways

thisblocks uses time.sleep, which blocks the game looop

thisdoesnt awaits asyncio.sleep, which doesn't

Now - we'll run both of them with a loop

```python
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
```
### output

Run with "1" or "2" to show both ways:

```bash
user@USER> python3 demo.py 1
/Users/afrankel02/asyncdrom/demo.py:38: DeprecationWarning: There is no current event loop
  loop = asyncio.get_event_loop()
[demo::main] Running 2  async functions: thisblocks then justprints
[demo::thisblocks] in func
[demo::thisblocks] done!
[demo::justprints] HEY

<KeyboardInterrupt>
```

Here we see the loop being blocked while thisblocks runs

Now with awaiting:
```bash
user@USER> python3 demo.py 2
[demo::main2] ---
Runninng 2 async functions: thisdoesnt then justprints
/Users/afrankel02/asyncdrom/demo.py:46: DeprecationWarning: There is no current event loop
  loop = asyncio.get_event_loop()
[demo::thisdoesnt] in func
[demo::justprints] HEY
[demo::thisdoesnt] done!

<KeyboardInterrupt>
```
Here we see that the game loop kept chugging, let our print func run

