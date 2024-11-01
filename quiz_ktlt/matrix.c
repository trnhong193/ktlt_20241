#include <stdio.h>

// Hàm hoán vị hai dòng của ma trận
void swapRows(int matrix[][100], int n, int i, int k) {
    if (i < n && k < n) {
        for (int j = 0; j < n; j++) {
            int temp = matrix[i][j];
            matrix[i][j] = matrix[k][j];
            matrix[k][j] = temp;
        }
    } else {
        printf("Chi so dong khong hop le.\n");
    }
}

// Hàm tính tổng các phần tử của mỗi cột trong ma trận
void columnSums(int matrix[][100], int n, int sums[]) {
    for (int j = 0; j < n; j++) {
        sums[j] = 0;
        for (int i = 0; i < n; i++) {
            sums[j] += matrix[i][j];
        }
    }
}

// Hàm tính giá trị dik = max(Aik, Bik, Cik)
void calculateD(int A[][100], int B[][100], int C[][100], int D[][100], int n) {
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            int maxVal = A[i][k];
            if (B[i][k] > maxVal) maxVal = B[i][k];
            if (C[i][k] > maxVal) maxVal = C[i][k];
            D[i][k] = maxVal;
        }
    }
}

// Hàm hiển thị ma trận
void printMatrix(int matrix[][100], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int n, i, k;
    printf("Nhap kich thuoc ma tran n: ");
    scanf("%d", &n);

    int A[100][100], B[100][100], C[100][100];
    int D[100][100];
    int sums[100];

    // Nhập giá trị cho ma trận A
    printf("Nhap cac phan tu cua ma tran A:\n");
    for (int row = 0; row < n; row++) {
        for (int col = 0; col < n; col++) {
            scanf("%d", &A[row][col]);
        }
    }

    // Nhập giá trị cho ma trận B
    printf("Nhap cac phan tu cua ma tran B:\n");
    for (int row = 0; row < n; row++) {
        for (int col = 0; col < n; col++) {
            scanf("%d", &B[row][col]);
        }
    }

    // Nhập giá trị cho ma trận C
    printf("Nhap cac phan tu cua ma tran C:\n");
    for (int row = 0; row < n; row++) {
        for (int col = 0; col < n; col++) {
            scanf("%d", &C[row][col]);
        }
    }

    // Nhập chỉ số i và k để hoán vị dòng
    printf("Nhap chi so dong i va k de hoan vi (0 <= i, k < n): ");
    scanf("%d%d", &i, &k);
    swapRows(A, n, i, k);

    // Tính tổng các phần tử của mỗi cột trong ma trận A
    columnSums(A, n, sums);

    // Tính ma trận D theo công thức dik = max(Aik, Bik, Cik)
    calculateD(A, B, C, D, n);

    // In kết quả
    printf("Ma tran A sau khi hoan vi dong %d va %d:\n", i, k);
    printMatrix(A, n);

    printf("Tong cac phan tu cua moi cot trong ma tran A:\n");
    for (int j = 0; j < n; j++) {
        printf("%d ", sums[j]);
    }
    printf("\n");

    printf("Ma tran D voi dik = max(Aik, Bik, Cik):\n");
    printMatrix(D, n);

    return 0;
}
