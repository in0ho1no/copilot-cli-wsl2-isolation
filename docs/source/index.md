# 「外部通信禁止」と言われたので、<br>Copilot CLIをWSL2に閉じ込めた

```{mascot}
:action: jump
```

:::{container} eyebrow
GitHub Copilot CLI × WSL2
:::

:::{container} byline
inoinoino

GitHub: in0ho1no
:::

```{revealjs-notes}
今日は、外部通信を禁止された案件でもCopilot CLIを使い続けるために作った環境と、その判断の過程を話す。（2分パートの入口）
```

## inoinoino

:::{container} eyebrow
自己紹介
:::

::::::{container} profile

```{image} /_static/images/profile-icon.jpg
:alt: プロフィール画像のジョウビタキ
:class: profile-icon
```

:::::{container}
:::{container} accounts
GitHub: in0ho1no　／　X: @in0ho1no
:::

::::{container} stack
:::{container} card
普段は組み込み開発

C言語一筋10年 / 趣味でPythonを数年
:::

:::{container} card
AIは個人利用が主

業務での利用は推進中
:::
::::
:::::
::::::

```{revealjs-notes}
普段は組み込み開発で、C言語一筋10年。Pythonは趣味で数年。AIは個人での利用が中心で、業務での利用はいま推進しているところ。今日の話も、その推進の中で出てきた要件への対応。
登壇するのは初めての経験なので、お手柔らかに。
```

## 今日の流れ

:::{container} eyebrow
アジェンダ
:::

:::{container} agenda
1. 背景：外部通信禁止の要件と、案件混在の防止
2. Copilot Chatでは足りなかった
3. Copilot CLIをWSL2に閉じ込める
4. 運用に落とす
5. まとめ：多層防御の一層と、残る制約
:::

```{revealjs-notes}
今日の流れ。背景、最初に試したCopilot Chatで足りなかったこと、本題のWSL2への閉じ込め、運用への落とし込み、最後に残る制約の順に話す。3章が中心。
```

```{include} chapters/01-background.md
```

```{include} chapters/02-copilot-chat.md
```

```{include} chapters/03-confinement.md
```

```{include} chapters/04-operation.md
```

```{include} chapters/05-summary.md
```
