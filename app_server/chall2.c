#include <stdio.h>
#include <unistd.h>
 
void phase1(char *inp)
{
	FILE *secret = fopen("flag.txt", "rt");
	char buffer[32];
	fgets(buffer, sizeof(buffer), secret);
	printf("It's really you ? ",inp);
	fclose(secret);
}
void phase2(char *inp)
{
	int var;
	int check  = 0x04030201;
 
	char fmt[128];
	memset( fmt, 0, sizeof(fmt) );

	snprintf( fmt, sizeof(fmt), inp );
 
	if ((check != 0x04030201) && (check != 0xcafebabe))
		printf ("\nYou are on the right way !\n");
	printf( "Check=0x%x\n", check );
 
	if (check==0xcafebabe)
   	{
		printf("Yeah dude! You win!\nHere is your girl...\n");
     		system("/bin/cat flag.txt");
   	}
}
int main(int argc, char *argv[]){
	char name[32];
	char pass[128];
	printf("Please provide your name: ");
	scanf("%s",name);
	phase1(name);
	printf("And password: ");
	scanf("%s", pass);
	phase2(pass);
	return 0;
}
