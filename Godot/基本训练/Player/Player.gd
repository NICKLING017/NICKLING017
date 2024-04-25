extends CharacterBody2D

@onready var shoot_pos = $shoot_pos
@onready var timer = $Timer
@onready var bullet = preload("res://Bullet/bullet.tscn")

@export var speed = 400
@export var max_scale_factor = Vector2(1.1, 1.1)

var default_scale = Vector2(1, 1) # 默认缩放为1
var charging = false # 是否正在蓄力
var should_restore_scale = false # 是否开始恢复缩放
@export var restore_speed = 2 # 恢复缩放速度
var charge_time = 0.0 # 蓄力时间
var can_charge = true # 初始时允许蓄力
var bullet_shoot_time = 0.5 #子弹发射时间间隔
var bullet_speed = 2000
var bullet_hurt = 1

func _ready():
	default_scale = scale

func get_input_move():
	var input_direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")
	velocity = input_direction * speed

func get_input_skill(delta):
	if Input.is_action_pressed("SPACE") and can_charge:
		charging = true
		charge_time += delta
		var jitter = Vector2(randf_range( - 0.05, 0.05), randf_range( - 0.05, 0.05))
		scale = default_scale + jitter
	elif charging:
		charging = false
		should_restore_scale = true
		can_charge = false
		# 计算最终缩放值，基于蓄力时间
		var scale_increase = min(charge_time, 1.0) / 1.0 # 限制最大蓄力时间影响
		var scale_adjustment = max_scale_factor - default_scale
		scale = default_scale + scale_adjustment * scale_increase
		charge_time = 0.0 # 重置蓄力时间
	if should_restore_scale:
		if scale.distance_to(default_scale) > 0.01:
			scale = scale.lerp(default_scale,restore_speed * delta)
		else :
			scale = default_scale
			should_restore_scale = false
			can_charge = true # scale恢复到默认值后，可以继续蓄力
	#print(scale)

func _physics_process(delta):
	get_input_move()
	get_input_skill(delta)
	move_and_slide()


func _on_timer_timeout():
	var now_bullet = bullet.instantiate() # 实例化子弹
	var mouse_position = get_global_mouse_position() # 鼠标全局位置
	now_bullet.speed = bullet_speed
	now_bullet.hurt = bullet_hurt
	now_bullet.position = shoot_pos.global_position
	var direction = (mouse_position - shoot_pos.global_position).normalized() # 子弹向鼠标方向发射
	now_bullet.dir = direction
	get_tree().root.add_child(now_bullet)
	pass # Replace with function body.
