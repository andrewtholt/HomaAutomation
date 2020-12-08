
BINS=http-post simple restGetAll restGet restSet

CC ?=gcc
CXX ?= g++

CXXFLAGS=-std=c++11

LIBS=-lcurl

all:	$(BINS)

http-post:	http-post.c
	$(CC) -g http-post.c -o http-post $(LIBS)

simple:	simple.c
	$(CC) -g simple.c -o simple $(LIBS)

restGetAll:	restGetAll.cpp
	$(CXX) -g restGetAll.cpp -o restGetAll $(LIBS)

restGet:	restGet.cpp
	$(CXX) -g restGet.cpp -o restGet $(LIBS)

restSet:	restSet.cpp
	$(CXX) -g restSet.cpp -o restSet $(LIBS)

haClass.o:	haClass.cpp haClass.h
	$(CXX) $(CXXFLAGS) -c -g haClass.cpp -o haClass.o #  $(LIBS)

clean:
	rm -f *.o $(BINS)
