## VS CodeのSandboxを有効にしても、通信は止まらない

```{mascot}
:position: bottom-left
```

:::{container} eyebrow
02 Copilot Chatでは足りなかった
:::

:::{container} rows
外向き通信
: 既定で許可。トグルはオン・オフだけで、通信は止まらない

fetch・統合ブラウザ
: サンドボックスの対象外。別のポリシーで止める必要がある

Localセッション
: 対象外。効くのはAgent Hostセッションだけ
:::

```{revealjs-notes}
最初はVS CodeのCopilot Chatで試した。Sandboxのトグルを有効にしても外向き通信は既定で許可のまま。fetchや統合ブラウザは対象外、Localセッションも対象外。個別の設定で塞げる穴はあるが、全部を揃える必要がある。（このパートは3分で流す）
```

## 案件単位で強制できない

```{mascot}
:position: bottom-left
```

:::{container} eyebrow
02 Copilot Chatでは足りなかった
:::

::::{container} cards cols-2
:::{container} card
分離

VS Code Serverが、案件をまたいで共有される
:::

:::{container} card
起動

起動のしかたを揃えられず、案件ごとの設定を強制する入口がない
:::
::::

:::{container} callout
案件ごとにプロセスを分けて起動できる、Copilot CLIを選んだ
:::

```{revealjs-notes}
結局、案件ごとに分けて強制する入口がないのが問題だった。CLIなら案件ごとに別プロセスで、ランチャーで起動条件を決められる。Claude Codeと同じ考え方で揃えられる。
```
