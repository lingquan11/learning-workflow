# learning-workflow

三个学习仓库（[cpp-matmul-performance](https://github.com/lingquan11/cpp-matmul-performance)、[AI-Infra-Learning](https://github.com/lingquan11/AI-Infra-Learning)、[IC-Design-Learning](https://github.com/lingquan11/IC-Design-Learning)）共用的工作流：规则、提示词、模板和进度脚本的**唯一来源**。

## 三栏学习
| 栏 | 谁 | 怎么做 |
|---|---|---|
| 阅读 `Rxx` | 我自己 | 读逻辑连贯的长文，不和 AI 对话；读完对 Muse 说"读完 R03" |
| 编程 `Pxx` | GPT | "开始写代码" … "结束"：带我写 `[me]` 代码，跑测试，归档 |
| 动手 `Hxx` | Muse | "准备环境" / "做 H02"：装环境、跑实验与工具、整理结果，归档；也负责记录阅读 |

## 同步
```bash
python sync.py ../AI-Infra-Learning
python sync.py ../IC-Design-Learning
```
同步会写入学习仓库的 `start/WORKFLOW.lock`；学习仓库的 CI 运行 `progress.py --check`，共享文件被直接修改时会变红。**要改共享文件，只改这里，再重新同步。**

## 内容
| 文件 | 同步到 | 作用 |
|---|---|---|
| `AGENTS.md` | 仓库根目录 | GPT 和 Muse 的分工与触发词 |
| `RULES.md` | `start/RULES.md` | 全部规则（一页） |
| `prompts/` | `start/prompts/` | coding-tutor、coding-archiver（GPT）；hands-on（Muse） |
| `templates/` | `start/templates/` | 战役（三张表）、任务卡、STATE、日志、README、实验 README |
| `scripts/progress.py` | `start/scripts/` | 首页三栏进度条与成果表；检查行数、链接、状态一致性、共享文件版本 |
