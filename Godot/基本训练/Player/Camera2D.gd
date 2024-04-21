extends Camera2D

const MAX_DISTANCE = 48 # 摄像头移动的最大距离

var target_distance = 0
var center_pos = position # 初始化摄像头位置

func _process(delta):
	var direction = center_pos.direction_to(get_local_mouse_position()) # 计算摄像头位置到鼠标位置的方向向量
	var target_pos = center_pos + direction * target_distance # 根据方向和目标距离计算目标位置

	target_pos = target_pos.clamp(
		center_pos - Vector2(MAX_DISTANCE,MAX_DISTANCE),
		center_pos + Vector2(MAX_DISTANCE,MAX_DISTANCE)
	)

	position = target_pos

func _input(event):
	if event is InputEventMouseMotion: # 如果检测到鼠标移动事件
		target_distance = center_pos.distance_to(get_local_mouse_position())/2 # 取中心点

