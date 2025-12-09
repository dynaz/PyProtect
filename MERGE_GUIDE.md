# Git Merge Guide: Windows Branch → Main

## Current Status
- **Current branch**: `windows`
- **Target branch**: `main`
- **Untracked files**: `PyProtect/` directory

## Step-by-Step Merge Process

### Option 1: Merge via Command Line (Recommended)

#### Step 1: Commit any changes on windows branch
```powershell
# Check what files need to be committed
git status

# Add all changes (or specific files)
git add .

# Commit the changes
git commit -m "Add Windows installation support and PyPI publishing"

# Push windows branch to remote (optional, but recommended)
git push origin windows
```

#### Step 2: Switch to main branch
```powershell
git checkout main
# or
git switch main
```

#### Step 3: Pull latest changes from remote main
```powershell
git pull origin main
```

#### Step 4: Merge windows branch into main
```powershell
git merge windows
```

#### Step 5: Push merged changes to remote
```powershell
git push origin main
```

### Option 2: Merge via GitHub/GitLab Web Interface

1. **Push your windows branch** (if not already pushed):
   ```powershell
   git push origin windows
   ```

2. **Go to your repository** on GitHub/GitLab

3. **Create a Pull Request**:
   - Click "New Pull Request" or "Merge Request"
   - Select `windows` → `main`
   - Review changes
   - Click "Create Pull Request"

4. **Merge the Pull Request**:
   - Review the changes
   - Click "Merge Pull Request"
   - Confirm merge

5. **Pull the updated main branch locally**:
   ```powershell
   git checkout main
   git pull origin main
   ```

## Quick Merge Commands (All at Once)

If you want to do it quickly:

```powershell
# 1. Commit changes on windows branch
git add .
git commit -m "Add Windows support and PyPI publishing"

# 2. Switch to main and merge
git checkout main
git pull origin main
git merge windows

# 3. Push to remote
git push origin main

# 4. Switch back to windows (optional)
git checkout windows
```

## Resolving Merge Conflicts

If you get merge conflicts:

1. **See which files have conflicts**:
   ```powershell
   git status
   ```

2. **Open conflicted files** and look for conflict markers:
   ```
   <<<<<<< HEAD
   (code from main branch)
   =======
   (code from windows branch)
   >>>>>>> windows
   ```

3. **Edit files** to resolve conflicts (keep what you want)

4. **Mark conflicts as resolved**:
   ```powershell
   git add <resolved-file>
   ```

5. **Complete the merge**:
   ```powershell
   git commit -m "Merge windows branch into main"
   ```

## Verify Merge

After merging, verify everything is correct:

```powershell
# Check you're on main branch
git branch

# See the merge commit
git log --oneline -5

# Check status
git status
```

## Common Issues

### Issue: "Your branch is ahead of 'origin/main'"
**Solution**: Push your changes:
```powershell
git push origin main
```

### Issue: "Please commit your changes or stash them"
**Solution**: Commit or stash changes first:
```powershell
# Option 1: Commit
git add .
git commit -m "Your message"

# Option 2: Stash (temporary save)
git stash
# ... do merge ...
git stash pop  # restore stashed changes
```

### Issue: Merge conflicts
**Solution**: Resolve conflicts manually (see "Resolving Merge Conflicts" above)

---

**Ready to merge?** Follow the steps above or use the quick merge commands!

