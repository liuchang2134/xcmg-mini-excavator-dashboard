from __future__ import annotations

import html
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OWNERSHIP = ROOT / "data" / "crane-ppt-insights" / "image-ownership.json"
GALLERY_REVIEW = ROOT / "data" / "crane-ppt-insights" / "gallery-image-review.json"
SOURCE_MANIFEST = ROOT / "data" / "crane-ppt-insights" / "source.json"
OUTPUT = ROOT / "crane-image-conflict-review.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def image_size(relative_path: str) -> tuple[int, int]:
    with Image.open(ROOT / relative_path) as image:
        return image.size


def render_reuse_decision(index: int, decision: dict) -> str:
    asset = decision["source_assets"][0]
    width, height = image_size(asset)
    slides = "、".join(str(value) for value in decision["source_slides"])
    return f"""
    <article class="decision-card">
      <div class="decision-index">{index:02d}</div>
      <figure>
        <button type="button" class="image-button" data-full-src="{esc(asset)}" aria-label="放大查看第 {index} 组图片">
          <img src="{esc(asset)}" alt="{esc(decision['caption_zh'])}" loading="lazy">
        </button>
        <figcaption>{width} × {height}px</figcaption>
      </figure>
      <div class="decision-copy">
        <span class="status">已确认源资料复用</span>
        <h2>{esc(decision['caption_zh'])}</h2>
        <dl>
          <div><dt>PPT 原页</dt><dd>第 {slides} 页</dd></div>
          <div><dt>裁决理由</dt><dd>{esc(decision['reason_zh'])}</dd></div>
          <div><dt>处理结果</dt><dd>保留一份唯一图片资产；页面使用中采用中性说明并列明复用页码。</dd></div>
        </dl>
      </div>
    </article>"""


def render_gallery_review(item: dict) -> str:
    width, height = image_size(item["path"])
    return f"""
    <article class="gallery-review-item">
      <button type="button" class="image-button" data-full-src="{esc(item['path'])}" aria-label="放大查看已复核素材">
        <img src="{esc(item['path'])}" alt="{esc(item['asset_type_zh'])}" loading="lazy">
      </button>
      <div><span class="status keep">保留</span><h3>{esc(item['asset_type_zh'])}</h3>
      <p>{esc(item['reason_zh'])}</p><small>{width} × {height}px</small></div>
    </article>"""


def main() -> None:
    ownership = json.loads(OWNERSHIP.read_text(encoding="utf-8"))
    gallery_review = json.loads(GALLERY_REVIEW.read_text(encoding="utf-8"))
    source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    decision_cards = "".join(
        render_reuse_decision(index, decision)
        for index, decision in enumerate(ownership["decisions"], 1)
    )
    gallery_cards = "".join(render_gallery_review(item) for item in gallery_review["items"])
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>起重机图片自动裁决报告</title>
  <style>
    :root{{--blue:#075a9f;--navy:#06365f;--yellow:#f5b400;--green:#087d50;--ink:#082e50;--muted:#526b80;--line:#c8d7e5;--soft:#f2f6f9}}
    *{{box-sizing:border-box}}body{{margin:0;background:#edf3f7;color:var(--ink);font-family:Arial,"Microsoft YaHei",sans-serif}}button{{font:inherit}}
    header{{padding:24px max(20px,calc((100vw - 1480px)/2));background:var(--navy);color:#fff;border-bottom:4px solid var(--yellow)}}
    header h1{{margin:0 0 7px;font-size:26px}}header p{{margin:0;color:#d9e8f3;line-height:1.65}}
    main{{width:min(1480px,calc(100% - 28px));margin:20px auto 60px}}.summary{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1px solid var(--line);background:#fff}}
    .summary div{{padding:18px;border-right:1px solid var(--line)}}.summary div:last-child{{border:0}}.summary b{{display:block;color:var(--blue);font-size:30px}}.summary span{{font-size:12px;color:var(--muted)}}
    section{{margin-top:18px}}.section-head{{display:flex;align-items:end;justify-content:space-between;gap:16px;padding:0 0 9px;border-bottom:2px solid var(--blue)}}.section-head h2{{margin:0;font-size:20px}}.section-head p{{margin:0;color:var(--muted);font-size:12px}}
    .gallery-review-grid{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-top:12px}}.gallery-review-item{{display:grid;grid-template-rows:160px auto;border:1px solid var(--line);background:#fff}}
    .gallery-review-item>div{{padding:10px}}.gallery-review-item h3{{margin:7px 0 5px;font-size:14px}}.gallery-review-item p{{margin:0 0 7px;color:var(--muted);font-size:11px;line-height:1.55}}.gallery-review-item small{{color:var(--muted)}}
    .decision-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:12px}}.decision-card{{position:relative;display:grid;grid-template-columns:210px minmax(0,1fr);min-height:220px;border:1px solid var(--line);background:#fff}}
    .decision-index{{position:absolute;z-index:1;left:0;top:0;padding:7px 10px;background:var(--blue);color:#fff;font-size:12px;font-weight:900}}figure{{margin:0;min-width:0;border-right:1px solid var(--line);background:#f7fafc}}.image-button{{display:block;width:100%;height:182px;padding:0;border:0;background:#fff;cursor:zoom-in}}.image-button img{{display:block;width:100%;height:100%;object-fit:contain}}figcaption{{padding:8px;color:var(--muted);font-size:10px;text-align:center}}
    .decision-copy{{padding:14px}}.decision-copy h2{{margin:8px 0 10px;font-size:16px}}.status{{display:inline-block;padding:3px 7px;background:#e3f4ec;color:var(--green);font-size:10px;font-weight:900}}.status.keep{{background:#fff2c7;color:#775200}}
    dl{{display:grid;gap:7px;margin:0}}dl div{{display:grid;grid-template-columns:72px minmax(0,1fr);gap:8px}}dt{{color:var(--blue);font-size:11px;font-weight:900}}dd{{margin:0;color:#29475e;font-size:11px;line-height:1.55}}
    dialog{{width:min(96vw,1400px);height:min(92vh,980px);padding:45px 14px 14px;border:0;background:#fff}}dialog::backdrop{{background:rgba(3,22,39,.82)}}dialog img{{display:block;width:100%;height:100%;object-fit:contain}}dialog button{{position:absolute;right:10px;top:8px;width:32px;height:32px;border:1px solid #829bad;background:#fff;color:var(--ink);font-size:22px;cursor:pointer}}
    @media(max-width:900px){{.summary{{grid-template-columns:1fr 1fr}}.summary div:nth-child(2){{border-right:0}}.summary div:nth-child(-n+2){{border-bottom:1px solid var(--line)}}.gallery-review-grid,.decision-grid{{grid-template-columns:1fr}}.gallery-review-item{{grid-template-columns:150px 1fr;grid-template-rows:auto}}.decision-card{{grid-template-columns:130px minmax(0,1fr)}}.image-button{{height:150px}}}}
    @media(max-width:520px){{header{{padding:18px 14px}}main{{width:calc(100% - 16px)}}.summary b{{font-size:24px}}.gallery-review-item,.decision-card{{grid-template-columns:1fr}}figure{{border-right:0;border-bottom:1px solid var(--line)}}dl div{{grid-template-columns:1fr;gap:2px}}}}
  </style>
</head>
<body>
  <header><h1>起重机图片自动裁决报告</h1><p>依据源 PPT 中的图片二进制、出现页码和页面上下文自动判定；本报告为只读审计结果。</p></header>
  <main>
    <div class="summary"><div><b>{ownership['decision_count']}</b><span>已确认复用组</span></div><div><b>{source['deduplicated_groups']}</b><span>已去重组</span></div><div><b>{source['generated_assets']}</b><span>唯一图片资产</span></div><div><b>{gallery_review['reviewed_count']}</b><span>候选整页图已复核</span></div></div>
    <section><div class="section-head"><h2>候选整页截图复核</h2><p>5 张均为有效背景、工况、产品或型谱素材，未从证据库排除。</p></div><div class="gallery-review-grid">{gallery_cards}</div></section>
    <section><div class="section-head"><h2>源资料复用裁决</h2><p>完全相同的图片仅保留一份文件，页面说明不再强行绑定唯一机型或区域。</p></div><div class="decision-grid">{decision_cards}</div></section>
  </main>
  <dialog id="viewer"><button type="button" aria-label="关闭">×</button><img alt="原始图片预览"></dialog>
  <script>
    const viewer=document.querySelector('#viewer'),viewerImage=viewer.querySelector('img');
    document.querySelectorAll('.image-button').forEach(button=>button.addEventListener('click',()=>{{viewerImage.src=button.dataset.fullSrc;viewer.showModal()}}));
    viewer.querySelector('button').addEventListener('click',()=>viewer.close());viewer.addEventListener('click',event=>{{if(event.target===viewer)viewer.close()}});
  </script>
</body>
</html>"""
    OUTPUT.write_text(page, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT} with {ownership['decision_count']} adjudicated reuse groups")


if __name__ == "__main__":
    main()
