extends Area2D


@onready var collision = $CollisionShape2D
@onready var disabletimer = $DisableTimer

signal hurt(damage)

func _on_area_entered(area):
	if area.is_in_group("attack"):
		# print("碰撞成功")
		# 碰撞成功 则关闭collision
		collision.set_deferred("disabled",true)
		# 然后开启计时器，方便持续碰撞生效
		disabletimer.start()
	var damage = area.damage
	emit_signal("hurt",damage)


func _on_disable_timer_timeout():
	collision.set_deferred("disabled",false)
