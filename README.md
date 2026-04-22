# Life Nudge

监听北京 AQI，当 AQI 在 `50` 阈值两侧发生变化时，通过 Bark 发送提醒。

判定规则：

- 本次 `< 50` 且上次 `> 50`：空气质量变好
- 本次 `> 50` 且上次 `< 50`：空气质量变差
- 等于 `50` 不触发提醒

## 配置

必须配置：

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

