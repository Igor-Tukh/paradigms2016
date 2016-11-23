#ifndef TPOOL_H
#define TPOOL_H

#include <pthread.h>
#include "../include/wsqueue.h"

typedef struct Task{
    struct list_node node;
    void (*f)(void *);
    void* arg;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    int stop;
} Task_t;

typedef struct ThreadPool{
    struct wsqueue* queue;
    pthread_t* threads;
    size_t cnt;
    int stop;
} ThreadPool_t;

void thpool_init(ThreadPool_t* pool, size_t threads_nm);
void thpool_submit(ThreadPool_t* pool, Task_t* task);
void thpool_wait(Task_t* task);
void thpool_finit(ThreadPool_t* pool);

#endif
