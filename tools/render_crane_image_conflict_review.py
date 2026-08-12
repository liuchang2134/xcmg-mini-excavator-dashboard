import html
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "crane-image-conflicts.json"
OUTPUT = ROOT / "crane-image-conflict-review.html"


def image_size(relative_path: str) -> tuple[int, int]:
    with Image.open(ROOT / relative_path) as image:
        return image.size


def render_group(index: int, group: dict) -> str:
    canonical = group["files"][0]
    width, height = image_size(canonical)
    files = "".join(
        f"<li><code>{html.escape(path)}</code></li>" for path in group["files"]
    )
    unique_candidates = []
    for usage in group["usages"]:
        candidate = usage["caption"]
        if candidate not in unique_candidates:
            unique_candidates.append(candidate)
    choices = "".join(
        (
            f'<label class="choice"><input type="radio" name="group-{index}" '
            f'value="{html.escape(candidate, quote=True)}">'
            f'<span><b>候选 {choice_index}</b>{html.escape(candidate)}</span></label>'
        )
        for choice_index, candidate in enumerate(unique_candidates, 1)
    )
    usages = "".join(
        (
            "<tr>"
            f"<td>{html.escape(usage['page'])}</td>"
            f"<td>{html.escape(usage['caption'])}</td>"
            "</tr>"
        )
        for usage in group["usages"]
    )
    return f"""
    <section class="conflict" data-index="{index}">
      <header>
        <div><span class="number">{index:02d}</span><h2>图片归属冲突</h2></div>
        <code>{html.escape(group['hash'])}</code>
      </header>
      <div class="review-grid">
        <figure>
          <button type="button" class="image-button" aria-label="查看图片原尺寸">
            <img src="{html.escape(canonical)}" alt="第 {index} 组待裁决图片">
          </button>
          <figcaption>原图 {width} × {height}px</figcaption>
        </figure>
        <div class="decision">
          <h3>请选择正确说明</h3>
          <div class="choices">{choices}
            <label class="choice reuse"><input type="radio" name="group-{index}" value="SOURCE_REUSE"><span><b>源材料复用</b>保留多处展示，并标明各自来源幻灯片</span></label>
            <label class="choice unresolved"><input type="radio" name="group-{index}" value="UNRESOLVED"><span><b>暂无法判断</b>保留待核验状态，不进入后续去重</span></label>
          </div>
        </div>
      </div>
      <details>
        <summary>查看文件与当前使用位置</summary>
        <div class="evidence"><ul>{files}</ul><table><thead><tr><th>页面</th><th>当前说明</th></tr></thead><tbody>{usages}</tbody></table></div>
      </details>
    </section>"""


def main() -> None:
    groups = json.loads(SOURCE.read_text(encoding="utf-8"))
    content = "".join(render_group(index, group) for index, group in enumerate(groups, 1))
    initial_preview = html.escape(groups[0]["files"][0])
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>起重机图片归属人工裁决</title>
  <style>
    :root{{--blue:#004d8f;--blue-2:#0066b3;--yellow:#f5b400;--ink:#092b4c;--muted:#52697f;--line:#c7d7e6;--soft:#f3f7fa;--white:#fff}}
    *{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:#edf3f7;color:var(--ink);font-family:Arial,"Microsoft YaHei",sans-serif}}
    .topbar{{position:sticky;top:0;z-index:5;display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:16px;align-items:center;padding:16px 28px;background:#062f55;color:#fff;border-bottom:4px solid var(--yellow)}}
    .topbar h1{{margin:0;font-size:22px}}.topbar p{{margin:4px 0 0;color:#d7e6f2;font-size:13px}}.progress{{font-weight:700;white-space:nowrap}}button{{font:inherit}}
    .toolbar{{display:flex;gap:8px;align-items:center}}.copy,.filter{{border:1px solid #fff;background:#fff;color:#073e6e;padding:9px 14px;font-weight:700;cursor:pointer}}.copy:hover,.filter:hover,.filter.active{{background:var(--yellow)}}
    main{{width:min(1500px,calc(100% - 32px));margin:24px auto 64px;display:grid;gap:18px}}
    .conflict{{background:var(--white);border:1px solid var(--line);border-top:3px solid var(--blue-2)}}
    .conflict>header{{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:14px 18px;border-bottom:1px solid var(--line)}}
    .conflict>header>div{{display:flex;align-items:center;gap:12px}}.conflict h2{{margin:0;font-size:18px}}.number{{display:grid;place-items:center;width:40px;height:30px;background:var(--blue);color:#fff;font-weight:800}}
    code{{font-family:Consolas,monospace;font-size:12px;overflow-wrap:anywhere}}.review-grid{{display:grid;grid-template-columns:minmax(360px,46%) minmax(0,1fr);gap:20px;padding:18px}}
    figure{{margin:0;min-width:0}}.image-button{{display:block;width:100%;padding:0;border:1px solid var(--line);background:#e8eef3;cursor:zoom-in}}
    figure img{{display:block;width:100%;max-height:520px;object-fit:contain;background:#fff}}figcaption{{padding:8px 10px;color:var(--muted);font-size:12px;border:1px solid var(--line);border-top:0}}
    .decision h3{{margin:0 0 12px;font-size:16px}}.choices{{display:grid;gap:8px}}.choice{{display:grid;grid-template-columns:20px minmax(0,1fr);gap:10px;align-items:start;padding:12px;border:1px solid var(--line);background:var(--soft);cursor:pointer}}
    .choice:hover{{border-color:var(--blue-2)}}.choice:has(input:checked){{border-color:var(--yellow);box-shadow:inset 4px 0 var(--yellow);background:#fff9df}}.choice input{{margin-top:3px}}.choice span{{line-height:1.55}}.choice b{{display:block;color:var(--blue);font-size:12px}}
    .reuse{{background:#eef8f4}}.unresolved{{background:#fff4f2}}details{{border-top:1px solid var(--line)}}summary{{padding:12px 18px;font-weight:700;cursor:pointer}}.evidence{{padding:0 18px 18px;overflow:auto}}ul{{margin:0 0 12px;padding-left:20px}}table{{width:100%;border-collapse:collapse;font-size:13px}}th,td{{padding:8px;border:1px solid var(--line);text-align:left;vertical-align:top}}th{{background:var(--blue);color:#fff}}
    dialog{{width:min(94vw,1400px);max-height:94vh;border:0;padding:12px;background:#fff}}dialog::backdrop{{background:rgba(0,25,48,.86)}}dialog img{{display:block;max-width:100%;max-height:88vh;margin:auto;object-fit:contain}}dialog button{{position:absolute;right:16px;top:16px;width:40px;height:40px;border:0;background:#062f55;color:#fff;font-size:24px;cursor:pointer}}
    .conflict.resolved{{border-top-color:#1f8b62}}.conflict.hidden-by-filter{{display:none}}
    @media(max-width:800px){{.topbar{{grid-template-columns:1fr auto;padding:12px 16px}}.topbar p{{display:none}}.toolbar{{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr}}main{{width:calc(100% - 20px);margin-top:12px}}.review-grid{{grid-template-columns:1fr;padding:12px}}.conflict>header{{align-items:flex-start;flex-direction:column;gap:8px}}}}
  </style>
</head>
<body>
  <header class="topbar"><div><h1>起重机图片归属人工裁决</h1><p>选择正确归属，或明确标记源材料复用。选择结果自动保存在本机浏览器。</p></div><div class="progress">已裁决 <span id="done">0</span> / {len(groups)}</div><div class="toolbar"><button class="filter" id="filter">只看未裁决</button><button class="copy" id="copy">复制 / 下载结果</button></div></header>
  <main>{content}</main>
  <dialog id="viewer"><button type="button" aria-label="关闭">×</button><img src="{initial_preview}" alt="原始图片预览"></dialog>
  <script>
    const total={len(groups)},storageKey='xcmg-crane-image-decisions-v1',done=document.querySelector('#done'),viewer=document.querySelector('#viewer'),viewerImage=viewer.querySelector('img'),filterButton=document.querySelector('#filter');
    function decisions(){{return [...document.querySelectorAll('.conflict')].map(section=>{{const selected=section.querySelector('input:checked');return {{group:Number(section.dataset.index),decision:selected?selected.value:null}}}})}}
    function save(){{localStorage.setItem(storageKey,JSON.stringify(decisions()))}}
    function refresh(){{const values=decisions(),complete=values.filter(item=>item.decision).length;done.textContent=complete;document.querySelectorAll('.conflict').forEach(section=>{{const resolved=Boolean(section.querySelector('input:checked'));section.classList.toggle('resolved',resolved);section.classList.toggle('hidden-by-filter',filterButton.classList.contains('active')&&resolved)}});save()}}
    try{{const stored=JSON.parse(localStorage.getItem(storageKey)||'[]');stored.forEach(item=>{{if(!item.decision)return;const input=[...document.querySelectorAll(`input[name="group-${{item.group}}"]`)].find(candidate=>candidate.value===item.decision);if(input)input.checked=true}})}}catch(error){{console.warn('Unable to restore decisions',error)}}
    document.addEventListener('change',refresh);filterButton.addEventListener('click',()=>{{filterButton.classList.toggle('active');filterButton.textContent=filterButton.classList.contains('active')?'显示全部':'只看未裁决';refresh()}});
    document.querySelectorAll('.image-button').forEach(button=>button.addEventListener('click',()=>{{viewerImage.src=button.querySelector('img').src;viewer.showModal()}}));
    viewer.querySelector('button').addEventListener('click',()=>viewer.close());viewer.addEventListener('click',event=>{{if(event.target===viewer)viewer.close()}});
    document.querySelector('#copy').addEventListener('click',async event=>{{const result=JSON.stringify(decisions(),null,2);await navigator.clipboard.writeText(result);const blob=new Blob([result],{{type:'application/json'}}),link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='crane-image-decisions.json';link.click();URL.revokeObjectURL(link.href);event.currentTarget.textContent='已复制并下载';setTimeout(()=>event.currentTarget.textContent='复制 / 下载结果',1600)}});refresh();
  </script>
</body>
</html>"""
    OUTPUT.write_text(page, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT} with {len(groups)} groups")


if __name__ == "__main__":
    main()
