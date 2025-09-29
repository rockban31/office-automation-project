# AP Uptime Threshold Changes

## Updated Thresholds

### Previous Thresholds (Before Change):
- **Warning**: AP uptime > 30 days → "Consider rebooting AP for optimal performance"
- **Critical**: AP uptime > 60 days → "Reboot AP immediately to prevent performance degradation"

### New Thresholds (After Change):
- **Warning**: AP uptime > 90 days → "Consider checking and rebooting AP for optimal performance"
- **Critical**: AP uptime > 180 days → "Reboot AP immediately to prevent performance degradation"

## Code Changes Made

### File: `scripts/automated_network_troubleshooting.py`
**Lines ~608-639**: Updated the AP uptime check logic

```python
# Old thresholds
if uptime_days > 30:  # Warning
if uptime_days > 60:  # Critical

# New thresholds  
if uptime_days > 180:  # Critical (moved to first check)
if uptime_days > 90:   # Warning (moved to elif)
```

**Key Changes:**
1. **Increased Warning threshold**: 30 days → 90 days
2. **Increased Critical threshold**: 60 days → 180 days
3. **Updated recommendation text**: Added "checking and" to warning recommendation
4. **Reordered logic**: Critical check (180 days) now comes before warning check (90 days)

## Rationale for Changes

### More Realistic Thresholds
- **90 days**: Allows APs to run for 3 months before suggesting maintenance
- **180 days**: Flags APs that have been running for 6+ months as requiring immediate attention

### Reduced Alert Fatigue
- Previous 30-day threshold was too aggressive for enterprise environments
- New thresholds focus on truly problematic long-running APs

### Maintains Combined Signal Logic
- **Signal + Uptime check** remains at 14 days (unchanged)
- This catches the combination of poor signal AND moderate uptime for targeted reboots

## Impact on Output

### Warning Example (90+ days):
```
🟡 High AP uptime: 125.7 days (Finance-Floor-AP-01)
   💡 Suggested: Consider checking and rebooting AP for optimal performance
```

### Critical Example (180+ days):
```
🔴 Very high AP uptime: 198.5 days (Warehouse-AP-05)
   💡 Action: Reboot AP immediately to prevent performance degradation
```

## Updated Documentation
- `docs/ap-health-checks.md`: Updated thresholds and examples
- `docs/output-examples.md`: Updated sample outputs with new thresholds
- All examples now reflect 90/180 day thresholds instead of 30/60 days

## Testing
- Script compiles successfully with new thresholds
- Logic flow remains the same, only threshold values changed
- Combined signal + uptime logic (14 days) unchanged to catch performance issues early
