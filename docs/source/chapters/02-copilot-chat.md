## 実現手段として3つを順に検討した

:::{container} steps
GitHub Copilot Chat（VS Code）
: まず導入しやすい手段

Copilot Chat＋標準のSandbox
: VS Code標準の封じ込めを追加

Copilot CLI＋WSL2
: VS Codeの外で起動を制御する
:::

## Copilot Chatだけでは、経路を止める境界がない

:::::{container} split
::::{container}
![Copilot Chat（VS Code）からコマンド実行・Web取得・MCPサーバを経由して外部へつながる経路の図](/_static/figures/chat-paths.svg)

:::{container} callout
実行前の承認は人の判断に頼る。OSが止めるわけではない
:::
::::

::::{container} stack
:::{container} card
通信

案件単位で外部通信を遮断する強制力がない
:::

:::{container} card
分離

ユーザメモリは全ワークスペース共通。VS Code Serverも案件をまたいで共有される
:::
::::
:::::
