
#include <stdlib.h>
#include <stdio.h>
 
/*
gcc -m32 -o ch13 ch13.c -fno-stack-protector
*/
 
void shell() {
   printf("Yeah dude! You win!\nHere is your flag...\n");
    system("/bin/cat flag.txt");
}
void sup() {
    printf("Turn back ! Wrong way dude !!\n");
}
void phase2()
{
  int var;
  void (*func)()=sup;
  char buf[128];
  fgets(buf,133,stdin);
  func();
}
void phase1()
{
  int var;
  int check = 0x04030201;
  char buf[40];
 
  fgets(buf,45,stdin);
  printf("\n[buf]: %s\n", buf );
  printf("[check] %p\n", check);

  if ((check != 0x04030201) && (check != 0xdeadbeef))
    printf ("\nYou are on the right way!\n");

  if (check == 0xdeadbeef)
   {
     printf("Yeah dude! You win!\nHere is your flag...\n");
     system("/bin/cat flag.txt");
   }
}
int main()
{
  phase1();
  phase2();
  return 0;
}
