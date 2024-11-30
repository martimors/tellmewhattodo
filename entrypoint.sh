#!/usr/bin/env bash

fastapi run tellmewhattodo/api.py &
python -m tellmewhattodo.tasks &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?