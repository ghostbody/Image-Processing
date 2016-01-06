test:
	g++ `pkg-config --cflags opencv` stero.cpp -g -o stero `pkg-config --libs opencv` 
	./stero left.png right.png left
	./stero left.png right.png right
eval:
	g++ `pkg-config --cflags opencv` evaluate.cpp -g -o evaluate `pkg-config --libs opencv`
	./evaluate disp1.png Left.png
	./evaluate disp2.png Right.png
