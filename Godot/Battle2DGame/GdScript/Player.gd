extends CharacterBody2D

@export var speed = 400
@export var acceleration = 600
@export var friction = 800
@export var fire_rate = 0.1  # 射击间隔时间（秒）
@export var bullet_scene: PackedScene
@export var base_texture: Texture2D
@export var shot_texture: Texture2D

@onready var _animation_player = $AnimatedSprite2D
@onready var sprite = $Sprite2D

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

	if velocity != Vector2.ZERO:
		_animation_player.visible = true
		_animation_player.play("Walk")
	else:
		_animation_player.stop()
		_animation_player.visible = false


	 # 获取鼠标在世界中的位置
	var mouse_position = get_global_mouse_position()
	# 计算玩家到鼠标的方向
	var direction = (mouse_position - global_position).normalized()
	# 计算旋转角度
	rotation = direction.angle()

	if Input.is_action_pressed("fire") and time_since_last_shot >=fire_rate:
		shoot_bullet()
		time_since_last_shot = 0

# 切换到基本纹理
func switch_back_texture():
	sprite.texture = base_texture
	print("base texture")

func shoot_bullet():
	var bullet = bullet_scene.instantiate()

	# 切换到射击纹理
	sprite.texture = shot_texture
	print("shot texture")

	# 设置子弹属性并发射
	var offset = Vector2(100, 0).rotated(rotation) # 枪口位置偏移
	bullet.global_position = global_position + offset
	bullet.rotation = rotation # 子弹方向跟随角色方向
	bullet.direction = Vector2.RIGHT.rotated(rotation)
	get_tree().current_scene.add_child(bullet)

	# 使用计时器延迟切换回基本纹理
	var timer = get_tree().create_timer(0.2)
	timer.timeout.connect(switch_back_texture) # 超时后调用switch_back_texture



