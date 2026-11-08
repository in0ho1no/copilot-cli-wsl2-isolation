## 案件ごとに起動を制御できるCopilot CLIを選んだ

```{mascot}
:position: top-right
```

|  | Copilot Chat | Chat＋Sandbox | Copilot CLI＋WSL2 |
| --- | --- | --- | --- |
| コマンドの通信遮断 | [×]{.ng} | [△]{.mid} 設定が別途必要 | [○]{.ok} |
| Web取得の遮断 | [×]{.ng} | [△]{.mid} 別ポリシー | [○]{.ok} |
| 案件ごとの環境分離 | [×]{.ng} | [△]{.mid} Server共有 | [○]{.ok} ディストリ単位 |
| 起動方法の統一 | [×]{.ng} | [×]{.ng} | [○]{.ok} ランチャー |

:::{container} footnote
○はWindows版の検証と設計に基づく評価。WSL2上の動作は未検証（後述）
:::

:::{container} callout
MXCをWindowsで直接使う案は、Claude Codeが未対応のため見送り。Claude Codeと手段を揃え、現場の混乱を減らす
:::

## 案件ごとの専用ディストリに閉じ込める

![Windowsホスト上に既存のWSL2、Gitリポジトリ、案件ごとの専用ディストリAI-caseAとAI-caseBがあり、通信するのは各ディストリのCopilot CLI本体から公式サーバ（GitHub）へだけであることを示す構成図](/_static/figures/distro-overview.svg)

## 案件ごとの専用ディストリに閉じ込める（ディストリの中）

:::{container} rows
wsl.conf
: Windowsのファイル・アプリに届かない

ランチャー
: 環境変数を絞って起動

サンドボックス
: AIが実行するコマンド

  通信遮断・作業フォルダ外は不可

Copilot CLI本体
: 通信するのはCLI本体だけ。通信先は公式サーバ（GitHub）
:::

## 3つの層で、止めるものを分担する

:::{container} rows layers
サンドボックス＋管理設定
: AIが実行するコマンド

  bubblewrapとslirp4netnsで通信と作業フォルダ外を遮断。管理設定で緩められない下限を置く

ランチャー
: 起動の条件

  許可リスト外の環境変数を捨て、決まった設定で起動する。直接起動は案内に置き換える

専用ディストリビューション
: 案件の境界

  案件ごとに分け、wsl.confでWindows側のファイルとアプリへの経路を断つ
:::

## Windows版で遮断を確認済み。WSL2上は未検証

::::{container} cards cols-2
:::{container} card
確認済み（Windows、1.0.93）

- curlは名前解決で失敗
- 組み込みのWeb取得は拒否
- リモートMCPサーバは接続不可
- 案件外のファイルは読み取り不可
- 作業フォルダ内の設定では緩められない
:::

:::{container} card pending
未検証（WSL2上の動作）

- bubblewrapで同じ遮断ができるか
- 緩める設定が無視されるか（allowBypass、enabledなど）
- ファイル配置の管理設定が反映されるか
- リポジトリのフックを止められるか
:::
::::
