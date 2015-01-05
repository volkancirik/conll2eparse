FASTSUBS_GIT_REPO=https://github.com/ai-ku/fastsubs.git

fastsubs: check

	test -e ../src/fastsubs || (cd ../src/ ; git clone ${FASTSUBS_GIT_REPO}) 
	cd ../src/fastsubs; make
	test -e $@ || ln -s ../src/fastsubs/fastsubs .
	test -e fastsubs-omp || ln -s ../src/fastsubs/fastsubs-omp .

perl: check
	test -e `ls *.pl`  || ls *.pl | xargs -I '{}' unlink '{}'
	ln -s ../src/scripts/*.pl .

python: check
	test -e `ls *.py` || ls *.py | xargs -I '{}' unlink '{}'
	ln -s ../src/scripts/*.py .
concatSubs: check
	test -e $@ || (cd ../src/ ; g++ -O3 -o $@ $@.cpp -lm)
	ln -s ../src/$@ .
check:
	true
all : perl python concatSubs

clean:
	-rm concatSubs *.pl *.py fastsubs* 

