# Intro

[Yahoo LDA](https://github.com/shravanmn/Yahoo_LDA) is my fav [LDA](http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) implementation at the moment but 
I've found though to understand the topics it generates it's useful to have some helper scripts. Here they are...

# Dependencies

It's a mix of python and c++. (I wrote it all in python but go bored waiting for large files to be processed) The c++ stuff requires some building...

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

    $ bin/chop_most_least_freq --input documents.normalised --lower 0.001 --upper 0.3 > documents.chopped

This removes all tokens that don't appear in at least 0.1% of documents or appear in more than 30% of documents. (For a zipfian distribution of tokens I've
found this to give reasonable results) TODO: rewrite upper/lower based on absolute freq of tokens rather than number of documents to make it distribution agnostic)

Additionally you might have specially marked up tokens that you want to retain regardless of their frequency. If so run with `--keep`.
Eg to retain all tokens starting with `foo` you can run

    $ bin/chop_most_least_freq --input documents.normalised --lower 0.001 --upper 0.3 --keep foo > documents.chopped

( This app requires two passes over the data so doesn't accept STDIN )

# Running YahooLDA

(For completeness) You run YahooLDA using `formatter` and `learntopics`

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

To examine the sum of topic probabilities use `mass_per_topic`. 
It outputs for each topic the total mass assigned to the topic from across the documents.
Eg the following shows that topics 58 and 17 have the most mass whereas 42 and 92 are hardly represented at all.

    $ cat lda.docToTop.txt | bin/mass_per_topic.py | sort -k2 -nr
    58	1795.96650244
    17  1673.9486237
    ...
    42	71.94400991
    92  67.45150241

On a large corpus you can sample to get a representative result (eg using awk to take every 1000th document)

    $ cat lda.docToTop.txt | awk 'NR%1000==0' | bin/mass_per_topic.py | sort -k2 -nr

### top topics for word

To examine which tokens are strongest for a particular topic use `top_topics_for_word.py`. 
It outputs the top probabilities along with the corresponding topic ids for specified token. 
Eg to see which topics are strongest for the token 'time' run ...

    $ bin/top_topics_for_word.py time lda.topToWor.txt 
    0.106124 58
    0.0999629 4
    ...

### top docs for a topic

To examine which documents are strongest for a particular topic use `top_docs_for_topic.py`. 
It outputs the topic probability along with the full document. 
Eg to see the top documents for topic 10 run ...

    $ cat lda.docToTop.txt | bin/top_docs_for_topic.py 10 documents.chopped  | sort -nr
    0.88835  77a7e6a3dfda7bdfed9151f17ce8472c 2012-01-22T08:45:00 Iwa Moto wants to make a comeback : ...
    0.885886 a7212ee57e42aec1b994002f3498ac51 2012-01-24T10:39:18 Create a Grunge & textured mixed Collage in Photoshop ...
    ...

As before for a very large corpus you can sample `lda.docToTop.txt` to lessen the memory used by `top_docs_for_topic`

### topic freqs 

Dump a list of topics frequencies per document (like a more complete version of lda.docToTop.txt)

    $ head -n1 lda.worToTop.txt 
    3       3       (a,413) (b,198) (c,60) (d,198) (e,290) (f,198) (g,198) (h,290)

    $ head -n1 lda.worToTop.txt | worToTop_to_topics.py 
    3   3 60   1.000000000000000
    3   3 198  4.000000000000000
    3   3 290  2.000000000000000
    3   3 413  1.000000000000000

Optionally with l2 normalisation

    $ head -n1 lda.worToTop.txt | worToTop_to_topics.py --normalise True
    3   3 60   0.213200716355610
    3   3 198  0.852802865422442
    3   3 290  0.426401432711221
    3   3 413  0.213200716355610

And with cumsum chop (ie cut back to a particular magnitude)

    $ head -n1 lda.worToTop.txt | worToTop_to_topics.py --normalise True --chop 0.9
    3   3	 198			 0.852802865422442
    3   3	 290			 0.426401432711221








   



