#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "minunit.h"

int tests_run = 0;


struct Rle {
  int *ls;
  int *a;
  int *b;
  int size;
};


static struct Rle run_length(int *ls1, int ls1_length, int *ls2, int ls2_length) {

  int ax = 0;
  int bx = 0;

  int a_rem = ls1[0];
  int b_rem = ls2[0];


  int maxlen = ls1_length > ls2_length ? ls1_length : ls2_length;
  int maxlen_x2 = 2 * maxlen;


  int *new_lengths = (int *)malloc(sizeof(int)*(maxlen_x2));
  int *av = (int *)malloc(sizeof(int)*(maxlen_x2));
  int *bv = (int *)malloc(sizeof(int)*(maxlen_x2));


  int i;
  for (i=0; i < maxlen_x2; i++) {
    new_lengths[i] = -1;
    av[i] = -1;
    bv[i] = -1;
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

  int j = maxlen_x2 - 1;
  while (new_lengths[j] == -1) {
    j--;
  };

  /* since length is end + 1 in 0-idx */
  int final_size = j + 1;

  struct Rle rle = {new_lengths, av, bv, final_size};

  return rle;

}


static char * test_runlength(){

  int size = 1e3;
  int *ls1 = (int *)malloc(sizeof(int)*(size));
  int *ls2 = (int *)malloc(sizeof(int)*(size));

  int i;
  for (i=0; i < size; i++){
    ls1[i] = i % 2 == 0 ? 1 : 2;
  }

  for (i=0; i < size; i++){
    ls2[i] = i % 2 == 0 ? 2 : 1;
  }

  clock_t begin = clock();

  struct Rle rle = run_length(ls1, size, ls2, size);

  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

  printf("Time used: %f\n", time_spent);

  printf("\n");

  mu_assert("new_lengths not correct", rle.ls[0] == 1 && rle.ls[1] == 1);
  mu_assert("rle.ls[rle.size - 1] is not correct", rle.ls[rle.size - 1] == 1);

  return 0;

}


static char * test_runlength2(){

  int SIZE=4;
  static int SOURCE[4] = { 1, 2, 3, 4 };
  int *ls1= malloc(sizeof(int)*SIZE);
  memcpy(ls1, SOURCE, sizeof(int) * SIZE);


  static int SOURCE2[4] = { 4, 3, 2, 1};
  int *ls2= malloc(sizeof(int)*SIZE);
  memcpy(ls2, SOURCE2, sizeof(int) * SIZE);


  clock_t begin = clock();

  struct Rle rle = run_length(ls1, 4, ls2, 4);

  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

  printf("Time used: %f\n", time_spent);

  printf("\n");

  int i;
  for (i=0; i<rle.size;i++) {
    printf("l %i\n", rle.ls[i]);
    printf("a %i\n", rle.a[i]);
    printf("b %i\n\n", rle.b[i]);
  };

  mu_assert("rle.ls not correct", rle.ls[0] == 1 && rle.ls[1] == 2);
  mu_assert("rle.ls[rle.size - 1] is not correct", rle.ls[rle.size - 1] == 1);


  return 0;

}


static char * test_runlength3(){

  int SIZE=1;
  static int SOURCE[1] = { 1 };
  int *ls1= malloc(sizeof(int)*SIZE);
  memcpy(ls1, SOURCE, sizeof(int) * SIZE);


  static int SOURCE2[1] = { 1 };
  int *ls2= malloc(sizeof(int)*SIZE);
  memcpy(ls2, SOURCE2, sizeof(int) * SIZE);


  clock_t begin = clock();

  struct Rle rle = run_length(ls1, 1, ls2, 1);

  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

  printf("Time used: %f\n", time_spent);

  printf("\n");

  int i;
  for (i=0; i<rle.size;i++) {
    printf("l %i\n", rle.ls[i]);
    printf("a %i\n", rle.a[i]);
    printf("b %i\n", rle.b[i]);
  };

  mu_assert("rle.ls not correct", rle.ls[0] == 1);
  mu_assert("rle.ls[rle.size - 1] is not correct", rle.ls[rle.size - 1] == 1);


  return 0;

}


static char * test_runlength4(){

  static int SOURCE[2] = { 1, 5};
  int *ls1= malloc(sizeof(int)*2);
  memcpy(ls1, SOURCE, sizeof(int) * 2);


  static int SOURCE2[3] = { 1, 2, 3 };
  int *ls2= malloc(sizeof(int)*3);
  memcpy(ls2, SOURCE2, sizeof(int) * 3);


  clock_t begin = clock();

  struct Rle rle = run_length(ls1, 2, ls2, 3);

  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

  printf("Time used: %f\n", time_spent);

  printf("\n");

  int i;
  for (i=0; i<rle.size;i++) {
    printf("l %i\n", rle.ls[i]);
    printf("a %i\n", rle.a[i]);
    printf("b %i\n", rle.b[i]);
  };

  mu_assert("rle.ls not correct", rle.ls[0] == 1);
  mu_assert("rle.ls[rle.size - 1] is not correct", rle.ls[rle.size - 1] == 3);

  return 0;

}



static char * test_runlength5(){

  static int SOURCE[2] = { 1, 1};
  int *ls1= malloc(sizeof(int)*2);
  memcpy(ls1, SOURCE, sizeof(int) * 2);


  static int SOURCE2[3] = { 1, 2, 3 };
  int *ls2= malloc(sizeof(int)*3);
  memcpy(ls2, SOURCE2, sizeof(int) * 3);


  clock_t begin = clock();

  struct Rle rle = run_length(ls1, 2, ls2, 3);

  clock_t end = clock();
  double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

  printf("Time used: %f\n", time_spent);

  printf("\n");

  int i;
  for (i=0; i<rle.size;i++) {
    printf("l %i\n", rle.ls[i]);
    printf("a %i\n", rle.a[i]);
    printf("b %i\n", rle.b[i]);
  };

  mu_assert("rle.ls not correct", rle.ls[0] == 1);
  mu_assert("rle.ls[rle.size - 1] is not correct", rle.ls[rle.size - 1] == 3);

  return 0;

}


static char * all_tests() {
  mu_run_test(test_runlength);
  mu_run_test(test_runlength2);
  mu_run_test(test_runlength3);
  mu_run_test(test_runlength4);
  mu_run_test(test_runlength5);
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
