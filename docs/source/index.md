# WSL2を用いたCopilot CLI環境の分離

```{mascot}
:action: jump
```

:::{container} subtitle
外部通信の禁止と案件間の情報分離を、利用者のPC上で実現する
:::

```{revealjs-notes}
顧客要件をきっかけに検討した、Copilotの封じ込め方法を紹介します。
```

## アジェンダ

:::{container} agenda
1. そもそもの発端
2. GitHub Copilot Chatでは不十分だった
3. 単なるサンドボックスでは不十分だった
4. Copilot CLI+WSL2で封じ込める
5. 運用方針
6. まとめ
:::

```{include} chapters/01-origin.md
```

```{include} chapters/02-copilot-chat.md
```

```{include} chapters/03-sandbox.md
```

```{include} chapters/04-cli-wsl2.md
```

```{include} chapters/05-operation.md
```

```{include} chapters/06-summary.md
```
