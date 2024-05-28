MNIST_classification_in_C: main.c images_handler.c neural_network_handler.c
	gcc main.c images_handler.c neural_network_handler.c -lm -pg  -o MNIST_classification_in_C
    ./MNIST_classification_in_C -l 1 -n 64 -e 10 -lr 0.001
    gprof MNIST_classification_in_C gmon.out > gprof_out.txt
