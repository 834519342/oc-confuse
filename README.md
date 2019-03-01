# oc-deal

1.OC_JiaFeiDaiMa_deal     在OC代码中加废方法，创建废类

	-path PATH  OC代码所在目录
	-replace    直接替换oc源代码,会在脚本所在目录创建OC_JiaFeiDaiMa_backup文件夹备份源文件

  	用法：$ ./OC_JiaFeiDaiMa_deal -path 路径 -replace


2.Lua_resource_deal    在资源目录添加垃圾资源，修改所有文件的md5值

  	-path RES_DIR       资源目录
  	-out_path OUT_PATH  资源导出目录,默认导出到Lua_resource

  	用法：./Lua_resource_deal -path 路径


3.JunkFile_maker    垃圾文件生成器

  	用法：直接运行，会在脚本当前目录生成一个JunkFiles文件夹


4.OC_define_deal    扫描OC文件的类、方法、属性，用宏定义的方式混淆成随机命名，报错的地方需要添加白名单
	
	-path PATH  扫描目录

	用法：$ ./OC_define_deal -path 路径