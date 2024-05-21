extends Node

var health = 100

func _ready():
	health = 40
	health = 20 + 30
	health += 20
	health -= 10
	print(health)
