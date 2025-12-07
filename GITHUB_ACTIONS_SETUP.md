# GitHub Actions Setup Guide

## Quick Start: Setting Up On-Demand Wireless Troubleshooting

This guide will help you set up GitHub Actions to run wireless network troubleshooting on-demand when connectivity issues are reported.

### ✅ Prerequisites

- GitHub repository for this project
- Mist API token (get from Mist Dashboard)
- Basic familiarity with GitHub Actions

### 🚀 Setup Steps

#### Step 1: Push the Workflow to GitHub

The workflow file is already created at `.github/workflows/wireless-troubleshooting.yml`. 

Push it to your repository:

```bash
git add .github/
git commit -m "Add GitHub Actions workflow for wireless troubleshooting"
git push origin main
```

#### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

| Secret Name | Value | Notes |
|------------|-------|-------|
| `MIST_API_TOKEN` | Your Mist API token | **Required** - Get from Mist Dashboard |
| `MIST_ORG_ID` | Your Organization ID | Optional - Will auto-detect if not provided |

**How to get your Mist API Token:**
1. Log into Mist Dashboard (https://manage.mist.com)
2. Go to Organization → Settings → API Tokens
3. Create a new token with read permissions
4. Copy the token value


### 🎯 How to Use

#### Manual Run (Reactive Troubleshooting)

1. Go to **Actions** tab in your GitHub repository
2. Select **Wireless Network Troubleshooting** workflow
3. Click **Run workflow** dropdown
4. Fill in the form:
   - **Client IP Address**: e.g., `192.168.1.100`
   - **Client MAC Address**: e.g., `aa:bb:cc:dd:ee:ff`
   - **Hours Back**: e.g., `24` (hours of historical data)
   - **Enable Verbose Output**: Check for detailed logs
5. Click **Run workflow**

**Use this when:**
- A user reports connectivity issues
- You need to investigate specific client problems
- Proactive troubleshooting is needed for a known device

### 📊 Viewing Results

#### Artifacts (Full Logs)

1. Go to **Actions** tab
2. Click on a completed workflow run
3. Scroll to **Artifacts** section at the bottom
4. Download `troubleshooting-logs-{run_number}.zip`
5. Extract and view the `.log` files

#### Summary Report (Quick View)

1. Go to **Actions** tab
2. Click on a workflow run
3. View the **Summary** section at the top
4. See configuration, output preview, and key information

### 🔧 Workflow Features

| Feature | Description |
|---------|-------------|
| **Manual Trigger** | On-demand reactive troubleshooting |
| **Configurable Inputs** | IP, MAC, hours back, verbose mode |
| **Automatic Logging** | Timestamped logs with full troubleshooting output |
| **Artifact Storage** | Logs stored for 30 days (configurable) |
| **Summary Reports** | Quick preview in GitHub UI |
| **Always Uploads** | Logs saved even if troubleshooting fails |

### 🛠️ Customization Examples

#### Change Artifact Retention Period

Edit `.github/workflows/wireless-troubleshooting.yml`:

```yaml
- name: Upload troubleshooting logs
  uses: actions/upload-artifact@v4
  with:
    retention-days: 90  # Keep for 90 days instead of 30
```

#### Change Python Version

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.12'  # Use Python 3.12
```

#### Add Notifications (e.g., Slack, Email)

Add a notification step at the end:

```yaml
- name: Notify on Failure
  if: failure()
  uses: actions/slack-notification@v1
  with:
    webhook: ${{ secrets.SLACK_WEBHOOK }}
    message: 'Wireless troubleshooting failed!'
```

### 🐛 Troubleshooting

#### "Authentication failed" error

**Problem**: Workflow can't authenticate with Mist API

**Solutions**:
- Verify `MIST_API_TOKEN` secret is set correctly
- Check if token has expired
- Ensure token has proper read permissions
- Try running locally first: `python office_automation_cli.py auth test`


#### No artifacts uploaded

**Problem**: Can't find logs in artifacts section

**Solutions**:
- Check if workflow completed (even partially)
- Artifacts upload even on failure (using `if: always()`)
- Verify logs directory exists: `mkdir -p logs` runs before script
- Check workflow permissions: Settings → Actions → General → Workflow permissions


### 🔐 Security Best Practices

1. **Never commit API tokens** to the repository
2. **Use secrets** for all sensitive data (tokens, credentials)
3. **Use variables** for non-sensitive configuration (MAC, IP)
4. **Review workflow logs** for any exposed secrets (GitHub auto-redacts secrets)
5. **Limit token permissions** to read-only if possible
6. **Rotate tokens regularly** (update GitHub secret when you do)

### 📚 Additional Resources

- [Workflow README](.github/workflows/README.md) - Detailed workflow documentation
- [Main README](README.md) - Project overview and features
- [GitHub Actions Docs](https://docs.github.com/en/actions) - Official GitHub Actions documentation
- [Mist API Docs](https://api.mist.com/api/v1/docs/Home) - Mist API reference

### ✨ What's Next?

After setup:
1. **Test manually** with known devices to verify configuration
2. **Review the logs** to ensure output meets your needs
3. **Train your team** on how to trigger workflows when issues are reported
4. **Set up notifications** (optional) for critical issues
5. **Document findings** from troubleshooting runs for future reference

### 💡 Pro Tips

- **Keep credentials handy** when users report issues for immediate troubleshooting
- **Use verbose mode** when debugging complex connectivity problems
- **Download artifacts regularly** before they expire (30 days)
- **Document common MAC addresses** for frequently troubleshot devices
- **Monitor your GitHub Actions usage** (free tier limits apply)
- **Train your team** on how to trigger workflows for incident response

---

## Example: Complete Setup in 5 Minutes

```bash
# 1. Push workflow to GitHub
git add .github/
git commit -m "Add automated troubleshooting workflow"
git push origin main

# 2. Set secrets via GitHub CLI (alternative to web UI)
gh secret set MIST_API_TOKEN --body "your_token_here"
gh secret set MIST_ORG_ID --body "your_org_id_here"

# 3. Trigger manual run
gh workflow run wireless-troubleshooting.yml \
  -f client_mac=aa:bb:cc:dd:ee:ff \
  -f client_ip=192.168.1.100 \
  -f hours_back=24 \
  -f verbose=true

# 5. Watch the run
gh run watch
```

That's it! Your automated wireless troubleshooting is now set up. 🎉
