# Intro

[Yahoo LDA](https://github.com/shravanmn/Yahoo_LDA) is my fav [LDA](http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) implementation at the moment. 

I've found though to understand the topics it generates it's useful to have some helper scripts, like these...

# Dependencies

These helpers are a mix of python and c++. I wrote everything in python but then rewrote the slow ones in c++. Uses [boost](http://www.boost.org/).

    sudo apt-get install libboost-all-dev
    cmake .
    make # builds straight into bin

# Input helpers

## lda_prep

The input format for YahooLDA is

    $ cat documents
    primary_id secondary_id token token token ...

To do a simple normalisation (downcase and remove all tokens with len < 3 and without at least one alpha numeric) use `lda_prep`

    $ cat documents | bin/lda_prep > documents.normalised

## chop_most_least_freq

Sometimes you'll get better results by chopping the most/least frequent terms. A simple version of this can be done with `chop_most_least_freq`

    $ bin/chop_most_least_freq --input documents --lower 0.001 --upper 0.3 > documents.chopped

This removes all tokens that don't appear in at least 0.1% of documents or appear in more than 30% of documents. (For a zipfian distribution of tokens I've
found this to give reasonable results) TODO: rewrite upper/lower based on absolute freq of tokens rather than number of documents to make it distribution agnostic)

Additionally you might have specially marked up tokens that you want to retain regardless of their frequency. If so run with `--keep`.
Eg to retain all tokens starting with `foo` you can run

    $ bin/chop_most_least_freq --input documents.normalised --lower 0.001 --upper 0.3 --keep foo > documents.chopped

( This app requires two passes over the data so doesn't accept STDIN )

# Output helpers

`learntopics` produces a few useful output files

### lda.docToTop.txt

Document to Topic mapping, one line per document.

    <primary_id> <secondary_id> (<topic_id>, <weight>) (<topic_id>, <weight>) ...

### lda.topToWor.txt

Topic to Word mapping, one line per topic.

    Topic <N>: (<token>, <weight>) (<token>, <weight>) ...

### lda.worToTop.txt

Word to Topic mapping, one line per document.

    <primary_id> <secondary_id> (<token>, <topic_id>) (<token>, <topic_id>) 

## Helpers

### topic prob mass per topic

to examine the sum of topic probabilities

    cat lda.docToTop.txt | bin/mass_per_topic.py | sort -k2 -nr

eg the following output (the first and last two lines of the output) tells us topics 58 and 17 have the most mass whereas 42 and 92 are hardly represented at all.

    58	1795.96650244
    17  1673.9486237
    ...
    42	71.94400991
    92  67.45150241






   



