#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ERROR 0
#define SUCCESS 1
void Log(char *msg);

int bad1(char *fileName){
    char buffer[100] = "";
    FILE *pFile;

   
    pFile = fopen(fileName, "r");
    if (pFile == NULL){
        Log("Error open file");
        
        return SUCCESS;
    }

    
    if (fgets(buffer, 100, pFile) < 0){
        Log("Error read file");
        
       return ERROR;
    }
    
    fclose(pFile);
    return SUCCESS;
}

int bad2() {
    char buffer[100] = "";
    
    if (fgets(buffer, 100, stdin) < 0){
        Log("Error read file");
        return ERROR;
    }
    
    return SUCCESS;
}

int good1(char* fileName){
    char buffer[100] = "";
    FILE *pFile;

    
    if (fileName == NULL){
        Log("Error file");
        return ERROR;
    }
    pFile = fopen(fileName, "r");

    if (pFile == NULL){
        Log("Error open file");
        return ERROR;
    }

    if (fgets(buffer, 100, pFile) == NULL){
        Log("Error read file");
        fclose(pFile);
        return ERROR;
    }
    
    fclose(pFile);
    return SUCCESS;
}

int good2(){
    char buffer[100] = "";
    if (fgets(buffer, 100, stdin) == NULL){
        Log("Error read file");
        return ERROR;
    }
    
    return SUCCESS;
}

int main(){
    char *fileName = "example.c";
    bad1(fileName);
    bad2();
    good1(fileName);
    good2();
}


