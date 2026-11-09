"""Markdown とキャラクターを使うスライドの Sphinx 設定。

sphinx-revealjs-mascot の雛形 (.agents/skills/markdown-to-slides/assets/starter) を基にしている。
"""

project = 'WSL2を用いたCopilot CLI環境の分離'
extensions = ['myst_parser', 'sphinx_revealjs_mascot']
root_doc = 'index'
source_suffix = {'.md': 'markdown'}
language = 'ja'
# chapters/ は index.md から include するため、単独の文書としてはビルドしない
exclude_patterns = ['_build', 'chapters']

# colon_fence: ::: による入れ子の container、deflist: ラベルと説明の行、attrs_inline: 表中の記号の色分け
myst_enable_extensions = ['colon_fence', 'deflist', 'attrs_inline']

revealjs_static_path = ['_static']
revealjs_css_files = ['slides.css']
# 章ラベルを全章のナビに置き換える (章名は Markdown の eyebrow から取る)
revealjs_js_files = ['chapter-nav.js']
revealjs_style_theme = 'white'
revealjs_script_conf = {
    'width': 1280,
    'height': 720,
    'margin': 0.06,
    'center': False,
    'transition': 'none',
    'hash': True,
}
revealjs_script_plugins = [
    {'name': 'RevealNotes', 'src': 'revealjs/plugin/notes/notes.js'},
]

# オンライン発表のため、本文は全幅を使いキャラクターとの重なりを許容する (slides.css 冒頭を参照)
revealjs_mascot_position = 'bottom-right'
revealjs_mascot_width = 12
