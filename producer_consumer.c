#include <stdlib.h>
#include <stdio.h>
#include <semaphore.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>

typedef struct {
int* buffer; /* Buffer array */
int n;     /* Maximum number of slots */
int front; /*  first item */
int rear;  /* last item */
pthread_mutex_t mutex; /* sempahore to protect accesses to buf */
sem_t slots; /* sempaphore to count available slots */
sem_t items; /* semaphore to count available items */
} sbuf_t;

void init(sbuf_t *sp, int n);  /* Initialize the data structure sbuf_t members...*/
void clean(sbuf_t *sp);        /* Free memory allocated for the buffer */
char produceNextLetter(int i);      /*produce the next letter, starting with 'a'*/
void *producer(void *); /* called by producer thread */
void *consumer(void *); /* called by consumer thread */

int main(int argc, char* argv[]){

    if(argc != 2){
        printf("Usage: %s n where n is the buffer size\n", argv[0]);
        exit(1);
    }
    int n = atoi(argv[1]);
    sbuf_t sb;
    init(&sb, n);

    pthread_t tprod;
    pthread_t tcons;

    pthread_create(&tprod, NULL, producer, &sb);
    pthread_create(&tcons, NULL, consumer, &sb);

    pthread_join(tprod, NULL);
    pthread_join(tcons, NULL);

    clean(&sb);
    return 0;
}

/*Initialize all the struct members here*/
void init(sbuf_t *sb, int size){
    sb->buffer = (int *) malloc(size*sizeof(int));
    sb->n = size;
    sb->rear = 0;
    sb->front = 0;
    sem_init(&sb->mutex, 0, 1);
    //pthread_mutex_init(&sb->mutex, NULL);
    sem_init(&sb->slots, 0, size);
    sem_init(&sb->items, 0, 0);
}

/*This function will produce the next char. loop back to a when you reach z.*/
char produceNextLetter(int i){
    return (char) (i%26 + 65);
}

/*This function will produce and insert the char. at the rear of the buffer */
void *producer(void *param){
    int n = 0;
    sbuf_t *sb = (sbuf_t *) param;
    
    int l = 0;
    int m = 1;
    int temp;

    int i = 0;
    while (1) {

        char nextchar = produceNextLetter(n++);
        //if (i > 10) {
        //    exit(1);
        //}
        sem_wait(&sb->slots);
        sem_wait(&sb->mutex);
        //pthread_mutex_lock(&sb->mutex);
        sb->buffer[(++sb->rear) % sb->n] = m;
        printf("producer: new char = %i\n", m);
       
        temp = l;
        l = m;
        m = m + temp;
        sem_post(&sb->mutex);
        //pthread_mutex_unlock(&sb->mutex);
        sem_post(&sb->items);
        sleep(1);
        //i++;
    }
}

/*This function will consume the item at the front of the buffer*/
void *consumer(void *param){

    int item;
    sbuf_t *sb = (sbuf_t *) param;

    //sleep(1);
    int i = 0;
    while (1) {
        //if (i > 10) {
        //    exit(1);
        //}

        sem_wait(&sb->items);
        sem_wait(&sb->mutex);
        //pthread_mutex_lock(&sb->mutex);
        item = sb->buffer[(++sb->front) % (sb->n)];
        printf("consumer: char = %i\n", item);
        sem_post(&sb->mutex);
        //pthread_mutex_unlock(&sb->mutex);
        sem_post(&sb->slots);

        sleep(2);
        //i++;
    }

}

/*Nothig more to be done here*/
void clean(sbuf_t *sb){
    free(sb->buffer);
}

