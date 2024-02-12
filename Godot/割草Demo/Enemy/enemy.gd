extends CharacterBody2D

@export var movement_speed = 200.0

@onready var player = get_tree().get_first_node_in_group("player")
@onready var anim = $AnimatedSprite2D

func _physics_process(delta):
	movement()

func movement():
	# 怪物朝着玩家位置移动
	var direction = global_position.direction_to(player.global_position)
	velocity = direction * movement_speed
	move_and_slide()
	if velocity.x < 0:
		anim.animation = "enemy_left"
	elif velocity.x > 0 :
		anim.animation = "enemy_right"
	anim.play()

