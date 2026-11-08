## 発端1：特定の案件で外部通信の禁止が必要になった

::::{container} cards
:::{container} card
プロンプトインジェクションの防止

外部のページに仕込まれた指示を、AIに読ませない
:::

:::{container} card
OSSコード流入の防止

外部のコードが、成果物に混ざらないようにする
:::

:::{container} card
検索クエリからの漏えい防止

案件の情報が、検索語に乗って外へ出ないようにする
:::
::::

## 発端2：案件間で情報が混ざらないようにする必要があった

::::{container} split
:::{container} figure-box
![1台のPC上で、発注元Aと発注元Bの案件がAIのメモリ／workspaceを経由して混ざる図](/_static/figures/data-mixing.svg)
:::

:::{container} panel
防ぎたいこと

メモリやworkspaceを経由した、別案件への情報流出

人経由の流入はこれまでもあった。今回防ぐのは、AIが意図せず流用してしまうこと
:::
::::
