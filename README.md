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

The input format for YahooLDA is `primary_id` `secondary_id` `token` `token` `token`

    $ cat documents
    a4c6da2cd18db81a210cd94773344234 2012-01-01T08:32:50 Your Money : Investors seek security in ...
    33350e22199526324bc12d1c7700f944 2012-01-01T08:32:51 Skilled nail tech position | Please contact Kat ...
    ...

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

# Running YahooLDA

For completeness you can run YahooLDA using `formatter` and `learntopics`

    $ formatter < documents.chopped
    $ learntopics --topics 100 --iter=100

# Output helpers

`learntopics` produces a few useful output files

### lda.docToTop.txt

Document to Topic mapping, one line per document.

    <primary_id> <secondary_id> (<topic_id>, <weight>) (<topic_id>, <weight>) ...

    a4c6da2cd18db81a210cd94773344234 2012-01-01T08:32:50    (86,0.25) (45,0.220779) (13,0.207792) (98,0.100649) ...
    33350e22199526324bc12d1c7700f944 2012-01-01T08:32:51    (39,0.705882) (36,0.117647) (48,0.0882353) ...
    ...
    
### lda.topToWor.txt

Topic to Word mapping, one line per topic.

    Topic <N>: (<token>, <weight>) (<token>, <weight>) ...

    Topic 0: (video,0.151826) (show,0.121268) (live,0.106091) (watch,0.090558)  ...
    Topic 1: (game,0.124723) (season,0.085363) (coach,0.0830232) ...
    ...

### lda.worToTop.txt

Word to Topic mapping, one line per document.

    <primary_id> <secondary_id> (<token>, <topic_id>) (<token>, <topic_id>) 

    a4c6da2cd18db81a210cd94773344234 2012-01-01T08:32:50 (money,13) (investors,45) (seek,98) ...
    33350e22199526324bc12d1c7700f944 2012-01-01T08:32:51 (skilled,39) (nail,36) (tech,39) ...
    ...

## Helpers

### topic prob mass per topic

to examine the sum of topic probabilities

    $ cat lda.docToTop.txt | bin/mass_per_topic.py | sort -k2 -nr

eg the following output (the first and last two lines of the output) tells us topics 58 and 17 have the most mass whereas 42 and 92 are hardly represented at all.

    58	1795.96650244
    17  1673.9486237
    ...
    42	71.94400991
    92  67.45150241

### top docs for a topic

to examine which documents are strongest for a particular topic see `top_docs_for_topic.py`

eg to see the top docs for topic 10 run

    $ bin/top_docs_for_topic.py 10 lda.docToTop.txt documents.chopped | sort -nr

Which outputs the probability for the topic with the document

    0.88835  77a7e6a3dfda7bdfed9151f17ce8472c 2012-01-22T08:45:00 Iwa Moto wants to make a comeback : ...
    0.885886 a7212ee57e42aec1b994002f3498ac51 2012-01-24T10:39:18 Create a Grunge & textured mixed Collage in Photoshop ...
    ...










   



