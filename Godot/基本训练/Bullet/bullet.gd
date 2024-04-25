extends CharacterBody2D

var dir = Vector2.ZERO
var speed = 2000
var hurt = 1

func _process(delta):
	velocity =dir * speed
	move_and_slide()
