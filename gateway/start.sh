port=$1
nohup python fastpy.py $port > run.log 2>&1 &
