extends Sprite2D

var normal_scale = Vector2(1,1)
var enlarged_scale = Vector2(1.5,1.5)
var is_enlarged = false

func _ready():
	scale = normal_scale

func _process(_delta):
	position = get_viewport().get_mouse_position()

func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				scale = enlarged_scale
				is_enlarged = true
			else :
				scale = normal_scale
				is_enlarged = false


