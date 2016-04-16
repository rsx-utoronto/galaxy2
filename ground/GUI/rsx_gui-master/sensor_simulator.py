import random


def gas_sensor():
	n = random.random()

	if n <= 0.1:
		return random.randint(0,400)
	elif n >= 0.9:
		return random.randint(800,1023)
	elif n <= 0.4:
		return random.randint(400,500)
	elif n >= 0.6:
		return random.randint(600,800)
	else:
		return random.randint(500,600)


def moisture_sensor():
    n = random.random()

    if n <= 0.05:
        return random.randint(0,500)
    elif n >= 0.95:
        return random.randint(600,1023)
    else:
        return random.randint(500,600)


def gps_sensor():
    n1 = random.random()
    n2 = random.random()

    n1 *= 0.002
    n2 *= 0.002

    # return 38.406607 + n1, -110.791006 + n2
    return 38.406607, -110.791006


def compass_sensor():
    n = random.random()

    return 360*n
    # return 0

def temp_sensor1():
    n = random.random()

    return 60*n
    # return 50

def temp_sensor2():
    n = random.random()

    return 60*n
    # return 50

def temp_sensor3():
    n = random.random()

    return 60*n
    # return 50

def temp_sensor4():
    n = random.random()

    return 60*n
    # return 50

def temp_sensor5():
    n = random.random()

    return 60*n
    # return 50

def temp_sensor6():
    n = random.random()

    return 60*n
    # return 50




if __name__ == '__main__':
    pass