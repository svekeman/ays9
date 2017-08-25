# Debug Actor Templates

During the developement of your actor template you will probably want to use tools like ipdb to jump into the execution of the actions code and inspect the state of the services. But since AYS uses multiprocessing to improve the execution speed of the actions these tools don't work.

To force the execution of your action in process and thus allow utilisation of the debugger you can use the `--debug` flag in your AYS command. E.g.:

```python
# start writing actions code
vim actions.py
# now I want to test the new code
# call AYS update to force the new code to be inserted into the database
ays actor update --name actor_name
# execute the action in debug mode
ays action my_action -actor <actor-name> --service <service-name>
# start execution...
# ....
# ipdb breakpoint
ipdb>
```

Another useful feature of AYS is that it can auto-detect when some debugging is present in the code. If `ipdb` or `IPython` is found somewhere in the code then debug mode is enabled automatically.
