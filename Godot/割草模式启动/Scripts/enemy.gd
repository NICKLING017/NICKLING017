extends CharacterBody2D

@export var movement_speed = 200.0
# 访问player组中的第一个节点
@onready var player = get_tree().get_first_node_in_group("player")
@onready var sprite = $Sprite2D

func _physics_process(_delta):
	var direction = global_position.direction_to(player.global_position)
	velocity = direction * movement_speed
	move_and_slide()
	Sprite(direction)

# 敌人翻转
func Sprite(direction):
	if direction.x > 0:
		sprite.flip_h = true
	else: sprite.flip_h = false
