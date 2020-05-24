#####################################
### Dejavu example testing script ###
#####################################

###########
# Clear out previous results
rm -rf ./results ./temp_audio
mkdir results

###########
# Utilize local testing if no DB set
if [ -z "$DATABASE_URL" ]; then
    echo "NOTE: No database found, setting local sqlite database for testing..."
    export DATABASE_URL="sqlite:///results/test.db"
fi  

###########
# Fingerprint files of extension mp3 in the ./mp3 folder
python dejavu.py -f ./mp3/ mp3

##########
# Run a test suite on the ./mp3 folder by extracting 1, 2, 3, 4, and 5 
# second clips sampled randomly from within each song 8 seconds 
# away from start or end, sampling with random seed = 42, and finally 
# store results in ./results and log to dejavu-test.log
python run_tests.py \
	--secs 5 \
	--temp ./temp_audio \
	--log-file ./results/dejavu-test.log \
	--padding 8 \
	--seed 42 \
	--results ./results \
	./mp3
