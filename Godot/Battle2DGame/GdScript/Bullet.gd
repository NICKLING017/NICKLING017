extends Node2D

@export var speed = 1000
var direction = Vector2.ZERO

func _process(delta):
	# 仅根据初始方向移动
	position += direction * speed * delta

	# 如果子弹离开屏幕边界，销毁它
	if not get_viewport_rect().encloses(Rect2(global_position, Vector2.ZERO)):
		queue_free()
