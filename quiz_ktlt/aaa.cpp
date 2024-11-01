#include <iostream>
#include <cmath>
using namespace std;

//Ham tin i!!
int doubleFactorial (int n ){
    int res =1;
    for (int i = n; i>0; i-=2){
        res *= i;
    }
    return res;
}

int main(){
    int n;
    cout <<"Nhap n(n>1): " ;
    cin >> n;
    
    if (n<=1){
        cout << "n phai lon hon 1!"<<endl;
        return 1;
    }

    double S = 0;
    for (int i=0; i<n; i++){
        int doubleFact = doubleFactorial(i);
        S += doubleFact* pow(-1,i);
    }
    cout <<"Tong S: " <<S;
    return 0;
}

