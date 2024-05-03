extends Area2D



func _on_body_entered(body):
	print("+1 coin!")
	queue_free() # 将节点加入队列，在当前帧结束时删除
