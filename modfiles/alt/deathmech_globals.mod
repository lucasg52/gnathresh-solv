NEURON {
	SUFFIX apdeath
	RANGE deatht, begin
	GLOBAL flagbegin, flagactive, vthresh
	EXTERNAL updatet_deathupdate
}

PARAMETER {
	v			(millivolt)
	vthresh = -55		(millivolt)
	propthresh = -10	(millivolt)
	flagbegin = 0		(bool)
	flagactive = 0		(bool)
}
ASSIGNED{
	deatht (ms)
	begin (flag)
}
INITIAL{
	deatht = 0
	begin = 0
}
BREAKPOINT{
	if (t >= updatet_deathupdate){
		if (begin != 0 && deatht == 0){
			recordactive()
			: activity flag is different as it is reset for each update
		}
		if (begin == 1){
			recordbegin()
			
			begin = 2
		}
	}
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
		if (v > propthresh && begin > 0){
			begin = -1
		}
	}
	
}

PROCEDURE recordactive(){
	flagactive = 1
}

PROCEDURE recordbegin(){
	flagbegin = 1
}

 
