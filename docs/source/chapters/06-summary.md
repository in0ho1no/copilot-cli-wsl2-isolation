## まとめ

:::{container} rows compact
要件
: 外部通信の禁止と案件間の情報分離を、同時に満たす

判断
: VS Code上の対策では強制しきれず、Copilot CLI＋WSL2を選んだ

構成
: 案件ごとの専用ディストリ、ランチャー、サンドボックスの3層

運用
: 技術は誤操作の防止に使い、意図的な回避はルールで扱う
:::

:::{container} callout
今後：WSL2上の実機検証を進める。MXCはClaude Codeが対応した時点で再検討する
:::
