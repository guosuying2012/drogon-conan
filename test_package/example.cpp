#include <iostream>
#include <drogon/drogon.h>

using namespace std;
using namespace drogon;

int main(int atgc, char* argv[]) 
{
    cout << "Drogon Version: " << getVersion() << ". GitCommit: " << getGitCommit() <<endl;
    return 0;
}
