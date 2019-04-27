### 该目录下文件的说明

dev 小型测试集，用户在训练中评估模型性能
test SemEval2010Task8 中的测试集，用于训练好以后评估模型性能。部署到项目中的时候为待标注数据
test.jsonl.bak SemEval2010Task8 测试集的备份
train_all 训练集全集
train_activelearning 主动学习的训练集
train_activelearning_remain 主动学习的剩余训练集
train_control 对照组的训练集
train_control_remain 对照组的剩余训练集


### 主动学习流程

首先随机选择200个数据作为冷启动数据

训练完（epoch=3）以后，首先记录其在测试集上的结果
然后，用训练好的模型对剩余训练集进行预测
在预测结果中取熵最大的200个数据添加到现有训练集
对照组则从剩余训练集中随机选取200个数据
此时两者训练集中均有400个数据，测试集还是验证集

重复上述过程