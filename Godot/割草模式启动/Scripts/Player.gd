extends CharacterBody2D

var movement_speed = 400.0
var hp = 80

# Attacks
var iceSpear = preload("res://tscn/Player/Attack/ice_spear.tscn")

# AttackNodes
@onready var iceSpearTimer = $Attack/IceSpearTimer
@onready var iceSpearAttackTimer = $Attack/IceSpearTimer/IceSpearAttackTimer

# IceSpear
var icespear_ammo = 0
var icespear_baseammo = 1
var icespear_attackspeed = 1.5
var icespear_level = 1

# Enemy Related
var enemy_close = []

func _ready():
	attack()



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


func attack():
	if icespear_level > 0:
		iceSpearTimer.wait_time = icespear_attackspeed
		if iceSpearTimer.is_stopped():
			iceSpearTimer.start()

func _on_hurt_box_hurt(damage):
	hp -= damage
	print(hp)


func _on_ice_spear_timer_timeout():
	icespear_ammo += icespear_baseammo
	iceSpearAttackTimer.start()


func _on_ice_spear_attack_timer_timeout():
	if icespear_ammo > 0:
		# iceSpear.instantiate() 实例化iceSpear场景
		var icespear_attack = iceSpear.instantiate()
		icespear_attack.position = position
		icespear_attack.target = get_random_target()
		icespear_attack.level = icespear_level
		add_child(icespear_attack)
		icespear_ammo -= 1
		if icespear_ammo > 0:
			iceSpearAttackTimer.start()
		else:
			iceSpearAttackTimer.stop()




func get_random_target():
	if enemy_close.size() > 0:
		var potential_target = enemy_close.pick_random()
		if is_instance_valid(potential_target):
			return potential_target.global_position
	return Vector2.UP



func _on_enemy_detection_area_body_entered(body):
	if not enemy_close.has(body):
		enemy_close.append(body)


func _on_enemy_detection_area_body_exited(body):
	if not enemy_close.has(body):
		enemy_close.erase(body)
