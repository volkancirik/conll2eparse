# PREPARE DATA for parsing with word vectors
export PATH:= ../bin:${PATH} 
.PRECIOUS: %.sub.gz
# where word embeddings are, space separated, *UNKNOWN* is the tag for unknown words, file extension *.embeddings
EMB_PREFIX=../embeddings/

# your benchmark is under this folder
DPATH=../data

# name of the benchmark {conll07,conll-ptb whatever you want} where conll-formatted dataset which is under ${DPATH}
CONLL_DATA=conll-ptb-sample

# dimension of the word embeddings. for token based add dimensions for type and context vector dimensions
DIM=25

# extension of the conll formatted files
EXTENSION=dp
# run this one first
bin:
	cd ../bin ; make all

# your word-type embeddings
EMB_TYPE=cw-rcv1-25-scaled
# your word-context embeddings
EMB_CONTEXT=scode-wikipedia-25

# extract tokens from dataset
%.tok:
	find ${DPATH}/$*/ -name \*.${EXTENSION} | sort | xargs -I '{}' cat '{}' | cut -f2 | one-sentence-per-line.pl >> $@

### FASTSUBS options:
FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}

# generate substitute distributions
%.sub.gz: ../data/language_models/${LM} %.tok
	cat $*.tok | fastsubs-omp ${FS_OPTIONS} $< | gzip > $@

# embed context and type vectors
%.embedded.${EMB_TYPE}+${EMB_CONTEXT} : %.sub.gz ${EMB_PREFIX}${EMB_TYPE}.embeddings ${EMB_PREFIX}${EMB_CONTEXT}.embeddings
	zcat $< | concatSubs ${EMB_PREFIX}${EMB_TYPE}.embeddings ${EMB_PREFIX}${EMB_CONTEXT}.embeddings | tr '\t' ' ' | sed 's/ $$//' > $@

# add embedded token-vector representations to conll formattedfiles
prepare.token.%_${EMB_TYPE}+${EMB_CONTEXT}: %.embedded.${EMB_TYPE}+${EMB_CONTEXT}
	test -e $*_token_${EMB_TYPE}+${EMB_CONTEXT} || mkdir $*_token_${EMB_TYPE}+${EMB_CONTEXT}
	enrich_with_embeddings.py --token --delimiter " " --offset 1 --length ${DIM} $< ${DPATH}/$* $*_token_${EMB_TYPE}+${EMB_CONTEXT}
	rm -f $*.tok.gz $*.embedded
	touch $@
# add embedded word-type representations to conll formatted files
prepare.type.%_${EMB_TYPE}: ${EMB_PREFIX}${EMB_TYPE}.embeddings
	test -e $*_type_${EMB_TYPE} || mkdir $*_type_${EMB_TYPE}
	enrich_with_embeddings.py --delimiter " " --offset 1 --length ${DIM} $< ${DPATH}/$* $*_type_${EMB_TYPE}
	touch $@

# Example Run
# make prepare.type.conll-ptb-sample_cw-rcv1-25-scaled -n
# make prepare.token.conll-ptb-sample_cw-rcv1-25-scaled+scode-wikipedia-25 DIM=50 LM=wsj.lm.gz -n
