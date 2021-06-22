# mili_time=`date +"%H%M"`
# mili_time=`expr $mili_time + 1`

# if [[ `echo ${#mili_time}` == "3" ]]; then
#         mili_time=0$mili_time

# elif [[ `echo ${#mili_time}` == "2" ]]; then
#         mili_time=00$mili_time
# fi

# echo $mili_time

#! /bin/bash

# python3 .runner-test.py ValidConf SingleMultTime1 &> tests/test_runner.out &

# P1=$!

# END=5
# for i in $(seq 1 $END); do
#         python3 runstatus.py >> prog_runstatus_out 2> /dev/null 
#         sleep 1
# done

# wait $P1
# for elem in `ps -a | grep runner.py | awk '{print $1}'`; do
#         kill $elem
# done

# python3 .runner-test.py ValidConf SingleMultTime1 &> tests/test_runner.out &

# P1=$!

# END=5
# for i in $(seq 1 $END); do
#         python3 runstatus.py >> tests/test_runstatus.out 2> /dev/null

#         if [[ $i != 1 ]] && [[ $i != $END ]]; then
#                 echo "" >>tests/test_runstatus.out
#         fi

#         sleep 1
# done

# kill `cat ~/.runner-pid`
# {
# wait $P1
# } 2> /dev/null