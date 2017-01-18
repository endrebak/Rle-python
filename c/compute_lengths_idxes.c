#include <stdlib.h>
#include <stdio.h>
#include "minunit.h"

int tests_run = 0;

/*
function that

1 creates new arrays for new_lengths, a_indexes, b_indexes
2 extends run lengths
3 computes the new run lengths and indexes
*/


static int * run_length(int *ls1, int ls1_length, int *ls2, int ls2_length) { // # }, int *new_lengths) {

  /* mu_assert("lengths not equal!", ls1_length == ls2_length); */

  int ax = 0;
  int bx = 0;

  int a_rem = ls1[0];
  int b_rem = ls2[0];

  int maxlen = ls1_length + ls2_length;
  int *new_lengths = (int *)malloc(sizeof(int)*(maxlen));
  int *av = (int *)malloc(sizeof(int)*(maxlen));
  int *bv = (int *)malloc(sizeof(int)*(maxlen));

  int i;
  for (i=0; i < maxlen; i++) {
    new_lengths[i] = -1;
  }

  int nlx = 0;
  while (ax < ls1_length && bx < ls2_length) {

    int nb_to_take = a_rem < b_rem ? a_rem : b_rem;
    new_lengths[nlx] = nb_to_take;

    a_rem -= nb_to_take;
    b_rem -= nb_to_take;

    av[nlx] = ax;
    bv[nlx] = bx;

    nlx += 1;

    if (a_rem == 0) {
      ax += 1;
      a_rem = ax == ls1_length ? 0 : ls1[ax];
    }
    if (b_rem == 0) {
      bx += 1;
      b_rem = bx == ls2_length ? 0 : ls2[bx];
    }

  }

  return new_lengths;
}


static char * test_runlength(){

  int *ls1 = (int *)malloc(sizeof(int)*(10));
  int *ls2 = (int *)malloc(sizeof(int)*(10));

  int i;
  for (i=0; i < 10; i++){
    ls1[i] = i % 2 == 0 ? 1 : 2;
  }

  for (i=0; i < 10; i++){
    ls2[i] = i % 2 == 0 ? 2 : 1;
  }

  int *new_lengths = run_length(ls1, 10, ls2, 10);

  for(i = 0; i < 20; i++) {
      printf("%d ", new_lengths[i]);
    }
  printf("\n");

  mu_assert("new_lengths not correct", new_lengths[0] == 1);

  return 0;

}


static char * all_tests() {
  mu_run_test(test_runlength);
  return 0;
}

int main(int argc, char **argv) {
  char *result = all_tests();
  if (result != 0) {
    printf("%s\n", result);
  }
  else {
    printf("ALL TESTS PASSED\n");
  }
  printf("Tests run: %d\n", tests_run);

  return result != 0;
}
