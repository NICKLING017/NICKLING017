extends Area2D

@export_enum("Cooldown","HitOnce","DisableHitBox") var HurtBoxType = 0

@onready var collision = $CollisionShape2D
@onready var disableTImer = $DisableTimer

signal hurt(damage)

func _on_area_entered(area):
	if area.is_in_group("attack"):
		if not area.get("damage") == null:
			match HurtBoxType:
				0: #Cooldown
					# 专门用来延迟设置一个属性的函数
					collision.set_deferred("disabled",true)
					# call_deferred("method", args...)是一个更通用的函数，可以用来延迟调用任何方法
					# collision.call_deferred("set","disabled",true)
					disableTImer.start()
				1: #HitOnce
					pass
				2: #DisalbeHitBox
					if area.has_method("tempdisable"):
						area.tempdisable()
			var damage = area.damage
			emit_signal("hurt",damage)

func _on_disable_timer_timeout():
	collision.set_deferred("disabled",false)
