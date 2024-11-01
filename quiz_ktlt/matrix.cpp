/*
Cho các ma trận A, B, C. Viết chương trình thực hiện các công việc sau: 

Hoán vị dòng thứ i và dòng thứ k của ma trận nếu i<=n và k<=n 

Tính giá trị x1, x2,…, xn nếu xi bằng tổng các phần tử của cột thứ i của ma trận A. 

Tính các giá trị của dik (i,k=1,2,…,n) theo công thức dik = max(Aik, Bik, Cik) 
*/
#include <iostream>
#include <vector>
#include <algorithm> // Để sử dụng hàm max
using namespace std;

// Hàm hoán vị hai dòng của ma trận
void swapRows(vector<vector<int>>& matrix, int i, int k) {
    if (i < matrix.size() && k < matrix.size()) {
        swap(matrix[i], matrix[k]);
    } else {
        cout << "Chi so dong khong hop le." << endl;
    }
}

// Hàm tính tổng các phần tử của mỗi cột trong ma trận
vector<int> columnSums(const vector<vector<int>>& matrix) {
    int n = matrix.size();
    vector<int> sums(n, 0);
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            sums[j] += matrix[i][j];
        }
    }
    return sums;
}

// Hàm tính giá trị dik = max(Aik, Bik, Cik)
vector<vector<int>> calculateD(const vector<vector<int>>& A, const vector<vector<int>>& B, const vector<vector<int>>& C) {
    int n = A.size();
    vector<vector<int>> D(n, vector<int>(n, 0));
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            D[i][k] = max({A[i][k], B[i][k], C[i][k]});
        }
    }
    return D;
}

// Hàm hiển thị ma trận
void printMatrix(const vector<vector<int>>& matrix) {
    for (const auto& row : matrix) {
        for (int val : row) {
            cout << val << " ";
        }
        cout << endl;
    }
}

int main() {
    int n, i, k;
    cout << "Nhap kich thuoc ma tran n: ";
    cin >> n;

    // Khởi tạo ma trận A, B, C với kích thước n x n
    vector<vector<int>> A(n, vector<int>(n));
    vector<vector<int>> B(n, vector<int>(n));
    vector<vector<int>> C(n, vector<int>(n));

    // Nhập giá trị cho ma trận A
    cout << "Nhap cac phan tu cua ma tran A:" << endl;
    for (int row = 0; row < n; ++row) {
        for (int col = 0; col < n; ++col) {
            cin >> A[row][col];
        }
    }

    // Nhập giá trị cho ma trận B
    cout << "Nhap cac phan tu cua ma tran B:" << endl;
    for (int row = 0; row < n; ++row) {
        for (int col = 0; col < n; ++col) {
            cin >> B[row][col];
        }
    }

    // Nhập giá trị cho ma trận C
    cout << "Nhap cac phan tu cua ma tran C:" << endl;
    for (int row = 0; row < n; ++row) {
        for (int col = 0; col < n; ++col) {
            cin >> C[row][col];
        }
    }

    // Nhập chỉ số i và k để hoán vị dòng
    cout << "Nhap chi so dong i va k de hoan vi (0 <= i, k < n): ";
    cin >> i >> k;
    swapRows(A, i, k);

    // Tính tổng các phần tử của mỗi cột trong ma trận A
    vector<int> sums = columnSums(A);

    // Tính ma trận D theo công thức dik = max(Aik, Bik, Cik)
    vector<vector<int>> D = calculateD(A, B, C);

    // In kết quả
    cout << "Ma tran A sau khi hoan vi dong " << i << " va " << k << ":" << endl;
    printMatrix(A);

    cout << "Tong cac phan tu cua moi cot trong ma tran A:" << endl;
    for (int sum : sums) {
        cout << sum << " ";
    }
    cout << endl;

    cout << "Ma tran D voi dik = max(Aik, Bik, Cik):" << endl;
    printMatrix(D);

    return 0;
}