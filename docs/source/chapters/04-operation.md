## 利用者へのお願いは「ランチャーから起動する」だけ

:::{container} eyebrow
04 運用に落とす
:::

:::::{container} split
::::{container}
```text
$ copilot
Copilot CLIはランチャー（/opt/ai-env/launch-copilot.sh）から起動してください
$ /opt/ai-env/launch-copilot.sh
```
::::

::::{container} card
ランチャーがやること

- 許可リスト以外の環境変数を捨てる
- Gitリポジトリを保護してから起動する
- `--sandbox`と`--disable-builtin-mcps`を付ける
::::
:::::

:::{container} callout
直接起動はガード関数で案内に置き換える。設定し忘れる余地を作らない
:::

```{revealjs-notes}
利用者に覚えてもらうことを1つに絞った。copilotと直接打つと、ランチャーを使うよう案内が出る。ランチャーは環境変数を許可リストで絞り、Gitリポジトリを保護してから起動する。--disable-builtin-mcpsは、起動のたびにGitHub MCPの接続失敗が表示されて問い合わせが来るのを防ぐため。意図的な迂回（command copilotなど）は残るが、管理設定でサンドボックスは外れない。
```

## Git：コミットはエージェント、Pushは人

:::{container} eyebrow
04 運用に落とす
:::

::::{container} cards cols-2
:::{container} card pending
エージェント

- コミット：できる
- Push：できない

`Could not resolve host: github.com`
:::

:::{container} card
人（別ターミナル）

fine-grained PATでPushする

対象リポジトリだけ、Contentsの読み書きだけ、有効期限は短く。credential.helperのcacheでメモリに1時間だけ持つ
:::
::::

:::{container} callout
使わない：gh auth login、credential.helper store、SSH鍵。どれもディスクに残るため
:::

```{revealjs-notes}
エージェントは通信できないので、コミットまではできてもPushはできない。これは想定どおり。Pushは人が別ターミナルで行う。トークンは期限付きで、メモリに1時間だけ置くので、後から取り消して回る作業そのものが要らない設計にした。
```

## 仕込まれたフックは、人の操作で動く

:::{container} eyebrow
04 運用に落とす
:::

:::{container} callout warn
保護する前は、エージェントが置いたフックが、人のコミットをきっかけにWSL2内でも、Windows側のVS Codeからも実行された
:::

:::::{container} split
::::{container}
| 対象 | 所有者と権限 |
| --- | --- |
| `.git` | root:worker 3775（作れるが消せない） |
| `.git/config` | root:root 0644（書き換えられない） |
| `.git/hooks` | root:root 0755（追加できない） |
::::

::::{container} card
自動で保護する

ランチャーの起動前と、1分ごとのタイマーで実行。既に怪しいフックや設定があれば警告する
::::
:::::

```{revealjs-notes}
検証でいちばん意外だったところ。サンドボックスの中のエージェントは外に出られなくても、.git/hooksにフックを置かれると、人がサンドボックスの外でコミットしたときに人の権限で動く。Windows側のVS Codeからコミットすれば、通信制限もファイル制限もないWindows本体で動く。そこでOSのファイル権限で、configとhooksをroot所有にした。コミットやPushは普通にできる。
```

## 消すときは、トークンを取り消してから

:::{container} eyebrow
04 運用に落とす
:::

削除は専用のスクリプト（`Remove-AiDistro.ps1`）で行う。

:::{container} steps
取り出す
: ディストリ内のトークン。値は表示しない

取り消す
: GitHubのRevoke API（202）

確かめる
: そのトークンが401になるまで待つ

削除する
: 名前を再入力してから登録を解除
:::

:::{container} callout warn
どこかで失敗したら、ディストリは消さずに止まる

先に`wsl --unregister`で消すと、トークンを取り出せず手作業で取り消すしかない。手作業は必ず漏れる
:::

```{revealjs-notes}
案件が終わってディストリを消すとき、中のCopilot CLIのトークンはGitHub側で有効なまま残る。削除スクリプトは、トークンを取り出して取り消し、無効になったのを確かめてからディストリを消す。2つのディストリで、取り消しと削除まで成功した。
```

## VS Codeは、Windows側から開いて使う

:::{container} eyebrow
04 運用に落とす
:::

:::{container} rows
`\\wsl.localhost`経由で開く
: automountを切っているので、WSL拡張では接続できない

AI拡張は使わない
: サンドボックスを通らずに、案件のファイルを扱えてしまう

制限モードで開く
: エージェントが置いた`tasks.json`などが、Windows本体で自動実行されるのを防ぐ
:::

```{revealjs-notes}
IDEとして使いたいという声には、Windows側のVS Codeで\\wsl.localhost経由で開く形で応える。WSL拡張はVS Code Serverの導入に/mnt/cを使うので、automountを切ったこの構成ではつながらない。Windows本体には制限がないので、Copilot ChatなどのAI拡張は使わない。また、エージェントはサンドボックスの中でも作業フォルダに.vscode/tasks.jsonを書ける。信頼したワークスペースとして開くと、フォルダを開いたときに動くタスクがWindows本体で実行されてしまう。前の章のフックと同じで、エージェントが仕込み、人の操作で動く構図なので、制限モードで開く。
```
