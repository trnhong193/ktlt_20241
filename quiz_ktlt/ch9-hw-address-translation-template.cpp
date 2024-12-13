/* Mô phỏng thuật toán dịch địa chỉ logic sang vật lý có sử dụng TLB (slide 32):
- Địa chỉ logic có 5 bit cho page number, 3 bit cho offset
- Địa chỉ vật lý có 13 bit cho frame number
- TLB có kích thước 4 phần tử

Chú ý: Tải file template về và chỉ được điền vào các phần TODO. Không được sửa bất kỳ gì ngoài các phần TODO. */

#include <iostream>
#include <bitset> 
/*
q: thư viện bitset dùng để làm gì?
a: bitset là một kiểu dữ liệu dùng để lưu trữ các bit, nó giúp chúng ta thao tác với các bit một cách dễ dàng hơn.
   bitset cung cấp các phép toán logic như AND, OR, XOR, NOT, dịch trái, dịch phải, ...
   bitset cũng cung cấp các phép toán so sánh, truy cập, ...
   bitset cũng cung cấp các phép toán chuyển đổi giữa bitset và các kiểu dữ liệu khác như int, string, ...
*/
#include <cstring>
/* 
question: thư viện cstring dùng để làm gì?
answer: thư viện cstring dùng để thao tác với chuỗi kí tự, bao gồm các hàm xử lý chuỗi như so sánh, sao chép, nối, tìm kiếm, ...
 */
#include <list> 
using namespace std;

// khai báo các hằng số 
const int OFFSET_BITS = 3;
const int PAGE_NUM_BITS = 5;
const int FRAME_NUM_BITS = 13  ;
const int PAGE_TABLE_SIZE = 1 << PAGE_NUM_BITS; // 2^5 = 32 
const int TLB_SIZE = 4;

// khai báo các kiểu dữ liệu
typedef bitset<PAGE_NUM_BITS> PageNumber;
typedef bitset<FRAME_NUM_BITS> FrameNumber;
typedef bitset<OFFSET_BITS> OffsetNumber;
typedef bitset<PAGE_NUM_BITS + OFFSET_BITS> LogicalAddress;
typedef bitset<FRAME_NUM_BITS + OFFSET_BITS> PhysicalAddress;


// the page table
FrameNumber PT[PAGE_TABLE_SIZE];

// the TLB
pair<PageNumber, FrameNumber> TLB[TLB_SIZE];
int lastTLBEntry = 0;


// Returns physical address in `pa` and whether the TLB is hit in `TLBhit`
// Trả về địa chỉ vật lý vào biến `pa` và có sử dụng TLB hay không trong biết `TLBhit`
void MMU_translate(LogicalAddress la, PhysicalAddress& pa, bool& TLBhit) {
    // TODO BEGIN
    // Lấy Page Number từ địa chỉ logic
    PageNumber pageNum = la.to_ulong() >> OFFSET_BITS;  
    
    // Lấy Offset từ địa chỉ logic
    // OffsetNumber offset = la & bitset<OFFSET_BITS>((1 << OFFSET_BITS) - 1);  // Sửa lỗi tại đây
	OffsetNumber offset = OffsetNumber(la.to_ulong() & ((1 << OFFSET_BITS) - 1));
    // Kiểm tra TLB trước
    for (int i = 0; i < TLB_SIZE; i++) {
        if (TLB[i].first == pageNum) {  // Nếu TLB hit
            pa = TLB[i].second.to_ulong() << OFFSET_BITS | offset.to_ulong();
            TLBhit = true;  // Đánh dấu là hit trong TLB
            return;
        }
    }

    // Nếu không có trong TLB, tìm trong Page Table
    FrameNumber frameNum = PT[pageNum.to_ulong()];

    // Cập nhật TLB với mục mới
    TLB[lastTLBEntry] = make_pair(pageNum, frameNum);
    lastTLBEntry = (lastTLBEntry + 1) % TLB_SIZE;  // Vòng qua các mục TLB

    // Tính địa chỉ vật lý
    pa = frameNum.to_ulong() << OFFSET_BITS | offset.to_ulong();
    TLBhit = false;  // Không có hit trong TLB
    // TODO END
}



int main(int argc, const char** argv) {
	list<LogicalAddress> accessList;

	if (argc <= 1 || strcmp(argv[1], "-i") != 0) {
		for (int i = 0; i < PAGE_TABLE_SIZE; i++)
			PT[i] = (i + 37) * (i + 3) + 231;

		for (int i = 0; i < PAGE_TABLE_SIZE; i++) {
			int n = ((i + 13) * (i + 7) + 891) % PAGE_TABLE_SIZE,
				m = ((i + 21) * (i + 17) + 533) % PAGE_TABLE_SIZE;
			auto t = PT[m];
			PT[m] = PT[n];
			PT[n] = t;
		}

		srand(47261);
		for (int i = 0; i < PAGE_TABLE_SIZE * 5; i++) {
			int a = (rand() % PAGE_TABLE_SIZE) << OFFSET_BITS;
			int n = rand() % 20;
			for (int j = 0; j < n; j++)
				accessList.push_back(LogicalAddress(a + rand() % (1 << OFFSET_BITS)));
		}

	} else {
		for (int i = 0; i < PAGE_TABLE_SIZE; i++) {
			int f;
			cin >> f;
			PT[i] = f;
		}

		int n;
		cin >> n;

		for (int i = 0; i < n; i++) {
			LogicalAddress la;
			cin >> la;
			accessList.push_back(la);
		}
	}

	for (int i = 0; i < TLB_SIZE; i++)
		TLB[i] = make_pair(PageNumber(i), PT[i]);

	int TLBhitcount = 0;
	for (auto la : accessList) {
		PhysicalAddress pa;
		bool TLBhit;
		MMU_translate(la, pa, TLBhit);

		if (TLBhit) TLBhitcount++;

		cout << la << " --> " << pa << " " << TLBhit << endl;
	}

	cout << "TLB hit rate: " << (TLBhitcount * 100. / accessList.size()) << "%" << endl;
	
	return 0;
}