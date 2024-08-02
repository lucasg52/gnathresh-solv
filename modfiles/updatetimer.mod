NEURON {
	POINT_PROCESS deathupdate
	GLOBAL updatet
}

PARAMETER {
	updatet = 1e9
}

AFTER SOLVE{
	if (t >= updatet){
		updatet = updatet + 1e9
	}
}
