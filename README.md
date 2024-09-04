# weread_to_flomo

微信读书笔记同步至 flomo - Python 脚本实现

## 使用方法

- 将微信读书笔记导出至一个文本文件中：

  - 微信读书 App，我 - 笔记 - 点开某本书的笔记 - 点击 `导出笔记`
  - 创建一个空文件，将笔记粘贴到文件中，保存。
- 下载仓库里的 `weread_2_flomo.py` 脚本
- 终端中执行：

  ```shell
  python3 weread_2_flomo.py
  ```
- 根据提示输入：

  - flomo api （[获取方法](https://v.flomoapp.com/mine?source=incoming_webhook)）
  - 标签名称，带井号（如：`#读书/悉达多`）
  - 导出笔记的文件路径

## 帮助

- 导出的微信读书笔记中，开头会写有 `xx个笔记`，如果解析出的笔记数和这个数目不同，则脚本逻辑有错误，需要调整脚本
- flomo 每天通过 API 最多发布 100 条。
- 笔记是每个划线发送一条 flomo。如果想要每章所有划线聚合成一条flomo，可以自行更改脚本。
