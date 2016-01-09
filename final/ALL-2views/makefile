all:
	echo "make ASW|SDD|NCC|eval"
	g++ `pkg-config --cflags opencv` stero.cpp -g -o stero `pkg-config --libs opencv` 

ASW:
	g++ `pkg-config --cflags opencv` stero.cpp -g -o stero `pkg-config --libs opencv` 
	./stero

SDD:
	g++ `pkg-config --cflags opencv` stero1.cpp -g -o stero `pkg-config --libs opencv`
	./stero

NCC:
	g++ `pkg-config --cflags opencv` stero2.cpp -g -o stero `pkg-config --libs opencv`
	./stero

eval:
	g++ `pkg-config --cflags opencv` evaluate.cpp -g -o evaluate `pkg-config --libs opencv`
	./evaluate
