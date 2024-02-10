extends CharacterBody2D

var movement_speed = 400.0

func _physics_process(delta):
	movement()

 # 角色移动函数
func movement():
	var x_mov = Input.get_action_strength("right") - Input.get_action_strength("left")
	var y_mov = Input.get_action_strength("down") - Input.get_action_strength("up")
	var mov = Vector2(x_mov,y_mov)
	velocity = mov.normalized() * movement_speed
	move_and_slide()  # 角色移动内置函数
	animateSprite(x_mov)

# 角色面向动画函数
func animateSprite(x_mov):
	$AnimatedSprite2D.play()
	if x_mov > 0:
		$AnimatedSprite2D.animation = "player_right"
	if x_mov < 0:
		$AnimatedSprite2D.animation = "player_left"

