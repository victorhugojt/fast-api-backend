TIMES=2
for i in $(eval echo "{1..$TIMES}")
do  
    #     users times  
    siege -c 1 -r 20 http://localhost:80/flip-coins?times=10
    siege -c 3 -r 5  http://localhost:80/items/4343434343
    siege -c 2 -r 5  http://localhost:80/basic
    siege -c 5 -r 3  http://localhost:80/goodbye
    siege -c 2 -r 10 http://localhost:80/hi
    siege -c 2 -r 10 http://localhost:80/error
    siege -c 2 -r 10 http://localhost:80/random_status
    sleep 5
done