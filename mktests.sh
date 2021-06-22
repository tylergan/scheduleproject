#! /bin/bash

while true; do
        echo "Which test folder (ValidConf or InvalidConf) would you like to input your tests in: "
        read foldername 

        if [[ $foldername != "ValidConf" ]] && [[ $foldername != "InvalidConf" ]]; then
                echo Goodbye!
                break
        fi
        
        printf "\nWhat is the name of the test folder you would like to create?\n"

        while true; do
                read testfolder

                if [[ "$testfolder" == "" ]]; then
                        break

                else    
                        clear

                        folder=tests/$foldername/$testfolder
                        mkdir $folder

                        path=$folder/$testfolder

                        touch $testfolder.conf $testfolder.txt $testfolder.out
                        mv $testfolder.conf $path.conf && mv $testfolder.txt $path.txt && mv $testfolder.out $path.out

                        if [[ $foldername == "ValidConf" ]]; then
                                        touch $testfolder.status
                                        mv $testfolder.status $path.status
                        fi

                        printf "\nSuccessfully created test $testfolder in $foldername\n\n"

                fi
        done

done
