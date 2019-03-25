#include <iostream>
#include <cstdlib>
#include <string>
#include <unistd.h>

int main(int argc, char **argv){
    for (std::string line; std::getline(std::cin, line);){
        std::cout <<"Passed Succesfully: "<<line<<std::endl;
        usleep(500);
    }
    return 0;
}
