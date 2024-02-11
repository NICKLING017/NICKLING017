extends Node2D

# 生成敌人相关信息的数组
@export var spawns: Array[Spawn_info] = []

@onready var player = get_tree().get_first_node_in_group("player")

var time = 0



func _on_timer_timeout():
	time += 1
	var enemy_spawns = spawns
	# 遍历每一个Spawn_info 元素
	for i in enemy_spawns:
		# 时间符合 则执行生成逻辑
		if time >= i.time_start and time <= i.time_end:
			# 这部分代码处理敌人的生成延迟。如果延迟计数器小于设置的生成延迟，它就增加；否则，重置计数器并且生成敌人
			if i.spawn_delay_counter < i.enemy_spawn_delay:
				i.spawn_delay_counter += 1
			else :
				i.spawn_delay_counter = 0
				# 加载怪物场景（资源）
				var new_enemy = load(str(i.enemy.resource_path))
				# 根据需要生成的敌人数量，循环实例化敌人
				var counter = 0
				while counter < i.enemy_num:
					var enemy_spawn = new_enemy.instantiate()
					# 设置敌人的全局位置为一个随机位置，将敌人节点添加为当前节点的子节点，并增加计数器
					enemy_spawn.global_position = get_random_position() # get_random_position() 随机生成位置
					add_child(enemy_spawn)
					counter += 1


func get_random_position():
	# 获取游戏窗口尺寸并随机放大1.1~1.4倍 用于在频幕外生成敌人位置
	var vpr = get_viewport_rect().size * randf_range(1.1,1.4)
	var top_left = Vector2(player.global_position.x - vpr.x/2,player.global_position.y - vpr.y/2)
	var top_right = Vector2(player.global_position.x + vpr.x/2,player.global_position.y - vpr.y/2)
	var bottom_left = Vector2(player.global_position.x - vpr.x/2,player.global_position.y + vpr.y/2)
	var bottom_right = Vector2(player.global_position.x + vpr.x/2,player.global_position.y + vpr.y/2)
	# 随机选择一条边生成敌人
	var pos_side = ["up","down","right","left"].pick_random()
	var spawn_pos1 = Vector2.ZERO
	var spawn_pos2 = Vector2.ZERO

	match pos_side:
		"up":
			spawn_pos1 = top_left
			spawn_pos2 = top_right
		"down":
			spawn_pos1 = bottom_left
			spawn_pos2 = bottom_right
		"right":
			spawn_pos1 = top_right
			spawn_pos2 = bottom_right
		"left":
			spawn_pos1 = top_left
			spawn_pos2 = bottom_left

	var x_spawn = randf_range(spawn_pos1.x,spawn_pos2.x)
	var y_spawn = randf_range(spawn_pos1.y,spawn_pos2.y)
	return Vector2(x_spawn,y_spawn)


