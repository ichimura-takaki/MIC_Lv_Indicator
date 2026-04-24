# MIC_Lv_Indicator
## 概要
マイクのレベルインジケーターです。
3.5mmで接続してると不具合多発すると思うので、レベル監視に利用してください。
javaで作ったほうが良かったんじゃねって言わないでください！作ったあとに思いました（笑）

## アプリケーションとして利用する
pythonの事前インストールが必要です。
pythonのインストール時にpipがついてくると思うので、
以下コマンドからアプリ化する必要があります。
```
#macもwinも実施してください。
pip install pyinstaller
```

### .exeにする
windowsの人向けです。
```
cd "保存したいpath"
pyinstaller --noconsole --onefile "pythonファイルのpath"
#上記を実行すると/dict に生成されます
```
### .appにする
macの人向けです。
※テストしてないから正しく動作するかわかりません。
※最初にマイク権限を付与する必要があるっぽい。
```
cd "保存したいpath"
pyinstaller --onefile --windowed "pythonファイルのpath"
#上記を実行すると/dict に生成されます
```
