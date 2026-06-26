<div align="center">

<img src="assets/logo-mark.png" width="76" alt="Astralune" />

# astra-makeover

### *一张房间照进去，一张翻新 listing 出来，一分钟。*

![License](https://img.shields.io/badge/License-Source%20Available-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-green)
![Agent Skill](https://img.shields.io/badge/Agent%20Skill-Portable-yellow)
![Engine](https://img.shields.io/badge/OpenAI-gpt--image--2-black)

**[English](README.md)  ·  [中文](README_CN.md)**

</div>

<br>

<div align="center">

<img src="assets/demo-board.png" width="560" alt="装修分析板示例" />

<sub>*一张房间照 + 一份简短简报 → 这一整张板，一次生成。*</sub>

</div>

<br>

<div align="center">

**listing 照片显旧，买家一划就过。**
**请设计师出效果图，几百刀、好几天。**
**开放看房前的今天，你就得让买家看到「翻新后的样子」。**

<br>

[**快速开始**](#-快速开始) · [**你得到什么**](#-你得到什么) · [**怎么用**](#-怎么用) · [**适用场景**](#️-适用场景) · [**配置**](#️-配置)

</div>

<br>

---

## ✨ 为什么有它

以前要让买家看到房子「翻新后能变成什么样」，得请室内设计师或 PS 师傅出图——一个房间几百刀、
等上几天，还要来回改。

装上 **astra-makeover**，扔一张房间照、答一份简短的设计简报，一分钟后就有一张完整的**装修分析
板**：翻新渲染、前后对比、带标注的材料清单、三档预算、ROI 评估，合成一张干净的图，直接拿去给客户看。

它跑在你已经在用的 agent 里（Claude Code、Codex 等），一个 API key 就能自配置，出的板**不带任何
品牌**，你拿去当自己的展示。

## 🎯 你得到什么

每个房间一张图，含：

| 板块 | 内容 |
|------|------|
| 🏠 **实景渲染** | 同一个房间，按选定风格翻新——墙/窗/布局不动 |
| 🔁 **前后对比** | 原始照片，诚实并排对比 |
| 🔖 **标注渲染** | 每处升级带编号标注——材料、饰面、预估装机价 |
| 🎨 **材料板** | 地板 / 台面 / 橱柜 / 龙头 / 灯光 的整套搭配 |
| 💰 **预算（低/中/高）** | 材料 + 人工 + 预备金，含 GST |
| ⭐ **ROI 与优先级** | 买家吸引力星评 + 最高 ROI 到最低的取舍顺序 |
| ✅ **建议** | 策略、工期、总体评分 |

> **分钟级，不是按天；几分钱，不是几百刀。** 结构是真的——只翻新饰面，不挪你的墙和窗。

## ⚡ 快速开始

```bash
# 1. 一次性：配置 OpenAI API key（有引导）
python3 scripts/makeover.py --setup

# 2. 出板（先 dry-run 不花钱，确认后加 --confirm）
python3 scripts/makeover.py \
  --ref kitchen.jpg \
  --brief Style="Modern Australian" --brief Objective=Resale --brief Budget='$20-40k' \
  --brief Priority="Best Resale" \
  --property "12 King St" --room kitchen --confirm
```

或者直接跟你的 agent 说：**“给这个厨房出张转售翻新图”** —— 它会帮你跑完整个引导问答。

## 🔧 怎么用

```
  📷 给图  →  🔍 空间分析  →  📝 设计简报  →  🖼️  出一张板
```

1. **给图** —— 一个房间，一张或多张角度。
2. **空间分析** —— agent 读图。
3. **设计简报** —— 几个快问：风格、目标、预算、留什么、优先级。
4. **出一张板** —— 走 OpenAI gpt-image-2 生成，存到 `~/makeover-outputs/<房产>/`。

多房间？逐间跑。

## 🏘️ 适用场景

- **房产中介** —— 把陈旧的 listing 照变成「翻新潜力」板，用于推广和开放看房。
- **staging 公司** —— 实物布置前先给客户看最终效果。
- **flipper / 投资客** —— 买之前快速过一遍翻新预算和 ROI。
- **房东** —— 不动结构、提升租金的焕新预览。

## 🛠️ 配置

- **依赖：** Python 3.9+、`pip install openai`、一个 OpenAI API key。
- **Key：** 跑 `--setup`（有引导）——它会校验 key 并存到本地
  （`~/.config/astra-makeover/config.env`，chmod 600，绝不入库）。随时用 `--check-key` 复核。
- **成本：** 按张计费，一张板大约几分钱，从你自己的 OpenAI 账户出。

> **说明：** 生成永远走 OpenAI API 以保证质量。即使在自带生图的 agent 里，本技能也**故意只走
> API 路径**——它是对你真实房间的高质量 image-edit。

## 📄 许可

Astra Source Available License. 个人使用和学习免费，商用需单独授权。详见 [LICENSE](LICENSE)。

<br>

---

<div align="center">

<img src="assets/logo-mark.png" width="56" alt="Astralune" />

**展示潜力，拿下 listing。**

[![Website](https://img.shields.io/badge/astralune.ai-访问官网-111111?style=for-the-badge)](https://astralune.ai)

由 [**Astralune**](https://astralune.ai) 出品 · [github.com/Astralune-ai](https://github.com/Astralune-ai)

</div>
