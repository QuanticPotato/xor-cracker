#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define KEY_LENGTH 600

#define openFile(var, filename) (var) = fopen((filename), "r"); \
				if((var) == NULL) \
					printf("%s : no such file ...", (filename)); 

#define closeFiles(var, numFiles) for(i = 0 ; i < (numFiles) ; i++)  \
					fclose((var)[i]); \
				  free((var));

static unsigned char *key = NULL;

int genKey(int length);

int main(int argc, char **argv)
{
	FILE **inputFiles = NULL;
	int i, j, numInputs = 0, inputProcessed = 0;
	char **inputs = NULL, *tmpBuffer = NULL;
	size_t bufferLength;
	ssize_t *inputsLength;

	srand(time(NULL));
	genKey(KEY_LENGTH);

	if(argc < 2) {
		printf("Usage : generator <input_file1> <input_file2> ...\n");
		return -1;
	}

	inputFiles = (FILE**) malloc(sizeof(FILE*) * (argc - 1));
	if(inputFiles == NULL) {
		printf("Out of memory ...\n");
		return -1;
	}

	// First, count the number of lines
	for(i = 1 ; i < argc ; i++) {
		openFile(inputFiles[i - 1], argv[i]);
		if(inputFiles[i - 1] == NULL)
			continue;
		while(getline(&tmpBuffer, &bufferLength, inputFiles[i - 1]) != -1) {
			numInputs++;
		}
	}

	inputs = (char**) malloc(sizeof(char*) * numInputs);
	if(inputs == NULL) {
		closeFiles(inputFiles, argc - 1);
		printf("Out of memory ...i\n");
		return -1;
	}
	inputsLength = (ssize_t*) malloc(sizeof(ssize_t) * numInputs);
	if(inputsLength == NULL) {
		closeFiles(inputFiles, argc - 1);
		free(inputs);
		printf("Out of memory ... \n");
		return -1;
	}

	// Then read lines
	for(i = 1 ; i < argc ; i++) {
		if(inputFiles[i - 1] == NULL)
			continue;
		fseek(inputFiles[i - 1], 0, SEEK_SET);
		while((inputProcessed < numInputs) && (inputsLength[inputProcessed] = getline(&inputs[inputProcessed], &bufferLength, inputFiles[i - 1])) != -1) {
			inputProcessed++;
		}
	}


	// And finaly apply XOR crypt ...
	// ... And display it in a python-like list
	printf("messages = [");
	for(i = 0 ; i < numInputs ; i++) {
		printf("[");
		for(j = 0 ; j < inputsLength[i] - 1 ; j++) {
			printf("%d, ", (key[j % KEY_LENGTH] ^ inputs[i][j]));
		}
		printf("%d]", (key[j % KEY_LENGTH] ^ inputs[i][j + 1]));
		if(i != numInputs - 1) printf(",\n");
	}
	printf("]\n\n");

	// Output the key too in comment
	printf("#key = [");
	for(i = 0 ; i < KEY_LENGTH - 1 ; i++) 
		printf("%d, ", key[i]);
	printf("%d]\n\n", key[KEY_LENGTH - 1]);

	// Clean up everything ..
	closeFiles(inputFiles, argc - 1);
	for(i = 0 ; i < numInputs ; i++)
		free(inputs[i]);
	free(inputs);
	free(inputsLength);
	if(key != NULL) {
		free(key);
	}

	return 0;
}

int genKey(int length)
{
	int i;

	key = (unsigned char*) malloc(length);
	if(key == NULL) {
		printf("Out of memory ... \n");
		return -1;
	}
	for(i = 0 ; i < length ; i++) {
		key[i] = rand() % 256;
	}
	return 1;
}

