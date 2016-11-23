#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include "../include/thread_pool.h"

typedef struct TaskSort{
    int* data;
    int size;
    int depth;
    ThreadPool_t* pool;
    Task_t* leftTask;
    Task_t* rightTask;
} TaskSort_t;

void swap(int* a, int* b){
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int compar(const void* a, const void* b){
    return *((int*)a) - *((int*)b);
}

void taskSort_init(TaskSort_t* task, ThreadPool_t* pool, int* data, size_t len, size_t depth){
    task->data = data;
    task->size = len;
    task->depth = depth;
    task->leftTask = NULL;
    task->rightTask = NULL;
    task->pool = pool;
}

void task_init(Task_t* task, void (*f)(void *), void* arg){
    task->f = f;
    task->arg = arg;
    task->stop = 0;
	pthread_mutex_init(&task->mutex, NULL);
	pthread_cond_init(&task->cond, NULL);      
}

void sorting(void* data){
    //printf("Q\n");
    //fflush(stdout);
    TaskSort_t* task = (TaskSort_t*) data;
    if (task->size <= 1){
        //printf("B\n");
        //fflush(stdout);
        return;
    }
    if (task->depth == 0){
        qsort(task->data, task->size, sizeof(int), compar);
        //printf("A\n");
        //fflush(stdout);
        return;
    }
    
    int lt = 0;
    int rt = task->size - 1;
    
    int val = task->data[0];
 
 
    /*
    printf("%d\n", val);
    
    
    for(size_t i = 0; i < task->size; i++)
        printf("%d ", task->data[i]);
    printf("\n");
    */
    while (lt < rt){
        while (task->data[lt] < val) lt++;
        while (task->data[rt] > val) rt--;
        if (lt <= rt)
            swap(&(task->data[lt++]), &(task->data[rt--]));
    }
    
    /*
    for(size_t i = 0; i < rt + 1; i++)
        printf("%d ", task->data[i]);
    printf("\n");
    
    for(size_t i = lt; i < task->size - lt; i++)
        printf("%d ", task->data[i]);
    printf("\n");
    
    fflush(stdout);
    */
    //printf("C\n");
    Task_t* ltask = malloc(sizeof(Task_t));
    TaskSort_t* left = malloc(sizeof(TaskSort_t));
    taskSort_init(left, task->pool, data, rt + 1, task->depth-1);
    task_init(ltask, sorting, left);
    task->leftTask = ltask;
    thpool_submit(task->pool, ltask);
    
    Task_t* rtask = malloc(sizeof(Task_t));
    TaskSort_t* right = malloc(sizeof(TaskSort_t));
    taskSort_init(right, task->pool, data + lt, task->size - lt, task->depth-1);
    task_init(rtask, sorting, right);
    task->rightTask = rtask;
    thpool_submit(task->pool, rtask);
}

void wait_for_over(Task_t* task){
    if (task == NULL)
        return;
 
    printf("%d\n", ((TaskSort_t*)task->arg)->size);
    thpool_wait(task);
    Task_t* lt = ((TaskSort_t*)task->arg)->leftTask;
    Task_t* rt = ((TaskSort_t*)task->arg)->rightTask;
    
    printf("To lt\n");
    //printf("%d\n", ((TaskSort_t*)lt->arg)->size);
    wait_for_over(lt);
    printf("To rt\n");
    //printf("%d\n", ((TaskSort_t*)rt->arg)->size);
    wait_for_over(rt);
    
    free(task->arg);
    pthread_mutex_destroy(&task->mutex);
    pthread_cond_destroy(&task->cond);
    free(task);
}

int main(int argc, char* argv[]){
    size_t num = atoi(argv[1]);
    size_t len = atoi(argv[2]);
    size_t depth = atoi(argv[3]);
    
    int* data = malloc(len * sizeof(int));
    srand(42);
    for(int i = 0; i < len; i++)
        data[i] = rand();
    
    ThreadPool_t* pool = malloc(sizeof(ThreadPool_t));
    thpool_init(pool, num);
    
    TaskSort_t* global = malloc(sizeof(TaskSort_t));
    taskSort_init(global, pool, data, len, depth);
    Task_t* first = malloc(sizeof(Task_t));
    task_init(first, sorting, global);
    thpool_submit(pool, first);
    
    wait_for_over(first);
    
    thpool_finit(pool);
    
    for(int i = 1; i < len; i++)
        assert(data[i] >= data[i - 1]);
    free(data);
    
    printf("Successfully sorted"); 
}
