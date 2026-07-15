# 小身体原型 · Builder 契约（所有 screen builder 必读且严格遵守）

你在为「小身体」（原 Ego）品牌焕新原型建一个/几个 iPhone 屏。所有屏拼进一个统一画廊 `index.html`，**UI 必须与真机 App 一致、且各屏之间一致**。一致性靠这份契约强制。**违反契约 = 返工**。

## 0. 你的产出格式（最重要）

只产出一个或多个 `<article class="device" ...>…</article>` 块，**别的什么都不要**（不要 `<html>/<head>/<style>/<script>`，不要 markdown 代码围栏）。iPhone 外壳、状态栏、灵动岛、底部 tabbar、AI 悬浮键、home indicator、标题 caption **全部由主文件 JS 自动注入** —— 你**只写屏内可滚动内容**。

```html
<article class="device"
         data-caption="屏名 · 模块"        <!-- caption：· 前是主标题，后是小注 -->
         data-nav="none"                    <!-- 二级页导航栏：填标题字符串；开头加 ← 表示带返回箭头，如 "← 用药疗程"；一级页/全屏页填 none -->
         data-tab="none"                    <!-- 底部 tabbar 高亮：today | trends | events | none。仅今日/趋势/事件三个一级页有 tabbar -->
         data-fab="false"                   <!-- AI 悬浮键：true 显示 / false 隐藏。有 tabbar 时默认显示；二级页/表单/对话页填 false -->
         data-theme="light">                <!-- light 普通 / brand 全靛蓝底(状态栏文字转白) -->
  <div class="screen-pad fade">
     …你的屏内容…
  </div>
</article>
```

- `.screen-pad` = `padding:8px 18px 40px`。若屏顶是通栏 hero/图片，可不用 screen-pad 改自定义 padding，但**必须给顶部留 `padding-top` ≥ 8px**（状态栏 44px 已由 .screen 的 padding-top 处理；有 data-nav 时再 +44）。
- 需要底部固定操作条（如「下一步」）时，用 `position:absolute;left:0;right:0;bottom:0` 放在 `<article>` 内、`.screen-pad` 外。

## 1. 写到文件

把你负责的所有 article 写进指定的 `_frag/<名字>.html`（用 Write 工具）。文件里就是纯 article 块序列，无其它包裹。

## 2. 颜色 —— 只用这些 token（取自真机 EgoColor.swift）

内联 style 用 hex；能用 Tailwind class 也行（`text-ego-ink` / `bg-ego-card` 等，已配好）。**禁止臆造其它颜色**。

| 角色 | hex | 角色 | hex |
|---|---|---|---|
| 页面底 bg | `#F6F6F6` | 品牌靛蓝 primary | `#3C4FC1` |
| 卡片 card | `#FFFFFF` | 次强调 primary2 | `#586298` |
| 主文字 ink | `#2F3337` | 品牌图标蓝 brand | `#3E46CE` |
| 次文字 ink2 | `#59606B` | 成功/达标 green | `#4BC87E` |
| 三级文字 ink3 | `#7C838D` | 危险/删除 danger | `#E85D5D` |
| 说明 mute | `#9AA09F` | 警示 warn | `#E88A3C` |
| 占位 hint | `#C0C4CC` | 金/VIP gold | `#FFB300` |
| 次级填充 fill | `#EFEFEF` | 图表线 line | `#5B8DEF` |
| 分隔线 divider | `#EAEAEA`(或行内 `#F0F0F0`) | 边框 border | `#C9CDD2` |

类别色（图表/指标图标）：`red #F06B6B` `orange #F5A623` `teal #22BEC5` `green #4BC87E` `pink #EC6A8B` `purple #A88DE8`。
**指标图标固定配色**：HRV/心率→red、睡眠→orange、运动→teal、静息心率/电量→green、压力→red。
**偏离方向色**：偏高↑→orange `#F5A623`，偏低↓→red `#F06B6B`，持平→mute `#9AA09F`。数字高亮（一句话状态里）→teal `#22BEC5`。

## 3. 图标 —— 用共享 sprite `<svg><use href="#id"/></svg>`

可用 id（都在主文件里）：
`xst-mark`(白 logo) `xst-icon`(带底图标) `i-chevron-left` `i-chevron` `i-chevron-down` `i-bell` `i-calendar` `i-close` `i-check` `i-plus` `i-search` `i-gear` `i-mic` `i-share` `i-edit` `i-camera` `i-shield` `i-lock` `i-arrow-up` `i-arrow-down` `i-file` `i-chart` `i-heart` `i-moon` `i-run` `i-bolt` `i-battery` `i-pill` `i-drop` `i-wave` `i-sparkle` `i-lungs` `i-user` `i-doctor` `i-flame`

用法：`<svg style="width:20px;height:20px"><use href="#i-bell"/></svg>`，颜色由父级 `color` 决定。缺图标时可内联一个同风格 SVG（线性 stroke≈1.8 圆角 / 或填充），但优先用 sprite。**禁止 `<img>` / 外链图片 / emoji 当图标**（emoji 仅可做点缀）。

## 4. 组件配方（照抄，保证跨屏一致）

**卡片**
```html
<div class="bg-white egoshadow" style="border-radius:16px;padding:16px;">…</div>
```
**分区小标题**
```html
<div style="font-size:13px;font-weight:600;color:#9AA09F;margin:22px 4px 10px;">分区标题</div>
```
**设置/列表行**（多行放进一个圆角白卡容器，行间 `border-bottom:1px solid #F0F0F0`，末行无边框）
```html
<div style="display:flex;align-items:center;gap:12px;padding:14px 16px;">
  <div style="width:32px;height:32px;border-radius:9px;background:rgba(60,79,193,.1);color:#3C4FC1;display:flex;align-items:center;justify-content:center;"><svg style="width:18px;height:18px"><use href="#i-shield"/></svg></div>
  <div style="flex:1;font-size:15px;color:#2F3337;">行标题</div>
  <div style="font-size:13px;color:#9AA09F;">右值</div>
  <svg style="width:18px;height:18px;color:#C0C4CC"><use href="#i-chevron"/></svg>
</div>
```
**圆形图标徽章**（icon badge）：`width/height:34px;border-radius:50%;background:rgba(R,G,B,.15);color:#类别色`，内嵌 19px sprite。
**chip / 标签**：`font-size:11px;font-weight:700;padding:3px 9px;border-radius:999px;background:rgba(60,79,193,.1);color:#3C4FC1`。偏离/状态 chip 换对应类别色 + 该色 12% 透明底。
**主按钮**：`height:50px;border-radius:999px;background:#3C4FC1;color:#fff;font-size:16px;font-weight:700;` flex 居中。**次按钮**：底 `#EFEFEF`、字 `#59606B`。
**头像**：`width/height:36px;border-radius:50%;background:linear-gradient(135deg,#8FA0F5,#3C4FC1);color:#fff` 内嵌 `#i-user`。
**分段控件（日/周/月）**：外层 `background:#EFEFEF;border-radius:12px;padding:3px;display:flex`，选中段 `background:#fff;border-radius:9px;box-shadow:0 1px 3px rgba(0,0,0,.08)`，未选文字 `#7C838D`。
**大数值**：`font-size:22~30px;font-weight:800;color:#2F3337`，单位小一号灰。

**迷你趋势图/折线**：用内联 `<svg viewBox="0 0 300 120">` 画 `<polyline fill=none stroke=#5B8DEF stroke-width=2>` + 可选 P10-P90 参考带 `<rect fill=#D0D0D0 opacity=.25>`。别引图表库。

## 5. 硬规则

1. 品牌名一律 **小身体**，**绝不出现 "Ego"**（AI 人格、欢迎语、logo 全用小身体；logo 用 `<use href="#xst-mark">` 白标或 `#xst-icon` 带底）。
2. 全部 **mock 演示数据**，要真实可信（HRV 52ms、睡眠 7h25m、"连续 3 天偏低"、日期 7月14日 等），不要 "示例/xxx/占位"。
3. **读真机源码**再建：按分配读对应 SwiftUI view，复刻它的**布局顺序、字段名、标签文案、卡片结构**。拿不准的用合理 mock 补足，但版式要像真机。
4. 圆角：卡片 16px、大区块 18px、按钮/chip 999px、图标徽章圆形 —— 对齐真机。
5. 中文正文用系统字体即可（已全局 PingFang SC）。
6. 只输出 article 块并 Write 到指定 frag 文件；返回一句话说明写了哪几屏。

## 6. 参照样板

主文件 `index.html` 里已有 3 个建好的样板屏，**打开读它们**学版式：
- 「今日首页」= 指标卡 grid + 一句话状态 + 顶栏（铃铛/日历/头像）的标准做法（data-tab="today"）
- 「启动页」= brand 全靛蓝屏做法（data-theme="brand"）
- 「桌面图标」= 自定义 wallpaper 屏做法

你的屏要和它们**像出自同一设计师之手**。
