extends CharacterBody2D

@export var movement_speed = 400.0
@export var hp = 10

func _ready():
	pass

func _physics_process(delta):
	movement()

# 角色移动
func movement():
	var x_move = Input.get_action_strength("右") - Input.get_action_strength("左")
	var y_move = Input.get_action_strength("下") - Input.get_action_strength("上")
	var move = Vector2(x_move,y_move)
	velocity = move.normalized() * movement_speed
	move_and_slide()
	if velocity.x < 0:
		$AnimatedSprite2D.animation = "player_left"
	elif velocity.x > 0 :
		$AnimatedSprite2D.animation = "player_right"
	$AnimatedSprite2D.play()



func player_die():
	print("角色死亡")

# HurtBox 发出的信号 传递了本次碰撞的damage进来
func _on_hurt_box_hurt(damage):
	hp -= damage
	print(hp)
	if hp <= 0:
		player_die()
