# 项目特定优化知识 - Quant Trading Project

> **标记：项目特定优化知识** - 这是针对 quant_trading 项目的优化建议和最佳实践，不是通用技能

---

# Quant Trading Project - Optimization Review (2026-03-25)

## Critical Issues Identified

### 1. Strategy Code Incomplete & Contains Errors
- **`trend_following.py`**:
  - References non-existent `ArrayTool` (not in VeighNa)
  - `self.get_bars()` undefined
  - `self.strategy_engine.bars` may not exist
  - Manual `bar` update logic in `on_tick` is complex and error-prone
- **Recommendation**: Use VeighNa's `BarGenerator` to convert ticks to K-line; inherit from `CtaTemplate` correctly; use `self.get_array` for historical data; implement stop-loss with `self.pos` and `self.entry_price`

### 2. Risk Management Module Not Implemented
- **`risk_config.py`** is only configuration documentation (Markdown in `.py` file), no actual code
- **Recommendation**: Implement risk manager inheriting from `vnpy_riskmanager` base class; register in `MainEngine`; add real-time checks for max position, daily loss, etc.

### 3. Data Manager Not Fully Integrated
- **`data_manager.py`** only provides CSV import/export, no VeighNa database layer integration
- **Recommendation**: Use `vnpy_datamanager`'s `DatabaseManager` interface; implement data subscription and incremental updates; use Parquet/HDF5 for historical data

### 4. Configuration Management Chaos
- **`setting.py`** directly modifies global `SETTINGS`
- **`risk_config.py`** is Markdown (misleading `.py` extension)
- **Recommendation**: Use YAML/JSON config files with `pydantic`/`dataclass` for type validation; separate `default.yaml`, `production.yaml`, `development.yaml`

### 5. Hardcoded Sensitive Information
- **`setting.py`** contains hardcoded passwords
- **Recommendation**: Use environment variables or encrypted `.env` files; add `*.env`, `config/local.yaml` to `.gitignore`

### 6. Missing Error Handling & Logging
- **`data_manager.py`** doesn't handle file format errors, empty data
- **`run.py`** doesn't catch startup exceptions
- **Recommendation**: Use `try-except` for file reading, DB connections; add global exception catching in `run.py`; use `logging` module instead of `print`

### 7. Missing Unit Tests
- Only empty `tests/test_strategy.py` example
- **Recommendation**: Write unit tests for data manager, risk manager, strategies using `pytest`; set up CI for automated testing

## Architecture Recommendations

### 1.1 Unified Configuration Management
- Centralize config in YAML/JSON files
- Use `pydantic`/`dataclass` for type validation
- Environment variable overrides

### 1.2 Project Structure
```
src/
  engine/ # event engine, main engine
  gateway/ # interface wrappers
  strategies/ # CTA, combo, options
  data/ # data management
  risk/ # risk management
  utils/ # utility functions
  config/ # config loading
  tests/
    unit/
    integration/
  scripts/ # run scripts
```

### 1.3 Dependency Version Locking
- Use exact versions in `requirements.txt`
- Or use `poetry`/`pipenv`
- Keep VeighNa modules in sync with official versions

## Security Recommendations

- Use environment variables for sensitive info
- Filter sensitive fields from logs
- Set restrictive file permissions for log files

## Documentation & Testing

- Keep docs and code in sync
- Use Sphinx for API docs
- Write comprehensive unit tests
- Set up CI for automated testing

## Priority Actions

1. **Fix `trend_following.py`** - complete and correct strategy implementation
2. **Implement risk management module** - actual code, not just docs
3. **Integrate data manager** - connect to VeighNa DB layer
4. **Fix configuration management** - use proper config files, remove hardcoded secrets
5. **Add error handling** - comprehensive exception handling
6. **Write unit tests** - cover core modules
7. **Update documentation** - ensure docs match actual code

## Reference

- VeighNa official examples: `vnpy_example`
- Best practices: follow VeighNa framework conventions
