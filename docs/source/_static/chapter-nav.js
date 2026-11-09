// 各スライドの章ラベル（eyebrow）を、全章の番号を並べたナビに置き換える。
// 章名は「NN 章名」と書かれた最初の eyebrow から取るため、章名を変えるときは Markdown 側だけを直せばよい。
// 番号で始まらない eyebrow（表紙・自己紹介・アジェンダ）は章に属さないものとして、そのまま残す。
(function () {
  'use strict';

  const LABEL_PATTERN = /^(\d{2})\s+(.+)$/;

  function readLabel(eyebrow) {
    const match = eyebrow.textContent.trim().match(LABEL_PATTERN);
    return match ? { number: match[1], name: match[2] } : null;
  }

  function buildNav(chapters, current) {
    const nav = document.createElement('p');
    nav.className = 'chapter-nav';
    chapters.forEach(function (chapter, index) {
      if (index > 0) {
        const sep = document.createElement('span');
        sep.className = 'sep';
        sep.textContent = '-';
        nav.appendChild(sep);
      }
      const item = document.createElement('span');
      item.className = 'ch';
      if (chapter.number === current) {
        item.classList.add('current');
        item.textContent = chapter.number + ' ' + chapter.name;
      } else {
        item.textContent = chapter.number;
      }
      nav.appendChild(item);
    });
    return nav;
  }

  function render() {
    const eyebrows = Array.from(document.querySelectorAll('.reveal .slides section > .eyebrow'));
    const chapters = [];
    const seen = new Set();
    eyebrows.forEach(function (eyebrow) {
      const label = readLabel(eyebrow);
      if (label && !seen.has(label.number)) {
        seen.add(label.number);
        chapters.push(label);
      }
    });
    chapters.sort(function (a, b) {
      return a.number.localeCompare(b.number);
    });

    eyebrows.forEach(function (eyebrow) {
      const label = readLabel(eyebrow);
      if (!label) {
        return;
      }
      eyebrow.replaceChildren(buildNav(chapters, label.number));
      eyebrow.classList.add('has-chapter-nav');
    });
  }

  // 読み込み順が Reveal の初期化の前後どちらでも動くよう、DOM の構築完了を待ってから一度だけ実行する
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render);
  } else {
    render();
  }
})();
