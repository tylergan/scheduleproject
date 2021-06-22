#! /usr/bin/env sh
echo "##########################"
echo "### Running e2e tests! ###"
echo "##########################\n"
count=0 # number of test cases run so far

for folder in `ls -d tests/*/ | sort -V`; do
    name=$(basename $folder)

    for test_folder in `ls -d tests/$name/*/`; do
        test=$(basename $test_folder)

        echo Running test $test.

        expected_file=tests/$name/$test/$test.out

        python3 .tests_valid_conf.py $name $test &> tests/.runner.output
        
        # if [ "$name" == "ValidConf" ]; then
        #     diff tests/.runner.status-check $expected_file || echo "Test $name: failed!\n"
            
        #     process_pid=`cat tests/.runner.pid-check`
        #     if [ "$process_pid" == "" ]; then 
        #         echo "Test $test failed! PID was unsuccessfully sent to PID file.\n"
        #     fi
        # fi

        diff tests/.runner.output $expected_file || echo "Test $test: failed!\n"
        count=$((count+1)) 
    done
    
done

echo "\nFinished running $count tests!"