#include <ap_int.h>


void kernel(ap_uint<3> ctrl, char a[100], char b[100], int c[100]) {
#pragma HLS PIPELIME
#pragma HLS ARRAY_PARTITION variable=a
#pragma HLS ARRAY_PARTITION variable=b
#pragma HLS ARRAY_PARTITION variable=c

    char t[100];
#pragma HLS ARRAY_PARTITION variable=t
    for (int i=0; i<100; i++) {
        t[i] = a[i];
        t[i] = (ctrl[0] && i==0) ? 0 : a[i-1];
        t[i] = (ctrl[1] && i==99) ? 0 : a[i+1];
    }

    static int sum[100];
#pragma HLS ARRAY_PARTITION variable=sum
    for (int i=0; i<100; i++) {
        if (ctrl[2]) sum[i] = 0;
        sum[i] += t[i] * b[i];
    }

    for (int i=0; i<100; i++) {
        c[i] = sum[i];
    }
}
