# How to Use Multiple GitHub Accounts on One Machine

This guide explains how to configure Git and SSH to push to a specific repository using a different GitHub account than your default one.

## 1. Prerequisites
You should have a separate SSH key pair for your secondary account. If not, generate one:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_secondary_account
```
*Add the public key (`.pub`) to your secondary GitHub account under **Settings > SSH and GPG keys**.*

## 2. Configure SSH Config (`~/.ssh/config`)
Edit your SSH config file (on Windows: `C:\Users\YourUser\.ssh\config`) to define a "Host alias" for the secondary account.

**Crucial Step:** Use `IdentitiesOnly yes` to force SSH to use *only* the specified key, preventing it from accidentally using your default key.

```ssh
# Default GitHub Account (optional to list explicitly, but good for clarity)
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa

# Secondary GitHub Account (The Alias)
Host github.com-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/qaa243631_personal
    IdentitiesOnly yes
```

## 3. Create the Repository
You can create the repo via the GitHub website or CLI.

**Using GitHub CLI (gh):**
If you want to use the CLI, you must switch authentication to the secondary account first:
```bash
gh auth login
```
*Select GitHub.com > SSH. Follow the prompts to authenticate the secondary account.*

Then create the repo:
```bash
gh repo create my-repo-name --public --source=. --remote=origin
```

## 4. Configure Git Remote with the Alias
This is the magic step. Instead of using `git@github.com:...`, use the **Host alias** you defined in Step 2 (`github.com-personal`).

If the remote already exists:
```bash
git remote set-url origin git@github.com-personal:username/repo-name.git
```

If adding a new remote:
```bash
git remote add origin git@github.com-personal:username/repo-name.git
```

## 5. Push
Now, simply push as normal. Git will see the host `github.com-personal`, look up the config, find the correct `IdentityFile`, and authenticate correctly.

```bash
git push -u origin main
```
