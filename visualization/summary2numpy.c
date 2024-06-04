#define PY_SSIZE_T_CLEAN
#include <Python.h>


#define MAXITERS 1000
#define MAXLEN 512
#define FEOF (feof(streamin))


struct RectArray{
	int arrlen;
	int arrwid;
	double** seed;
};

struct WordArray{
	int len;
	int maxlen;
	int* wordposarr;
	int* wordlenarr;
};


int scanline(char* line, void* wrdarr_p, char sep){
	struct WordArray* wrdarr = (struct WordArray*)wrdarr_p; 
	int* posarr = wrdarr -> wordposarr;
	int* lenarr = wrdarr -> wordlenarr;
	int maxlen = wrdarr -> maxlen;

	char* p = line;
	for(int i = 0; i < maxlen; i++){
		
		posarr[i] = p - line;
		{
			char* pnext = strchr(p, sep);
			if (pnext == NULL){
				lenarr[i] = strlen(p) -1; 
				wrdarr -> len = i + 1;
				break;
			}
			lenarr[i] = pnext - p;
			p = pnext + 1;
		}
	}
	return 0;
}

int scanword(char* line, int* pos_p, int* len_p, char sep, int wordnum){ 
	char* pnext = line - 1;
	char* p;
	for(int i = 0; i <= wordnum; i++){
		
		p = pnext + 1;
		pnext = strchr(p, sep);
		if (pnext == NULL){
			if (i < wordnum)
				return 1;
			else{
				pnext = strchr(p, '\0');
				break;
			}
		}
	}
	*pos_p = p - line;
	*len_p = pnext - p;
	return 0;
}
int main(){
	char line[MAXLEN];
	char temp[MAXLEN];
	fgets(line, MAXLEN, stdin);
	fputs(line, stdout);
	int wordpos, wordlen;
	if (scanword
			(line, &wordpos, &wordlen, ' ', 0)
	)
		return 1;
	temp[0] = '\0';
	strncat(temp, line+wordpos, wordlen);
	int wordnum;
	if (sscanf(temp, "%d", &wordnum) != 1)
		return 2;
	if (scanword
			(line, &wordpos, &wordlen, ' ', wordnum)
	)
		return 3;
	temp[0] = '\0';
	printf("%d ; %d \n", wordpos, wordlen);
	strncat(temp, line+wordpos, wordlen);
	printf("[%s]\n",temp);


	//int wordlenarr[20];
	//int wordposarr[20];
	//struct WordArray mystruct = {
	//	.maxlen = 19, 
	//	.wordlenarr = wordlenarr,
	//	.wordposarr = wordposarr
	//};
	//printf("%d\n", scanline(line, (void*) &mystruct, ' '));
	//for(int i = 0; i < mystruct.len; i++){
	//	printf("%d\t%d\n", mystruct.wordposarr[i] ,mystruct.wordlenarr[i]);
	//}
	return 0;
}
//int find_label(double*){}

