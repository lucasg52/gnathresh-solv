NEURON {
	SUFFIX apdeath
	RANGE deatht, begin, vthresh
	GLOBAL proprecorded
}
PARAMETER {
	v			(millivolt)
	proprecorded = 0	(bool)
	vthresh = -55		(millivolt)
	propthresh = -10	(millivolt)
}
ASSIGNED{
	deatht (ms)
	begin (bool)
}
INITIAL{
	deatht = 0
	begin = 0
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
		if (v > propthresh && begin != -1){
			begin = -1
			recordprop()
		}
	}
}

PROCEDURE recordprop(){
	proprecorded = 1
}
