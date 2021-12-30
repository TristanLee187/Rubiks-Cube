#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

int main(){
    vector<int> a;
    for (int i=0; i<5; i++){
        a.push_back(i);
    }
    cout << a[a.size()-1];
    cout << endl;
}