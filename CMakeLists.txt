PROJECT(yahoo_lda_utils)

CMAKE_MINIMUM_REQUIRED(VERSION 2.4)

SET(CMAKE_VERBOSE_MAKEFILE ON)

ADD_DEFINITIONS(-Wall -O2 -DNDEBUG -march=native -mtune=native `getconf LFS_CFLAGS`)

ADD_EXECUTABLE(bin/lda_prep
               src/lda_prep
               )

TARGET_LINK_LIBRARIES(bin/lda_prep boost_system)
