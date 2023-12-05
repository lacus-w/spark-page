 
    以随机时间间隔在一个目录下生成大量文件，
    文件随机命名，文件中包含随机生成的一些
    英文语句，每个英文语句内部的单词用空格
    隔开。

- 分析：

启动程序后要随机的在某个目录下生成文件，每次生成新文件的时间间隔随机，比如可以是10秒内任意一个数

可以设计简单的循环程序，每次生成文件后，程序暂停x秒，x是1到10以内的随机数

- 提示：

### 1. 随机时间间隔

调用库函数得到随机整数：

```scala
// 调用构造函数，返回Random类的实例，存到变量r中：
val r = scala.util.Random
// x是1到10以内的随机数:
x = r.nextInt(10)
while(true) { // 持续生成文件，直到CTRL-C终止程序
    // TODO: 在某个目录下生成文件
    Thread.sleep( x*1000 ) // 每次生成文件后，程序暂停x秒 
}
```

### 2. 在目录中创建文件

> 读写文件的用法参考课本26页

生成文件的路径存在 `x_path` 变量中：
（在运行程序前先 `mkdir ~/exp19` 创建目录，这样程序就不会读到一个不存在的目录了）

```scala
val x_path = "/home/hm/exp19"
```

文件名称按编号顺序，每次创建新的文件：

```scala
var i = 1 //文件的编号
import java.io.PrintWriter
val a_file = new PrintWriter( x_path + "/" + i ) 
i += 1 // 创建对应编号的文件后，更新编号
a_file.print(/*由一些单词组成的行*/)
a_file.close // 写完一行后关闭文件
```

### 3. 随机单词

如果要用随机单词得到一句话，可以从一段文本中随便抽几个词组在一起

更简单的操作是随机得到几个小写字母放在一起：

```scala
val x_length = r.nextInt(10) + 1 // 单词的长度随机，范围是1到10
val a_word = r.alphanumeric.filter(_.isLower).take(x_length).mkString
print("生成的随机单词是:" + a_word)
```

得到的 `a_word` 是10个以内小写字母组成的单词

### 4. 随机个单词组成的句子

随机个单词组在一起，用空格隔开就可以得到一行内容了：

```scala
val n = r.nextInt(10) + 1 // 一行可以由随机个单词构成，范围是1到10
var a_line = ""
for (i <- 1 to n) {
  //TODO: 得到一个随机单词a_word
  a_line += a_word // 单词追加到句子里面
  a_line += " "    // 单词后面用空格隔开
}
print("生成的一行句子是:" + a_line)
```