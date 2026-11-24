# learning-workflow

三个学习仓库（[cpp-matmul-performance](https://github.com/lingquan11/cpp-matmul-performance)、[AI-Infra-Learning](https://github.com/lingquan11/AI-Infra-Learning)、[IC-Design-Learning](https://github.com/lingquan11/IC-Design-Learning)）共用的工作流：规则、提示词、模板和进度脚本的**唯一来源**。

## 同步
```bash
python sync.py ../AI-Infra-Learning          # 单线：GPT/Codex 导师 + Gemini 考官 + Muse 环境
python sync.py ../IC-Design-Learning --dual  # 双线：理论 GPT / 实践 Muse / Gemini 考官
```
同步会写入学习仓库的 `start/WORKFLOW.lock`。学习仓库的 CI 运行 `progress.py --check`，共享文件被直接修改时会变红。**要改共享文件，只改这里，再重新同步。**

## 内容
| 文件 | 同步到 | 作用 |
|---|---|---|
| `AGENTS.md` / `AGENTS-dual.md` | 仓库根目录 `AGENTS.md` | 三位 AI 的分工与触发词 |
| `GEMINI.md` | 仓库根目录 | 让 Gemini 找到考官说明 |
| `RULES.md` | `start/RULES.md` | 全部规则（一页） |
| `prompts/` | `start/prompts/` | tutor、archiver（单线）；examiner（Gemini）；setup（Muse） |
| `prompts-dual/` | `start/prompts/` | theory-tutor、theory-archiver（GPT）；practice-tutor、practice-archiver（Muse） |
| `templates/` | `start/templates/` | 战役、任务卡、STATE、日志、README、实验 README |
| `scripts/progress.py` | `start/scripts/` | 首页进度条与成果表；检查行数、链接、状态一致性、共享文件版本 |

## 仓库骨架
```
README.md   学习进度 + 对谁说什么 + 学习过程 + 学习成果（≤ 40 行）
AGENTS.md   GEMINI.md
start/      STATE、ROADMAP、RULES、IDEAS、campaigns/、prompts/、templates/、scripts/、WORKFLOW.lock
journey/    README（时间线）、log、notes、reviews（双线：theory/、practice/）、archive/
results/    README（结论表）、代码、experiments/
```
