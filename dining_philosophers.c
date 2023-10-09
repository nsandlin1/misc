#include <stdlib.h>
#include <stdio.h>
#include <semaphore.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>

typedef struct {
        sem_t leftchop;
        sem_t rightchop;
        int philnum;
        int timeseat;
} phil;

void* philosopher(void*);

int main(int argc, char* argv[]) {
        if (argc != 3) {
                printf("Invalid arguments.");
                exit(1);
        }

        // get cl variables
        int a1 = atoi(argv[1]);
        int a2 = atoi(argv[2]);
        if (a1 < 2) {
                printf("Must have at least 2 philosophers.");
                exit(1);
        }
        
        // initialize chopsticks
        int numchops = a1-1;
        sem_t chopsticks[numchops];
        for (int i=0; i<numchops; i++) {
                sem_init(&chopsticks[i],0,1);
        }

        // initialize philosophers
        phil philosophers[a1];
        for (int i=0; i<a1; i++) {
                if (i == 0) {
                        philosophers[0].leftchop = chopsticks[numchops];
                        philosophers[0].rightchop = chopsticks[1];
                        philosophers[0].philnum = i;
                        philosophers[0].timeseat = a2;
                } else if (i == a1) {
                        philosophers[a1].leftchop = chopsticks[a1-1];
                        philosophers[a1].rightchop = chopsticks[0];
                        philosophers[a1].philnum = i;
                        philosophers[a1].timeseat = a2;
                } else {
                        philosophers[i].leftchop = chopsticks[i-1];
                        philosophers[i].rightchop = chopsticks[i+1];
                        philosophers[i].philnum = i;
                        philosophers[i].timeseat = a2;
                }
        }

        // initialize threads
        pthread_t tphil[a1]; // supports up to 30 philosophers

        for (int i=0; i<a1; i++) {
                pthread_create(&tphil[i], NULL, philosopher, &philosophers[i]);
		sleep(1);
        }

        for (int i=0; i<a1; i++) {
                pthread_join(tphil[i], NULL);
        }

        return 0;
}

void* philosopher(void* param) {
        phil* phildata = (phil*) param;

	int curr = 0;

        if (phildata->philnum % 2 == 0) {
		while(1) {
                	printf("Philosopher %i is thinking...\n", phildata->philnum);
                	sem_wait(&phildata->leftchop);
                	sem_wait(&phildata->rightchop);
                	printf("Philosopher %i is eating...\n", phildata->philnum);
                	sem_post(&phildata->rightchop);
                	sem_post(&phildata->leftchop);
			
			curr++;
			if (curr >= phildata->timeseat) {
				pthread_exit(0);
			}

			sleep(7);
		}
        } else {
		while(1) {
                	printf("Philosopher %i is thinking...\n", phildata->philnum);
                	sem_wait(&phildata->rightchop);
                	sem_wait(&phildata->leftchop);
                	printf("Philosopher %i is eating...\n", phildata->philnum);
                	sem_post(&phildata->leftchop);
                	sem_post(&phildata->rightchop);
			
			curr++;
			if (curr >= phildata->timeseat) {
				pthread_exit(0);
			}

			sleep(7);
		}
	}
}
