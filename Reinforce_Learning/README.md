# Reinforce Learning Learning

Try on Q-Learning first

Q-Learning思路：

初始化Q(s,a),Vs e S,ae A(s),任意的数值，并且Q(terminal - state,”) =0

重复（对每一节episode)

初始化 状态S

重复（对episode中的每一步）：

使用某一个policy比如（e— greedy)根据状态S选取一个动作执行

执行完动作后，观察reward和新的状态S'

Q(S,A0- Q(S,AD) + a(R+1 + Amax. Q(S+1,a) - Q(S, Ag)

S-S'

循环直到S终止
