#include <stdio.h>
long long doubleFactorial(int n){
    long long res = 1;
    for (int i=n; i>0; i -= 2){
        res *= i;
    }
    return res;
}
int main(){
    int n;
    printf("Nhap gia tri n: ");
    scanf("%d", &n);
    long long res = doubleFactorial(n);
    printf("%d!! = %lld\n", n, res);
    return 0;
}