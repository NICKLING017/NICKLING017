extends CharacterBody2D

@export var movement_speed = 400.0
@export var hp = 10

# Attacks
var iceSpear = preload("res://Player/Attack/ice_spear.tscn")

# AttackNodes
@onready var iceSpearTimer = get_node("Attack/IceSpearTimer")
@onready var iceSpearAttackTimer = get_node("Attack/IceSpearTimer/IceSpearAttackTimer")

# IceSpear
var icespear_ammo = 0
var icespear_baseammo = 1
var icespear_attackspeed = 1.5
var icespear_level = 1

# Enemy Related
var enemy_close = []

func _ready():
	pass
	#attack()

func _physics_process(_delta):
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
	pass
	#print("角色死亡")

func attack():
	if icespear_level > 0:
		iceSpearTimer.wait_time = icespear_attackspeed
		if iceSpearTimer.is_stopped():
			iceSpearTimer.start()


# HurtBox 发出的信号 传递了本次碰撞的damage进来
func _on_hurt_box_hurt(damage):
	hp -= damage
	#print(hp)
	if hp <= 0:
		player_die()


func _on_ice_spear_timer_timeout():
	icespear_ammo += icespear_baseammo
	iceSpearAttackTimer.start()


func _on_ice_spear_attack_timer_timeout():
	if icespear_ammo > 0:
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
	if enemy_close.has(body):
		enemy_close.erase(body)
