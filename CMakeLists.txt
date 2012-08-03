PROJECT(yahoo_lda_utils)

CMAKE_MINIMUM_REQUIRED(VERSION 2.4)

SET(CMAKE_VERBOSE_MAKEFILE ON)

ADD_DEFINITIONS(-std=c++0x -Wall -O2 -DNDEBUG -march=native -mtune=native `getconf LFS_CFLAGS`)

ADD_EXECUTABLE(bin/lda_prep
               src/lda_prep
               )

ADD_EXECUTABLE(bin/chop_most_least_freq
               src/chop_most_least_freq
               )

TARGET_LINK_LIBRARIES(bin/lda_prep boost_system)

TARGET_LINK_LIBRARIES(bin/chop_most_least_freq boost_system boost_program_options)
