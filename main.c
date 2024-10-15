
#include <stdio.h>
#include "ztimer.h"

int main(void) {
    ztimer_sleep(ZTIMER_SEC, 3);

    puts("Hello World!");

    return 0;
}