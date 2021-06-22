AUTHOR: Tyler Gan
Date: 20/10/20

###############################################################################################################################################################
# IMPORTANT:                                                                                                                                                  #
# Please make sure that TEST_RUNNER.OUT and TEST_RUNSTATUS.OUT are EMPTY before running RUN_TESTS.SH. Otherwise, UNEXPECTED BEHAVIOUR may occur.              #
# These two files are located in the TESTS folder along with this README.TXT file. Other components needed for RUN_TESTS.SH are found outside of this folder. #
###############################################################################################################################################################

Please note that this tests file contains two folders:
    1. InvalidConf 
        a. Configuration files contain a bunch of errors that are NOT valid and need to be detected; this is tested here.

    2. ValidConf
        a. Configurations files contain no NOTICEABLE errors here and are then executed by RUNNER.PY. The status of each process determines whether the process ran 
           successfully or did not run successfully.

MKTESTS.SH was used to create the test folders located in InvalidConf and ValidConf to save time.

These tests are run using RUN_TESTS.SH which uses the following test programs (hybrid programs of the original programs, created for testing purposes):
    1. RUN_TEST_RUNNER.PY
    2. RUN_TEST_METHODS.PY

The modifications made to these hybrid programs are highlighted in the actual test programs itself.
