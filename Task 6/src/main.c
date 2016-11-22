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
    task->node = malloc(sizeof(struct list_node));
    task->f = f;
    task->arg = arg;
    task->stop = 0;
	pthread_mutex_init(&task->mutex, NULL);
	pthread_cond_init(&task->cond, NULL);      
}

void sorting(void* data){
    TaskSort_t* task = (TaskSort_t*) data;
    if (task->size <= 1)
        return;
        
    if (task->depth == 0){
        qsort(task->data, task->size, sizeof(int), compar);
        return;
    }
    
    int lt = 0;
    int rt = task->size - 1;
    
    int val = task->data[rand() % (rt - lt + 1) + lt];
    
    while (lt < rt){
        while (task->data[lt] < val && lt + 1 <= task->size-1) lt++;
        while (task->data[rt] > val && rt - 1 >= 0) rt--;
        if (lt < rt && task->data[lt] >= val && task->data[rt] <= val) {
            swap(&(task->data[lt++]), &(task->data[rt--]));
        }
    }
    
    task->leftTask = malloc(sizeof(Task_t));
    TaskSort_t* left = malloc(sizeof(TaskSort_t));
    taskSort_init(left, task-> pool, data, lt, task->depth-1);
    task_init(task->leftTask, sorting, left);
    thpool_submit(task->pool, task->leftTask);
    
    task->rightTask = malloc(sizeof(Task_t));
    TaskSort_t* right = malloc(sizeof(TaskSort_t));
    taskSort_init(right, task-> pool, data+rt, task->size - rt, task->depth-1);
    task_init(task->rightTask, sorting, right);
    thpool_submit(task->pool, task->rightTask);
}

void wait_for_over(Task_t* task){
    thpool_wait(task);
    Task_t* lt = ((TaskSort_t*)task->arg)->leftTask;
    Task_t* rt = ((TaskSort_t*)task->arg)->rightTask;
    
    if (lt != NULL)   
        wait_for_over(lt);
    if (rt != NULL)
        wait_for_over(rt);
    
    free(task->arg);
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
        assert(data[i] > data[i - 1]);
    
    printf("Array successfully sorted"); 
}
