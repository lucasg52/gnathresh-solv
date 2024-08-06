NEURON {
	SUFFIX apdeath
	RANGE deatht, begin
}

PARAMETER {
	v			(millivolt)
}

VERBATIM
#define DEATHMECH_VTHRESH -55.0F
ENDVERBATIM

ASSIGNED{
	deatht (ms)
	begin (flag)
}
INITIAL{
	deatht = 0
	begin = 0
}

AFTER SOLVE{
	if (begin == 0){
		if (v > DEATHMECH_VTHRESH){
			begin = t
		}
	}else{
		if (v < DEATHMECH_VTHRESH && deatht == 0){ 
			deatht = t
		}
	}
	
}



 
