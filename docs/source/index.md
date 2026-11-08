# sphinx-revealjs-mascot サンプル

Markdown で書いたスライドにキャラクターを常駐させる例です。

## スライドの基本

```{mascot}
:action: jump
```

- `##` 見出しごとに1枚のスライドになります
- 見出し直後の `mascot` でキャラクターの動きを指定します
- M キーでキャラクターの表示・非表示を切り替えます

```{revealjs-notes}
発表者ノートです。S キーで開くスピーカービューに表示されます。
```

## 段階表示とリアクション

```{mascot-fragment}
:action: wink

- 1つ目のブロックで表示する要点
- 同じタイミングで表示する要点
```

```{mascot-fragment}
:action: surprise

続けて表示する内容です。
```

## 表示位置を変える

```{mascot}
:action: idle
:position: bottom-left
```

````{container} mascot-left
キャラクターを左下へ移したスライドです。本文は CSS で右へ寄せています。

| 指定 | 例 |
| --- | --- |
| 定型位置 | `bottom-left` |
| 座標 | `70%, 60%` |
````

## まとめ

位置を指定しないスライドでは `conf.py` の位置 (右下) に戻ります。
