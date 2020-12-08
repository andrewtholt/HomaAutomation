
CXX = g++

BINS=async_consume sync_consume async_subscribe

LIBS=-lpaho-mqtt3c -lpaho-mqttpp3 -lpaho-mqtt3a

all:	$(BINS)

async_consume:    async_consume.cpp
	$(CXX) -g async_consume.cpp -o async_consume $(LIBS)

sync_consume:    sync_consume.cpp
	$(CXX) -g sync_consume.cpp -o sync_consume $(LIBS)

async_subscribe:    async_subscribe.cpp
	$(CXX) -g async_subscribe.cpp -o async_subscribe $(LIBS)
