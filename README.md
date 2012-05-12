# Intro

[Yahoo LDA](https://github.com/shravanmn/Yahoo_LDA) is my fav [LDA](http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) implementation at the moment. 

I've found though to understand the topics it generates it's useful to have some helper scripts, like these...

# Dependencies

These helpers are a mix of python and c++. I wrote everything in python but then rewrote the slow ones in c++. Uses [boost](http://www.boost.org/).

    sudo apt-get install libboost-all-dev
    cmake .
    make # builds straight into bin

# Input helpers

The input format for YahooLDA is

    $ cat documents
    primary_id secondary_id token token token ...

To do a simple normalisation (downcase and remove all tokens with len < 3 and without at least one alpha numeric) use `lda_prep`

    $ cat documents | bin/lda_prep > documents.normalised




   



