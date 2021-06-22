#! /bin/bash

count=0

for folder in `ls -d tests/*/ | sort -V`; do
        basefile=$(basename $folder)
    
        for test_folder in `ls -d tests/$basefile/*/`; do
                test=$(basename $test_folder)
                
                echo Running test $test:

                expected_out=tests/$basefile/$test/$test.out
                prog_runner_out=tests/test_runner.out
                prog_runstatus_out=tests/test_runstatus.out

                > $prog_runner_out
                > $prog_runstatus_out
                
                if [ "$basefile" == "InvalidConf" ]; then
                        #for mac, run `brew install coreutils` to use "gtimeout"
                        gtimeout 5 python3 run_test_runner.py $basefile $test 2> $prog_runner_out
                        
                        printf "======================================\nChecking RUNNER output: "
                        diff $prog_runner_out $expected_out && printf "RUNNER PASSED\n" || printf "\nRUNNER FAILED\n"
                        printf "======================================\n\n"

                else
                        expected_status=tests/$basefile/$test/$test.status
                        
                        #sending runner.py to background
                        python3 run_test_runner.py $basefile $test &> $prog_runner_out &
                        runner_PID=$!
                        
                        printf "\nRunning processes and directing output to files.\n\n"
                        #running the runstatus program three times (once in cojunction with runner.py and the other two times to obtain STDOUT)
                        END=7
                        for i in $(seq 1 $END); do
                                        python3 runstatus.py >> $prog_runstatus_out 2> /dev/null
                                        runstatus_PID=$!

                                        sleep 0.3
                        done
                        
                        #kill the runner.py process to prevent running of greater than around 2 seconds.
                        {
                        for elem in `ps -a | grep run_test_runner.py | awk '{print $1}'`; do
                                kill $elem
                        done

                        wait $runner_PID $runstatus_PID 
                        } 2> /dev/null #redirect any errors to null - not informative for testing.

                        printf "Verifying output.\n"
                        #checking output from both programs
                        printf "============================================\nChecking RUNNER output: "
                        diff $prog_runner_out $expected_out && printf "RUNNER PASSED\n" || printf "\nRUNNER FAILED\n"
                        printf "============================================\n"

                        printf "Checking RUNSTATUS output: "
                        diff $prog_runstatus_out $expected_status && printf "RUNSTATUS PASSED\n" || printf "\nRUNSTATUS FAILED\n"
                        printf "============================================\n\n"

                        > $prog_runstatus_out #reset the contents to nothing
                fi

                > $prog_runner_out

                count=$((count+1))
        done

done

echo Finished running $count tests!