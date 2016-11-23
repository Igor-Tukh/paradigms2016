#include <stdlib.h>
#include <stdio.h>
#include "../include/thread_pool.h"

void *consumer(void* data)
{   
    ThreadPool_t* pool = (ThreadPool_t*) data;
	struct wsqueue *queue = pool -> queue;
    
	while (!pool->stop || queue_size(&queue->squeue.queue)) {
	 	struct list_node* node;
        
		pthread_mutex_lock(&queue->squeue.mutex);
		while (!pool->stop && !queue_size(&queue->squeue.queue))
			pthread_cond_wait(&queue->cond, &queue->squeue.mutex);
		node = queue_pop(&queue->squeue.queue);
		pthread_mutex_unlock(&queue->squeue.mutex);

		if (node) {
	    	Task_t* task = (Task_t*) node;
	    	pthread_mutex_lock(&task->mutex);
			task->f(task->arg);
		    task->stop = 1;  
		    pthread_mutex_unlock(&task->mutex);
		    pthread_cond_signal(&task->cond);  
			free(node);
		}
	}

	return NULL;
}

void thpool_init(ThreadPool_t* pool, size_t threads_nm){
    pool->queue = malloc(sizeof(struct wsqueue));
    wsqueue_init(pool->queue);
	pool->threads = malloc(threads_nm * sizeof(pthread_t));
    pool->cnt = threads_nm;
    pool->stop = 0;
    
    for(size_t i = 0; i < pool->cnt; i++)
        pthread_create(&pool->threads[i], NULL, consumer, pool);
}

void thpool_submit(ThreadPool_t* pool, Task_t* task){
    wsqueue_push(pool->queue, &task->node);    
}

void thpool_wait(Task_t* task){
    pthread_mutex_lock(&task->mutex);
        
    while (!task->stop)
        pthread_cond_wait(&task->cond, &task->mutex);
    
    pthread_mutex_unlock(&task->mutex);
}

void thpool_finit(ThreadPool_t* pool){
    pool->stop = 1;
    for(size_t i = 0; i < pool->cnt; i++)
        pthread_join(pool->threads[i], NULL);
    
    free(pool->threads);
    wsqueue_finit(pool->queue);
    free(pool->queue);
    free(pool);   
}
