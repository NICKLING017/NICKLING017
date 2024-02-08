using Godot;
using System;

public partial class InputTest : Node
{
	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		// 鼠标设置：显示、隐藏、限制在游戏窗口内
		//Input.MouseMode = Input.MouseModeEnum.Confined;
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
		// 是否按下键盘的B键
		if (Input.IsKeyPressed(Key.B))
		{
			GD.Print("press B");
		}
		// 按下虚拟按键
		if (Input.IsActionJustPressed("跳跃"))
		{
			GD.Print("按下跳跃");
		}
		if (Input.IsActionPressed("跳跃"))
		{
			GD.Print("跳跃中");
		}
		if (Input.IsActionJustReleased("跳跃"))
		{
			GD.Print("跳跃完成");
		}
		// 获取按键力度
		// float s = Input.GetActionStrength("跳跃");
		// GD.Print(s);

		// 获取一个水平轴
		float horizontal = Input.GetAxis("左", "右");


		// 获取上下左右组成的向量

		Vector2 dir = Input.GetVector("左", "右", "上", "下");
		GD.Print(dir);


	}


	public override void _Input(InputEvent @event)
	{
		base._Input(@event);
		// 如果是键盘事件
		if (@event is InputEventKey)
		{
			// 转成键盘事件
			var key = @event as InputEventKey;
			// 判断当前是否按下的是v键
			if (key.Keycode == Key.V)
			{
				// 判断是否持续按压
				if (key.IsEcho())
				{
					GD.Print("持续按下");
				}
				// 判断是否按下瞬间
				else if (key.IsPressed())
				{
					GD.Print("按下瞬间");
				}
				// 判断是否抬起瞬间
				else if (key.IsReleased())
				{
					GD.Print("抬起瞬间");
				}
			}
		}

		// 如果是鼠标事件
		if (@event is InputEventMouse)
		{
			// 转成鼠标事件
			var mouse = @event as InputEventMouse;
			// 判断是否点击左键
			if (mouse.IsPressed())
			{
				// 打印鼠标位置
				GD.Print(mouse.Position);
				// 打印鼠标按键
				GD.Print(mouse.ButtonMask);

			}


		}

	}
}
