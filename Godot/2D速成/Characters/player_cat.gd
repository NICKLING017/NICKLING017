extends CharacterBody2D

@export var move_speed : float = 100
@export var starting_direction : Vector2 = Vector2(0,1)


@onready var animation_tree = $AnimationTree
@onready var state_machine = animation_tree.get("parameters/playback")

func _ready():
	# 默认待机动画
	update_animation_parameters(starting_direction)

func _physics_process(_delta):
	# 获取输入方向
	var input_direction = Vector2(
		Input.get_action_strength("right") - Input.get_action_strength("left"),
		Input.get_action_strength("down") - Input.get_action_strength("up")
	)
	# 移动动画
	update_animation_parameters(input_direction)
	# 设置速度
	velocity = input_direction * move_speed
	move_and_slide()
	pick_new_state()


# 根据输入方向更新动画
func update_animation_parameters(move_input:Vector2):
	if (move_input != Vector2.ZERO):
		animation_tree.set("parameters/Walk/blend_position",move_input)
		animation_tree.set("parameters/Idle/blend_position",move_input)

# 动画切换
func pick_new_state():
	if(velocity != Vector2.ZERO):
		state_machine.travel("Walk")
	else:
		state_machine.travel("Idle")
