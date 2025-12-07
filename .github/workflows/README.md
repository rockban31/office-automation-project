# GitHub Actions Workflows

## Wireless Network Troubleshooting Workflow

This workflow automates wireless network troubleshooting using the Mist API integration.

### 🚀 Features

- **Manual Trigger Only**: On-demand reactive troubleshooting when issues occur
- **Flexible Inputs**: Configurable IP and MAC addresses for each run
- **Log Storage**: Saves detailed logs as GitHub artifacts (30-day retention)
- **Summary Reports**: Generates visual reports in GitHub Actions UI

### 📋 Setup Instructions

#### 1. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

**Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description | Required |
|------------|-------------|----------|
| `MIST_API_TOKEN` | Your Mist API token for authentication | ✅ Yes |
| `MIST_ORG_ID` | Your Mist Organization ID (optional - auto-detected if not provided) | ⚠️ Optional |


### 🎯 How to Run

#### Manual Trigger (On-Demand Reactive Troubleshooting)
Go to **Actions → Wireless Network Troubleshooting → Run workflow**

Fill in the inputs:
- **Client IP Address**: Target client IP (e.g., `192.168.1.100`)
- **Client MAC Address**: Target client MAC (e.g., `aa:bb:cc:dd:ee:ff`)
- **Hours Back**: Number of hours to check historical data (default: 24)
- **Enable Verbose Output**: Toggle for detailed debugging

Click **Run workflow** to start the troubleshooting process.

### 📊 Accessing Results

#### Logs and Artifacts
1. Go to **Actions** tab
2. Click on a workflow run
3. Scroll to **Artifacts** section
4. Download `troubleshooting-logs-{run_number}.zip`

#### Summary Report
- Available in the workflow run summary
- Shows configuration, output preview, and key metrics
- Located in the main workflow page

### 🔧 Customization

#### Change Python Version
Modify the Python version in the workflow:

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # Change to '3.9', '3.10', '3.12', etc.
```

#### Adjust Artifact Retention
Change retention period (1-90 days):

```yaml
- name: Upload troubleshooting logs
  uses: actions/upload-artifact@v4
  with:
    retention-days: 30  # Change to desired number of days
```

### 🔐 Security Notes

- **Never commit secrets**: API tokens are stored securely in GitHub Secrets
- **Read-only operations**: The workflow only performs read operations on Mist API
- **Limited scope**: Workflow runs in isolated environment with minimal permissions

### 🐛 Troubleshooting

#### Workflow fails with authentication error
- Verify `MIST_API_TOKEN` secret is set correctly
- Check token hasn't expired
- Ensure token has proper permissions

#### No logs in artifacts
- Check if the workflow completed (even partially)
- Logs are uploaded even if the troubleshooting step fails (using `if: always()`)

### 📚 Additional Resources

- [Main Project README](../../README.md)
- [Office Automation CLI Documentation](../../office_automation_cli.py)
- [Mist API Documentation](https://api.mist.com/api/v1/docs/Home)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

### 🎓 Example Output

```
======================================================================
MIST WIRELESS NETWORK TROUBLESHOOTING
======================================================================
🔍 [STEP 1] Gathering Client Association Status & Events...
✅ Client found: Soumya-s-M31 connected to AP PHOENIX-FF-AP10
   SSID: COLLEAGUE
   Client details: RSSI=-57, SNR=37, IP=10.21.9.247

🔍 [STEP 2] Checking Authentication and Authorization Failure Logs...
✅ No authentication/authorization issues detected

🔍 [STEP 3] Checking DNS/DHCP Lease Errors...
✅ No DNS/DHCP lease errors detected

🔍 [STEP 4] Analyzing Client Health Metrics...
✅ All health metrics within normal range

📁 Detailed logs saved to: logs/troubleshooting-20251207-120000.log
======================================================================
```

### 💡 Tips

1. **Keep MAC/IP handy**: Have client information ready when issues are reported
2. **Monitor retention**: Download important logs before the 30-day retention expires
3. **Use verbose mode**: Enable when you need detailed debugging information
4. **Review summaries**: Check the workflow summary for quick insights without downloading artifacts
5. **Run on-demand**: Trigger immediately when users report connectivity issues for real-time troubleshooting
