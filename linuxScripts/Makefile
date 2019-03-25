CXX = g++

CXXFLAGS = -Wall -g

all: testStreamLoader

clean:

	-rm testStreamLoader.o testStreamLoader

testStreamLoader: testStreamLoader.o

	$(CXX) $(CXXFLAGS) -o testStreamLoader testStreamLoader.o

testStreamLoader.o: testStreamLoader.cpp

	$(CXX) $(CXXFLAGS) -c testStreamLoader.cpp


