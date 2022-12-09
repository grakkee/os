//CS446 PA1 Part 2
//Grace Meredith
//4 March 2022

//Create a shell script that can input simple commands and function accordingly

#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <stdbool.h>

void promptUser(bool isBatch);
void printError();
int parseInput(char *input, char *splitWords[]);
char *redirectCommand(char *special, char *line, bool *isRedirect, char *tokens[], char *outputTokens[]);
char *executeCommand(char *cmd, bool *isRedirect, char* tokens[], char* outputTokens[], bool *isExits);
bool exitProgram(char *tokens[], int numTokens);
void launchProcesses(char *tokens[], int numTokens, bool *isRedirect);
void changeDirectories(char *tokens[], int numTokens);
void printHelp(char *tokens[], int numTokens);

int main(int argc, char *argv[]){
	int BUFFER = 256;
	bool isBatch = (argc == 2);
	bool* isRedirect, *isExits = 0;
	char** tokens[BUFFER], **outputTokens[BUFFER];
	char* cmd;

	if(isBatch){
		FILE* bf;
		bf = fopen(argv[1], "r");
		fgets(cmd, BUFFER, bf);
		char* output = executeCommand(cmd, isRedirect, *tokens, *outputTokens, isExits);
		fclose(bf);
		return 0;
	} else{
		/*while(!isExits || strcmp(output, 'exit') != 0){
			promptUser(isBatch);
			FILE* cf;*/
		return 0;

		}
	}
void promptUser(bool isBatch){
	if(!isBatch){
		int BUFFER = 256;
		char *name, host[BUFFER], currentDirectory[BUFFER];
		int hostName = gethostname(host, BUFFER), directory = getcwd(currentDirectory, BUFFER);
		name = getenv("USERNAME");
		printf("%s%s:%s", name, host, currentDirectory);
	}
}

void printError(){
	printf("Shell Program Error Encountered");
}

int parseInput(char *input, char splitWords[]){
	int wordInd = 0;
	//strtock gives a 2d array of tokens. you can access first token & arguments
    splitWords[0] = strtok(input, " ");
    while(splitWords[wordInd] != NULL){
    	splitWords[++wordInd] = strtok(NULL, " ");
      }

      return wordInd;
}

char *redirectCommand(char *special, char *line, bool *isRedirect, char *tokens[], char *outputTokens[]){
	int numTokens = parseInput(special, &tokens);
	int numTokens2 = parseInput(line, &outputTokens );
	if(numTokens == 0 || numTokens2 != 1 ){
		printError();
		return NULL;
	} else{
		&isRedirect = true;
		return &outputTokens;
	}
}

char *executeCommand(char *cmd, bool *isRedirect, char* tokens[], char* outputTokens[], bool *isExits){
	char *input = strdup(cmd), output = ' ';
	strcat(input, "\n");
	char* special = strchr(input, ">");
	bool *isRedirect;

	if(special != NULL){
		output = redirectCommand(&special, &input, &isRedirect, &tokens, &outputTokens);
		return output;
	} else{
		int numTokens = parseInput(&input, &tokens);
		if(numTokens == 0){
			isExits = exitProgram(&tokens, numTokens);
			return output;
		} else{
			changeDirectories(&tokens, numTokens);
			printHelp(&tokens, numTokens);
			launchProcesses(tokens, numTokens, isRedirect);
			return output;
		}
	}
}

bool exitProgram(char *tokens[], int numTokens){
	if(numTokens > 1){
		printError();
		return false;
	} else if(strcmp(tokens[0], "exit") == 0){
		return true;
	} else{
		return false;
	}
}

void launchProcesses(char *tokens[], int numTokens, bool isRedirect){
	pid_t pid;
	int status;
	for(int i = 0; i < numTokens; i++){
		pid = fork();
		if(pid == -1){
			printError();
		} else if (pid == 0){
			status = execvp(tokens[i], tokens);
			if(status == -1 && strcmp(tokens[i], "exit") != 0 && strcmp(tokens[i], "help") != 0 && strcmp(tokens[i], "cd") != 0){
				printError();
			}
			pid_t cpic = waitpid(pid);
		}
	}
}

void changeDirectories(char *tokens[], int numTokens){
	if(numTokens != 2){
		printError();
	}else if(strcmp(tokens[0], "cd") == 0){
		int cd = chdir(tokens[1]);
	}
}

void printHelp(char *tokens[], int numTokens){
	if(numTokens > 1){
		printError();
	} else if (strcmp(tokens[0], "help") == 0){
		printf("Grace's Shell Program\nThese shell commands are defined internally.\nhelp -prints this screen so you can see available shell commands.\nls -shows list of available files in directory\nclear -clears the shell\ncd -changes directories to specified path; if not given, defaults to home.\nexit -closes the program.\n[input] > [output] -pipes input file into output file.");

	}
}