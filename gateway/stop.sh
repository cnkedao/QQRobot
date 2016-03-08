port=$1
ps -ef | grep fastpy | grep $port | awk '{print $2}' | xargs -i{} kill -9 {}
