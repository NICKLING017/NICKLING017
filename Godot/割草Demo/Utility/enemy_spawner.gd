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
					# 随机生成敌人的坐标位置
					enemy_spawn.global_position = get_random_position()
					# get_random_position()
					add_child(enemy_spawn)
					count += 1
					# print("生成敌人成功")




func get_random_position():
	# 获取游戏窗口大小并随机增大范围
	var viewport_size = get_viewport_rect().size  * randf_range(1.1,1.4)
	var top_left = Vector2(player.global_position.x - viewport_size.x/2,player.global_position.y - viewport_size.y/2)
	var top_right = Vector2(player.global_position.x + viewport_size.x/2,player.global_position.y - viewport_size.y/2)
	var bottom_left = Vector2(player.global_position.x - viewport_size.x/2,player.global_position.y + viewport_size.y/2)
	var bottom_right = Vector2(player.global_position.x + viewport_size.x/2,player.global_position.y + viewport_size.y/2)
	# 随机选择一条边生成敌人
	var pos_side = ["上","下","左","右"].pick_random()
	var spawn_pos1 = Vector2.ZERO
	var spawn_pos2 = Vector2.ZERO
	match pos_side:
		"上":
			spawn_pos1 = top_left
			spawn_pos2 = top_right
		"下":
			spawn_pos1 = bottom_left
			spawn_pos2 = bottom_right
		"左":
			spawn_pos1 = top_left
			spawn_pos2 = bottom_left
		"右":
			spawn_pos1 = top_right
			spawn_pos2 = bottom_right

	var x_spawn = randf_range(spawn_pos1.x,spawn_pos2.x)
	var y_spawn = randf_range(spawn_pos1.y,spawn_pos2.y)
	# print("生成敌人坐标：")
	# print(Vector2(x_spawn,y_spawn))
	return Vector2(x_spawn,y_spawn)


