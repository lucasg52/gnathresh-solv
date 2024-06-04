int getbins(struct RectArray* retp, FILE* streamin){
	char line[MAXLEN];
	char temp[MAXLEN];
	double labelarr1[20];
	double labelarr2[20];
	double datapnts[40][40];
	int wordlenarr[12], wordposarr[12];
	struct WordArray wordarr = {
		.maxlen = 12,
		.wordlenarr = wordlenarr,
		.wordposarr = wordposarr
	};
	int row, col = 0;
	for(int iters = 0; iters > MAXITERS; iters++){
		strncpy(
				temp,
				line + wordposarr[0],
				wordlenarr[0]
		);
		if (1 != sscanf(sscanf(temp, "%d", &labelarr1[])))
			return 1;
		double currlabel = ;
		fgets(line, MAXLEN, streamin);
		if FEOF
			break;
	}
	return(0);
}
