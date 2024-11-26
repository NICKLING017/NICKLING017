extends CharacterBody2D

@export var speed = 400
@export var acceleration = 600
@export var friction = 800
@export var fire_rate = 0.1  # 射击间隔时间（秒）
@export var bullet_scene: PackedScene

var time_since_last_shot = 0.0 # 距离上次射击的时间间隔

func get_input():
	return Input.get_vector("move_left", "move_right", "move_up", "move_down")

func _physics_process(delta):
	var input_direction = get_input()
	time_since_last_shot += delta

	if input_direction != Vector2.ZERO:
		# 加速
		velocity = velocity.move_toward(input_direction * speed, acceleration * delta)
	else:
		# 减速
		velocity = velocity.move_toward(Vector2.ZERO, friction * delta)
	move_and_slide()
	#print(velocity)

	 # 获取鼠标在世界中的位置
	var mouse_position = get_global_mouse_position()
	# 计算玩家到鼠标的方向
	var direction = (mouse_position - global_position).normalized()
	# 计算旋转角度
	rotation = direction.angle()

	if Input.is_action_pressed("fire") and time_since_last_shot >=fire_rate:
		shoot_bullet()
		time_since_last_shot = 0

func shoot_bullet():
	var bullet = bullet_scene.instantiate()

	# 计算枪口位置
	var offset = Vector2(100, 0).rotated(rotation)  # 设置偏移距离
	bullet.global_position = global_position + offset
	bullet.rotation = rotation  # 设置子弹的旋转与玩家一致
	bullet.direction = Vector2.RIGHT.rotated(rotation)  # 设置子弹的移动方向
	get_tree().current_scene.add_child(bullet)


