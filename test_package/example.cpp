#include <iostream>
#include <drogon/utils/Utilities.h>

using namespace std;
using namespace drogon;

int main(int atgc, char* argv[]) 
{
    cout << "RandomString: " << utils::genRandomString(10) <<endl;
    return 0;
}
