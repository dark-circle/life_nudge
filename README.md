# Life Nudge

监听北京 AQI，当 AQI 在 `50` 阈值两侧发生变化时，通过 Bark 发送提醒。

判定规则：

- 本次 `< 50` 且上次 `> 50`：空气质量变好
- 本次 `> 50` 且上次 `< 50`：空气质量变差
- 等于 `50` 不触发提醒

## 配置

可以在项目根目录创建 `.env`：

```bash
WAQI_TOKEN="your-waqi-token"
BARK_URL="https://api.day.app/your-bark-key"
```

也可以通过终端环境变量配置：

```bash
export WAQI_TOKEN="your-waqi-token"
export BARK_URL="https://api.day.app/your-bark-key"
```

可选配置：

```bash
export AQI_CITY="beijing"
export AQI_CHECK_INTERVAL_SECONDS="600"
export AQI_STATE_FILE=".aqi_state.json"
```

## 运行

```bash
python -m life_nudge
```

如果使用可编辑安装：

```bash
python -m pip install -e .
life-nudge
```

## 单次检查

用于 crontab、launchd 或手动测试：

```bash
python -m life_nudge --once
```

## GitHub Actions

项目包含每小时运行一次的 GitHub Actions 配置：

```text
.github/workflows/aqi-monitor.yml
```

需要在 GitHub 仓库的 `Settings` -> `Secrets and variables` -> `Actions` 中添加：

- `WAQI_TOKEN`
- `BARK_URL`

Actions 使用 `.aqi_state.json` 缓存上一次 AQI 值。第一次运行没有历史值，只会保存状态，不会发送变化提醒。
