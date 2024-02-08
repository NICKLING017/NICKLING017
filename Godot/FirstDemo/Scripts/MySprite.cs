using Godot;
using System;

public partial class MySprite : Sprite2D
{
	// 倒计时，设定一个计时器
	float timer = 5;

	// 节点添加到节点树中的时候调用
	public override void _EnterTree()
	{
		base._EnterTree();
		GD.Print("entertree!");

	}

	// Called when the node enters the scene tree for the first time.
	// 节点加载完成，准备初始化：一般把初始化写进这里
	public override void _Ready()
	{
		GD.Print("ready!");
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	// 每一帧调用该方法
	public override void _Process(double delta)
	{
		// 游戏逻辑
		timer -= (float)delta;
		if (timer <= 0)
		{
			timer = 100;
		}
		// 销毁节点
		this.QueueFree();

	}

	// 每次物理系统计算，会调用这个方法
	public override void _PhysicsProcess(double delta)
	{
		// 物理交互逻辑
		base._PhysicsProcess(delta);
	}

	// 节点离开节点树、销毁
	public override void _ExitTree()
	{
		base._ExitTree();
		GD.Print("exittree!");
	}
}
