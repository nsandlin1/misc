# include <stdio.h>
# include <stdlib.h>

int FIFO(int[], int, int[], int);
int LRU(int[], int, int[], int);
int OPT(int[], int, int[], int);

int main(int argc, char *argv[]) {
	// check for correct command line args
	if (argc != 3) {
		printf("Invalid Arguments");
		exit(1);
	}
	
	// create page references string
	int seed = atoi(argv[2]);
	srand(seed);
	int page_references[100];
	for (int i=0; i<100; i++) {
		page_references[i] = rand() % 10;
	}
	//int page_references[] = {2,8,7,2,0,3,1,7,3,1,9,3,6,1,8,4,5,1,8,8,3,4,4,3,4,2,0,6,6,7,0,1,0,9,3,6,4,6,8,0,4,6,2,3,5,7,8,0,3,2,0,0,0,4,6,9,1,4,3,8,8,0,0,9,7,0,7,0,9,7,7,3,8,8,9,2,7,2,1,2,0,9,1,1,1,5,0,7,1,4,9,1,9,5,8,4,4,7,9,6};
	int page_references_len = sizeof(page_references)/sizeof(page_references[0]);

	// initialize frames array
	int num_frames = atoi(argv[1]);
	int frames[num_frames];
	for (int i=0; i<num_frames; i++) {
		frames[i] = -1;
	}

	// get page fault values
	int pf_FIFO = FIFO(frames, num_frames, page_references, page_references_len);
	// reinitialize frames array
	for (int i=0; i<num_frames; i++) {
		frames[i] = -1;
	}
	int pf_LRU = LRU(frames, num_frames, page_references, page_references_len);
	for (int i=0; i<num_frames; i++) {
		frames[i] = -1;
	}
	int pf_OPT = OPT(frames, num_frames, page_references, page_references_len);

	printf("Algorithm	#Page faults\n");
	printf("FIFO		      %i\n", pf_FIFO);
	printf("LRU		      %i\n", pf_LRU);
	printf("OPT		      %i\n", pf_OPT);
	
	return 0;
}



int FIFO(int frames[], int num_frames, int page_references[], int page_references_len) {
	int faults = 0;
	int lru = 0;

	// loop through frames
	for (int i=0; i<page_references_len; i++) {
		// is it in frame already?
		int found = 0;
		for (int j=0; j<num_frames; j++) {
			if (frames[j] == page_references[i]) {
				found = 1;
				break;
			}
		}
		if (found == 1) {
			continue;
		}

		// place in frame
		frames[lru % num_frames] = page_references[i];
		lru++;
		faults++;
	}

	return faults;
}

int LRU(int frames[], int num_frames, int page_references[], int page_references_len) {
	int faults = 0;
	int index[num_frames];
	for (int i=0; i<num_frames; i++) {
		index[i] = page_references_len;
	}

	for (int i=0; i<page_references_len; i++) {
		// is it in frame already?
		int found = 0;
		for (int j=0; j<num_frames; j++) {
			if (frames[j] == page_references[i]) {
				index[j] = i;
				found = 1;
				break;
			}
		}
		if (found == 1) {
			continue;
		}

		// place in frame
		int lru = 0;

		for (int j=0; j<num_frames; j++) {
			// if emtpy
			if (index[j] == page_references_len) {
				lru = j;
				break;
			}
			if (index[j] < index[lru]) {
				lru = j;
			}
		}

		// update index and fault count
		index[lru] = i;
		frames[lru] = page_references[i];
		faults++;
	}

	return faults;
}

int OPT(int frames[], int num_frames, int page_references[], int page_references_len) {
	int faults = 0;

	for (int i=0; i<page_references_len; i++) {
		// is it in frame already? OR is there an empty frame?
		int found = 0;
		int empty = 0;
		for (int j=0; j<num_frames; j++) {
			if (frames[j] == page_references[i]) {
				found = 1;
				break;
			}
			if (frames[j] == -1) {
				empty = j;
			}
		}
		if (found == 1) {
			continue;
		}
		if (empty != 0) {
			frames[empty] = page_references[i];
			faults++;
			continue;
		}

		// get the optimum swap
		int opt_index;
		int opt_index_dist = 0;

		for (int j=0; j<num_frames; j++) {
			int not_in_list = 0;

			for (int k=i+1; k<page_references_len; k++) {
				if (frames[j] == page_references[k]) {
					if (k > opt_index_dist) {
						opt_index = j;
						opt_index_dist = k;
					}
					break;
				}
				if (k == page_references_len-1) {
					opt_index = j;
					not_in_list = 1;
				}
			}

			if (not_in_list == 1) {
				break;
			}
		}

		frames[opt_index] = page_references[i];
		faults++;
	}

	return faults;
}
