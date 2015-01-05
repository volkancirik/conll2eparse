## conll2eparse
============

This repository helps you prepare your conll-formatted benchmark for dependency parsing
with embeddings. Structure is as follows.

``src/`` the scripts and source code

``bin/`` binary files

``run/`` benchmark folders will be generated here

embeddings/ word embeddings file. space separated, \*UNKNOWN\* is for unknown words. file extension is .embeddings
data/ your benchmarks will be under this folder. the structure should be like this: there should be 3 folders. 00 for train, 01 for development 02 for test. file extension should be .dp .

See ``data/`` for sample benchmark *conll-ptb-sample*, and sample word vector files for ``embeddings/``.
Go to ``run/`` .First generate the binary files.

     make bin

then generate word-type embedded conll benchmark.

     make prepare.type.conll-ptb-sample_cw-rcv1-25-scaled 

This will generate a directory for the sample benchmark wiht CW embeddings.

To generate context-dependent (token-based) benchmark you need to generate substitute distributions which requires a language model. Train a language model using [this repository](https://github.com/ai-ku/upos) and put it under data/language_models. Assuming you have a language model wsj.lm.gz under data/language models you should be able to generate context dependent word vectors for the benchmark as follows.

     make prepare.token.conll-ptb-sample_cw-rcv1-25-scaled+scode-wikipedia-25 DIM=50 LM=wsj.lm.gz

Above cw-rcv1-25-scaled is wort-type embeddings and scode-wikipedia-25 is context embeddings. Set these word vectors whatever you want using EMB_TYPE and EMB_CONTEXT flags. DIM flag is 50 since the total number of embeddings is 25+25=50. See Makefile for other flags.
