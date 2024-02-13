extends Node2D

@export var spawns : Array[Spawn_info] = []

@onready var player = get_tree().get_first_node_in_group("player")

var time = 0


func _on_timer_timeout():
	# 每秒自增
	time += 1
	for i in spawns:
		# 判断是否在对应的生成信息组里 若不在这个组，则循环到下一个组 Spawn_info
		if time >= i.time_start and time <= i.time_end :
			# 如果没到时间间隔，则继续等待
			if i.spawn_delay_counter < i.enemy_spawn_delay:
				i.spawn_delay_counter += 1
			# 如果到了时间间隔，则生成敌人
			else :
				i.spawn_delay_counter = 0
				# 加载需要生成的敌人资源
				var new_enemy = i.enemy
				# 根据需要生成的数量，逐个实例化敌人
				var count = 0
				while count < i.enemy_num :
					var enemy_spawn = new_enemy.instantiate()
					#enemy_spawn.global_position = get_random_position()
					add_child(enemy_spawn)
					count += 1
					print("生成敌人成功")




func get_random_position():
	pass
