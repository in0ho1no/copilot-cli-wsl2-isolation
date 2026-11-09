## なぜ、WSL2の専用ディストリなのか

:::{container} eyebrow
03 Copilot CLIをWSL2に閉じ込める
:::

Copilot CLIのサンドボックスは、WindowsではMXCでも動く。それでもWSL2を選んだ

::::{container} cards cols-2
:::{container} card
Claude Codeも見据える

Claude Codeのサンドボックスは、ネイティブWindowsでは動かない。WSL2なら同じ構成で揃えられる
:::

:::{container} card
案件分離を意識させる

ディストリを丸ごと分ける。プロンプトのホスト名で、今どの案件にいるかが見える
:::
::::

```{revealjs-notes}
MXCを使わなかった理由は2つ。1つはClaude Codeでの利用も見据えていること。もう1つは、案件ごとにディストリを丸ごと分けることで、利用者に「別の箱で作業している」と強く意識させたかったこと。
```

## 構成：案件ごとに専用ディストリを作る

:::{container} eyebrow
03 Copilot CLIをWSL2に閉じ込める
:::

![Gitリポジトリの1ファイルから案件ごとに専用ディストリAI-caseAとAI-caseBを構築し、通信するのは各ディストリのCopilot CLI本体から公式サーバ（GitHub）へだけであることを示す構成図](/_static/figures/distro-overview.svg)

```{revealjs-notes}
構成はGitで管理したuser-data 1ファイルから、cloud-initで案件ごとのディストリを作る（約2分）。既存のWSL2には手を入れない。各ディストリの中は、wsl.conf、ランチャー、サンドボックスの層になっていて、GitHubと話すのはCLI本体だけ。AIが実行するコマンドはどこにも出られない。
```

## 3つの層で、止めるものを分担する

:::{container} eyebrow
03 Copilot CLIをWSL2に閉じ込める
:::

:::{container} rows layers
サンドボックス＋管理設定
: 止める：AIが実行するコマンド

  bubblewrapとslirp4netnsで、通信と作業フォルダ外を遮断。管理設定で、緩められない下限を置く

ランチャー
: 止める：起動の条件のばらつき

  許可リスト外の環境変数を捨て、決まった引数で起動する。直接起動は案内に置き換える

専用ディストリ
: 止める：案件をまたぐ参照

  案件ごとに分ける。wsl.confで、Windowsのファイル（`/mnt/c`）とアプリ（`powershell.exe`）への経路を断つ
:::

```{revealjs-notes}
下から、ディストリが案件の境界、ランチャーが起動条件、サンドボックスがAIのコマンドを担当する。1つの層に全部を任せず、それぞれ止めるものを分けている。Windowsアプリはサンドボックスの外で動くので、wsl.confで呼べなくしておくのが大事。
```

## 管理設定で、緩められない下限を置く

:::{container} eyebrow
03 Copilot CLIをWSL2に閉じ込める
:::

:::::{container} split
::::{container}

```{code-block} text
:caption: /etc/github-copilot/managed-settings.json

"sandbox": {
  "enabled": true,
  "failIfUnavailable": true,
  "allowBypass": false,
  "auth": { "git": false, "gh": false },
  "userPolicy": { "network": {
    "allowOutbound": false,
    "allowLocalNetwork": false
  } }
}
```

::::

::::{container} rows layers
エージェントの手が届かない場所に置く
: rootだけが書き込めるファイルにする

ここより緩められない
: ユーザ設定、リポジトリの設定、起動時の引数のどれでも

効いているかを見る
: 条件外は黙って無視される。`/sandbox`に（managed）と出るか
::::
:::::

```{revealjs-notes}
サンドボックスの設定は、/sandbox configで手で入れることもできるが、それだとエージェントやリポジトリ側の設定で緩められる余地が残る。そこで管理設定ファイルに置く。エージェントは利用者と同じworkerの権限で動くので、rootだけが書き込めるファイルにしておけば、エージェントには書き換えられない。Copilot CLIのほうも、root所有でない、root以外が書き込める、シンボリックリンクである、のどれかに当てはまるファイルは信用せず、エラーも出さずに無視する。だから構築のたびに表示で確かめる。実際は項目ごとの表示ではなく、/sandbox statusと/sandbox policyの末尾に「your organization's managed policy requires sandboxing」のような文が出る。スライドでは短く（managed）と書いている。個人のCopilot Pro+でも、ファイルで置いた管理設定が効いた。
```

## 検証結果：何がどう遮断されたか

:::{container} eyebrow
03 Copilot CLIをWSL2に閉じ込める
:::

| 確認したこと | 結果 |
| --- | --- |
| シェルからの通信（curl） | 名前解決できずに失敗。ネットワークはloだけ |
| Web取得・GitHub MCP | 接続できず、ツールは使えない |
| 作業フォルダ外のファイル | シェルからは存在ごと隠れ、組み込みツールは拒否 |
| トークン・設定ファイル | `~/.copilot/config.json`は読めず、`~/.copilot`にも書けない |
| 環境変数の鍵 | ランチャーで除かれる（`GITHUB_TOKEN`は未設定） |
| Windowsアプリ | command not found |
| 別の案件 | 別ディストリのファイルは見えない |
| メモリ機能 | 有効だと全リポジトリ共通の記憶に入った。無効化後は作業フォルダのAGENTS.mdへ |

:::{container} footnote
Copilot CLI 1.0.107、Ubuntu 24.04.5、bubblewrap 0.9.0、slirp4netns 1.2.1で確認
:::

```{revealjs-notes}
エージェントに1つずつ依頼して確かめた結果。通信は名前解決の段階で失敗し、サンドボックスの中のネットワークはループバックだけになっていた。トークンが平文で置かれる~/.copilot/config.jsonも、サンドボックスからは読めない。メモリ機能は要注意。Copilot Memoryはアカウント単位でクラウドに保存されるので、有効なままだと「覚えておいて」が全リポジトリ共通の記憶になり、ディストリを分けても案件をまたぐ。アカウント側で無効にし、CLIもmemory: falseにしたところ、作業フォルダのAGENTS.mdに書かれるようになった。個人のPro・Pro+では既定で有効、Business・Enterpriseでは既定で無効。
```

## エージェント側からは緩められない

:::{container} eyebrow
03 Copilot CLIをWSL2に閉じ込める
:::

::::{container} cards
:::{container} card
起動時の引数

`--no-sandbox`を付けても無視される

`--no-sandbox was ignored because an enterprise policy requires the sandbox.`
:::

:::{container} card
作業フォルダの設定

エージェントが書き込める場所に緩める設定を書いても、効かない
:::

:::{container} card
フック

disableAllHooksでも作業フォルダのフックは動いた。ただしフックもサンドボックス内で動き、通信できない
:::
::::

:::{container} callout
別ターミナルでの人の操作は、対象外。運用ルールで扱う
:::

```{revealjs-notes}
作業フォルダはエージェントが書き込める場所なので、そこに緩める設定を書かれたら終わり、では困る。管理設定がある限り、引数でも作業フォルダの設定でも緩められなかった。フックは止められなかったが、サンドボックスの中で動くので通信はできない。人が別のターミナルで直接操作するのは、技術ではなく運用ルールの領域。
```

## 遮断は、無害な結果に見えることがある

:::{container} eyebrow
03 Copilot CLIをWSL2に閉じ込める
:::

::::{container} cards cols-2
:::{container} card pending

```text
$ cat ~/outside/secret.txt
No such file or directory
```

ファイルは実在する。サンドボックスが存在ごと隠している
:::

:::{container} card pending

```text
$ touch ~/probe ~/.copilot/probe
（作成できたと表示）
```

実際のホームには残っていない。仮のホームに書かれて捨てられる
:::
::::

:::{container} callout
防御としては問題ない。ただ、利用者が混乱しないよう「遮断されるとこう見える」を周知しておく
:::

```{revealjs-notes}
拒否のされ方が「ファイルが無い」や「成功」に見えることがある。防御としては効いているが、利用者はバグだと思って問い合わせてくる。周知資料に、遮断されるとこう見える、の一覧を入れておく。
```
