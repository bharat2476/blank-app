# VS Code Copilot Prompts Guide
## Nike Hyper Personalization & Marketing Technology Simulator

**Repository:** https://github.com/bharat2476/blank-app  
**Live Demo:** https://blank-app-zwp52hqbzm2sxhgqckmv6w.streamlit.app/  
**Local Port:** http://localhost:8501

---

## 📋 Overview

This document provides three core VS Code Copilot prompts for managing, running, and deploying the Nike Personalization app. Use these to automate setup, development, and cloud deployment workflows.

---

## Prompt 1️⃣: Run Full App Using VS Code Copilot

### Purpose
Set up and launch the Streamlit app locally for development and testing.

### Full Prompt
```
Create a complete VS Code terminal task and development environment setup guide for the Nike Hyper Personalization & Marketing Technology Simulator Streamlit app. Include:

1. Python environment verification (v3.14+ required)
2. Virtual environment setup (optional but recommended)
3. Dependency installation from requirements.txt
4. Terminal command to start the Streamlit dev server with CORS and CSRF protection disabled
5. Environment variables to set (if any)
6. Browser launch instructions pointing to http://localhost:8501
7. Common startup errors and troubleshooting steps
8. How to verify all 7 tabs load successfully
9. Hot reload behavior during development
10. Cleanup steps when stopping the server

Requirements:
- Support Windows PowerShell, WSL2, and macOS/Linux terminals
- Include performance tips for large data generation
- Note that the app generates 500 products and 100 synthetic users on first load
- Include member selection filters and how to test each one
- Include privacy mode testing instructions (Full consent, Limited consent, No app usage data)
```

### Quick Start Command
```powershell
cd "c:\Users\agarw\Personalization using VS"
python -m streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
```

### Expected Success Indicators
✅ Terminal shows "You can now view your Streamlit app in your browser"  
✅ Local URL: http://localhost:8501  
✅ All 7 tabs load without errors  
✅ Member selection filters respond to changes  
✅ Recommendations tab shows ranked products  

---

## Prompt 2️⃣: Deployment to Streamlit Cloud Using VS Code Copilot

### Purpose
Deploy the app to Streamlit Cloud for public access and share the live URL.

### Full Prompt
```
Create a comprehensive Streamlit Cloud deployment guide for the Nike Hyper Personalization & Marketing Technology Simulator. This guide should help a developer go from local development to a production-ready deployment. Include:

1. Pre-deployment checklist
   - All code committed to GitHub (no uncommitted changes)
   - requirements.txt updated with all dependencies
   - .gitignore configured properly (.vscode, __pycache__, .streamlit/secrets.toml)
   - README.md includes live URL and setup instructions

2. GitHub repository setup
   - Ensure repo is public at https://github.com/bharat2476/blank-app
   - Verify main branch is up to date
   - How to fork or push code if needed

3. Streamlit Cloud deployment steps
   - Login to https://share.streamlit.io/
   - Click "New app" and select GitHub source
   - Configure app settings (main file: streamlit_app.py, branch: main)
   - CORS and CSRF settings for security

4. Environment variables and secrets
   - How to manage secrets in Streamlit Cloud (if API keys needed)
   - .streamlit/config.toml settings for production

5. Post-deployment verification
   - Verify all 7 tabs load correctly on live URL
   - Test member selection and simulation
   - Check performance metrics (load time, response time)
   - Monitor deployment logs for errors

6. Troubleshooting deployment issues
   - "Module not found" errors (missing dependencies)
   - Timeout errors during data generation
   - Git lock file errors during deployment
   - How to redeploy after code updates

7. Performance optimization
   - Caching strategy for 500+ products and 100 users
   - Session state management for faster reloads
   - CDN and static file serving

8. Monitoring and maintenance
   - How to check live app logs
   - How to debug production issues
   - When to restart the app
   - Updating code and redeploying

9. Success criteria
   - Live URL is publicly accessible
   - All features work without errors
   - Page loads in under 3 seconds
   - Member selection and recommendations work smoothly

10. Rollback and recovery
    - How to revert to previous version if deployment fails
    - How to pause/stop the app
    - How to delete and redeploy if needed
```

### Current Live Status
- **URL:** https://blank-app-zwp52hqbzm2sxhgqckmv6w.streamlit.app/
- **Status:** ✅ Active and accessible
- **GitHub:** https://github.com/bharat2476/blank-app
- **Branch:** main

### Deployment Command Flow
```powershell
# 1. Verify local changes
git status

# 2. Commit changes
git add .
git commit -m "Update: [description of changes]"

# 3. Push to GitHub
git push origin main

# 4. Log in to Streamlit Cloud
# https://share.streamlit.io/

# 5. Deploy or redeploy existing app (automatic on push to main)
```

### Common Issues & Fixes

**Issue:** "Another git process is running" when pushing  
**Fix:** Remove stale lock file and retry
```powershell
rm -Force .\.git\index.lock
git push origin main
```

**Issue:** Uncommitted changes error  
**Fix:** Commit all changes first
```powershell
git add .
git commit -m "Checkpoint commit"
git push origin main
```

**Issue:** Module not found on cloud deployment  
**Fix:** Update requirements.txt
```powershell
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

---

## Prompt 3️⃣: Git Workflow & Commit Guide Using VS Code Copilot

### Purpose
Understand and resolve common git issues, manage commits, and troubleshoot deployment blocks.

### Full Prompt
```
Create a comprehensive guide for managing git workflows in VS Code for the Nike Personalization app. This should be beginner-friendly but also cover advanced scenarios. Include:

1. Understanding VS Code Source Control panel
   - How to open Source Control (Ctrl+Shift+G)
   - Viewing changed files (M = modified, U = untracked, D = deleted)
   - Staging individual files vs. staging all changes
   - Discarding changes
   - Viewing diffs

2. Git status interpretation
   - "On branch main"
   - "Your branch is up to date with 'origin/main'"
   - "Untracked files" (files not added to git)
   - "Changes not staged for commit" (modified but not added)
   - "Changes to be committed" (staged, ready to commit)

3. The commit workflow
   - Stage files using git add or VS Code UI
   - Write meaningful commit messages (first line: brief summary, then details)
   - Commit using git commit or VS Code UI
   - Push using git push origin main
   - Verify on GitHub that changes appear

4. Common error: "index contains uncommitted changes"
   - What this means: You're trying to switch branches/rebase but have unsaved work
   - How to fix: 
     a) Commit your changes: git commit -m "message"
     b) Or stash them: git stash (temporarily save without committing)
   - Prevention: Always commit or stash before switching branches

5. Common error: "another git process is running in this repository"
   - Cause: Stale .git/index.lock file from interrupted git operation
   - Fix:
     a) Remove lock file: rm -f ./.git/index.lock
     b) Verify integrity: git fsck
     c) Retry the operation
   - Prevention: Don't force-kill git operations; let them complete

6. Files to commit for this project
   - streamlit_app.py (main application)
   - ranking.py (recommendation engine)
   - auction.py (sponsored ads auction)
   - metrics.py (KPI calculations)
   - data_generator.py (synthetic data generation)
   - requirements.txt (Python dependencies)
   - README.md (documentation)
   - architecture diagram.* (visual documentation)

7. Files to NOT commit
   - .vscode/ (user-specific editor settings)
   - __pycache__/ (compiled Python cache)
   - .streamlit/secrets.toml (sensitive credentials)
   - *.pyc (compiled Python files)

8. Branching strategy
   - Use main branch for production-ready code
   - Create feature branches for new features (feature/feature-name)
   - Merge back to main when feature is complete and tested
   - Delete feature branch after merge

9. Undoing changes
   - Undo local edits (not committed): git checkout -- <file>
   - Undo staged changes: git reset <file>
   - Undo last commit (keep changes): git reset --soft HEAD~1
   - Undo last commit (discard changes): git reset --hard HEAD~1
   - Undo pushed changes: git revert <commit-hash>

10. Verifying successful push
    - GitHub web interface shows your commit in commit history
    - Deployment automatically starts on Streamlit Cloud (if configured)
    - Live URL reflects your latest changes within 1-2 minutes

11. Debugging push failures
    - Check git status for uncommitted changes
    - Check internet connection
    - Verify GitHub credentials are cached/saved
    - Check for protected branch rules (ask repo admin)
    - Check for repository write permissions
```

### Step-by-Step Example

**Scenario:** You modified `streamlit_app.py` and want to push changes

```powershell
# 1. Check status
git status
# Output: On branch main, Changes not staged for commit

# 2. Stage the file
git add streamlit_app.py

# 3. Verify staging
git status
# Output: Changes to be committed

# 4. Write commit message
git commit -m "Feature: Add new recommendation filter to Tab 2"

# 5. Push to GitHub
git push origin main

# 6. Verify on GitHub
# https://github.com/bharat2476/blank-app/commits/main
# (You should see your commit in the list)
```

---

## 🔄 Troubleshooting Decision Tree

```
Something went wrong with git?
│
├─ "fatal: another git process is running"
│  └─→ Fix: rm -f ./.git/index.lock && git status
│
├─ "Changes not staged for commit" (after editing files)
│  └─→ Action: git add <file> && git commit -m "message" && git push
│
├─ "index contains uncommitted changes"
│  └─→ Action: git commit -m "message" (commit first, then switch branches)
│
├─ "Your branch is ahead of origin/main"
│  └─→ Action: git push origin main
│
├─ "Your branch is behind origin/main"
│  └─→ Action: git pull origin main (fetch latest from GitHub)
│
├─ "File already exists in index"
│  └─→ Action: git reset <file> && git add <file>
│
└─ Deployment didn't update on Streamlit Cloud
   └─→ Checklist:
       1. git status (no uncommitted changes?)
       2. git push origin main (pushed to GitHub?)
       3. Check Streamlit Cloud logs
       4. Hard refresh browser (Ctrl+Shift+R)
```

---

## 📊 Quick Reference Table

| Task | Command | Expected Output |
|------|---------|-----------------|
| Check status | `git status` | "On branch main" + file list |
| Stage all | `git add .` | (silent) |
| Stage one file | `git add filename.py` | (silent) |
| Commit | `git commit -m "message"` | List of changed files |
| Push | `git push origin main` | "master -> master" or similar |
| View history | `git log --oneline` | List of recent commits |
| View remote | `git remote -v` | GitHub URL |

---

## 🎯 Success Criteria Checklist

- [ ] App runs locally on localhost:8501 without errors
- [ ] All 7 tabs load and are interactive
- [ ] Git status shows "up to date with origin/main"
- [ ] No uncommitted changes (except .vscode/)
- [ ] Live demo URL works: https://blank-app-zwp52hqbzm2sxhgqckmv6w.streamlit.app/
- [ ] Latest code changes appear on live URL within 2 minutes of push
- [ ] Can commit changes using git workflow
- [ ] Can troubleshoot common git errors independently

---

## 🔗 Helpful Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **Git Documentation:** https://git-scm.com/doc
- **GitHub Guide:** https://guides.github.com/
- **GitHub Issues:** https://github.com/bharat2476/blank-app/issues
- **Streamlit Cloud Docs:** https://docs.streamlit.io/streamlit-cloud/get-started

---

## 📝 Notes

- The app generates synthetic data on first load (may take 10-15 seconds)
- Session state preserves data across tab switches for better UX
- Privacy modes filter signals to demonstrate consent-aware personalization
- Auction logic requires proper seller_id merge to avoid KeyError
- README.md documents all 7 tabs and live URL for quick reference

