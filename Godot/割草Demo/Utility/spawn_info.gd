extends Resource

class_name Spawn_info

@export var time_start : int # 阶段开始时间
@export var time_end : int # 阶段结束时间
@export var enemy : Resource # 生成的敌人资源场景
@export var enemy_num : int # 每次生成的数量
@export var enemy_spawn_delay : int # 生成逻辑时间间隔 每隔多少秒生成一次敌人

var spawn_delay_counter = 0 # 跟踪自上次生成敌人以来经过的时间


