pqsort: ./bin/main.o ./bin/thread_pool.o ./bin/wsqueue.o ./bin/squeue.o ./bin/queue.o ./bin/linkedlist.o
	gcc ./bin/main.o ./bin/thread_pool.o ./bin/wsqueue.o ./bin/squeue.o ./bin/queue.o ./bin/linkedlist.o -lpthread -o pqsort

bin/main.o: ./src/main.c include/thread_pool.h
	mkdir -p bin
	gcc -c -g ./src/main.c -o ./bin/main.o -I include 

bin/thread_pool.o: ./src/thread_pool.c include/thread_pool.h
	mkdir -p bin
	gcc -c -g ./src/thread_pool.c -o ./bin/thread_pool.o -I include

bin/wsqueue.o: ./src/wsqueue.c include/wsqueue.h
	mkdir -p bin
	gcc -c -g ./src/wsqueue.c -o ./bin/wsqueue.o -I include
	
bin/squeue.o: ./src/squeue.c include/squeue.h
	mkdir -p bin
	gcc -c -g ./src/squeue.c -o ./bin/squeue.o -I include

bin/queue.o: ./src/queue.c include/queue.h
	mkdir -p bin
	gcc -c -g ./src/queue.c -o ./bin/queue.o -I include		

bin/linkedlist.o: ./src/linkedlist.c include/linkedlist.h
	mkdir -p bin
	gcc -c -g ./src/linkedlist.c -o ./bin/linkedlist.o -I include	

clean:
	rm -rf bin pqsort
