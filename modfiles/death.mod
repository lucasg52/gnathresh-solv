NEURON {
	POINT_PROCESS DeathRec
	RANGE deatht, vthresh
}
PARAMETER {
	vthresh = -55 (millivolt)
}
ASSIGNED{
	deatht (ms)
	begin (bool)
}
INITIAL{
	deatht = 0
}
AFTER SOLVE{
	if (begin == 0){
		if (v > vthresh){
			begin = 1
		}
	}else{
		if (v < vthresh && deatht == 0){ 
			deatht = t
		}
	}
}
