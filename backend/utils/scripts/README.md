# Feature Flag Management Scripts

This directory contains scripts to manage feature flags in the Suna AI Worker.

## Scripts

### 1. `enable_agent_triggers.py`

A simple script to enable the `agent_triggers` feature flag.

**Usage:**
```bash
cd backend
python utils/scripts/enable_agent_triggers.py
```

### 2. `manage_feature_flags.py`

A comprehensive script to manage all feature flags.

**Usage:**
```bash
cd backend

# List all feature flags
python utils/scripts/manage_feature_flags.py list

# Enable a specific flag
python utils/scripts/manage_feature_flags.py enable --flag agent_triggers --description "Enable agent triggers"

# Disable a specific flag
python utils/scripts/manage_feature_flags.py disable --flag agent_triggers

# Check status of a specific flag
python utils/scripts/manage_feature_flags.py check --flag agent_triggers

# Enable all common feature flags
python utils/scripts/manage_feature_flags.py enable-common
```

## Common Feature Flags

The `enable-common` action enables these commonly used feature flags:

- `agent_triggers` - Enable agent triggers functionality
- `custom_agents` - Enable custom agent creation and management
- `triggers_api` - Enable triggers API endpoints
- `workflows_api` - Enable workflows API endpoints
- `knowledge_base` - Enable knowledge base functionality
- `mcp_module` - Enable MCP (Model Context Protocol) module
- `templates_api` - Enable templates API
- `pipedream` - Enable Pipedream integration
- `credentials_api` - Enable credentials API
- `suna_default_agent` - Enable Suna default agent

## Troubleshooting

If you encounter the error "Agent triggers are not enabled", run:

```bash
cd backend
python utils/scripts/manage_feature_flags.py enable --flag agent_triggers
```

Or to enable all common flags:

```bash
cd backend
python utils/scripts/manage_feature_flags.py enable-common
```

## How Feature Flags Work

Feature flags are stored in Redis and control access to various features in the application. When a feature flag is disabled, the corresponding API endpoints return a 403 error with a message indicating the feature is not enabled.

To enable a feature, the flag must be set to `true` in Redis using the flag management system.
