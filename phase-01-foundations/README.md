# Phase 1: Foundations & Mindset Reset
**Weeks 1–4 | 160 hours | 40 hrs/week**

> Consultant framing: "I can diagnose, tune, and secure any Linux system under production pressure — and explain the business impact of every decision."

---

## Phase Checklist

### Week 1 — Linux Deep Dive
- [ ] Lab 1.1: File system & permission hardening audit script
- [ ] Lab 1.2: Process management & systemd service creation
- [ ] Lab 1.3: Bash script — production-grade with error handling
- [ ] Lab 1.4: Network troubleshooting toolkit
- [ ] Lab 1.5: Kernel parameter tuning for high-throughput apps
- [ ] Project: Enterprise Linux Sysadmin Toolkit v1.0
- [ ] Interview: 20 Linux Q&A reviewed and practiced

### Week 2 — Networking Mastery
- [ ] Lab 2.1: TCP/IP deep dive with tcpdump
- [ ] Lab 2.2: DNS resolution tracing
- [ ] Lab 2.3: Build a load balancer from scratch (HAProxy)
- [ ] Lab 2.4: VPN setup with WireGuard
- [ ] Lab 2.5: Network security hardening (iptables/nftables)
- [ ] Project: Network Diagnostic & Monitoring Suite
- [ ] Interview: 20 Networking Q&A reviewed and practiced

### Week 3 — Git & Collaboration at Scale
- [ ] Lab 3.1: Git internals — objects, trees, commits
- [ ] Lab 3.2: Advanced merge strategies + conflict resolution
- [ ] Lab 3.3: Git hooks for automated quality gates
- [ ] Lab 3.4: Implement trunk-based development workflow
- [ ] Lab 3.5: GitOps repo structure design
- [ ] Project: Enterprise Git Workflow System
- [ ] Interview: 15 Git + workflow Q&A

### Week 4 — Communication & Python/Scripting
- [ ] Lab 4.1: Python automation scripts for sysadmin tasks
- [ ] Lab 4.2: REST API interaction with curl + Python requests
- [ ] Lab 4.3: JSON/YAML parsing and manipulation
- [ ] Lab 4.4: Cron job automation with alerting
- [ ] Lab 4.5: Documentation-as-code with Markdown + diagrams
- [ ] Project: Infrastructure Automation Suite v1.0
- [ ] STAR method: Write 10 career stories in STAR format
- [ ] Interview: 15 scripting + automation Q&A

---

## 📦 Enterprise Projects

### Project 1: Enterprise Linux Sysadmin Toolkit
**Duration:** Saturday Week 1 (6h) + Saturday Week 2 (3h)  
**Business Problem:** Mid-size company has 200 Linux servers with no standardised monitoring, no audit trail, inconsistent security posture. You're the consultant brought in to fix it.  
**Deliverables:**

```bash
sysadmin-toolkit/
├── audit/
│   ├── security_audit.sh          # CIS Benchmark checks
│   ├── user_audit.sh              # Find over-privileged users
│   ├── port_scanner.sh            # Open ports + service mapping
│   └── file_integrity.sh          # Changed files since last check
├── monitoring/
│   ├── resource_monitor.sh        # CPU/mem/disk with thresholds
│   ├── process_guardian.sh        # Restart failed services
│   └── log_analyzer.sh            # Top error patterns + alerting
├── hardening/
│   ├── ssh_hardener.sh            # Disable root, key-only, fail2ban
│   ├── sysctl_tuner.sh            # Kernel params for prod workloads
│   └── firewall_setup.sh          # iptables baseline rules
├── reporting/
│   ├── daily_report.sh            # HTML report emailed daily
│   └── compliance_report.sh       # SOC2-style evidence collection
└── README.md                      # Business impact + usage guide
```

**Business Impact to document:**
- Time to audit 1 server: before vs after
- Security findings discovered
- Compliance posture improvement

**Tech:** bash, Python, systemd, cron, iptables, fail2ban, auditd  
**CNCF Connection:** This is the foundation Falco and OPA are built on

---

### Project 2: Network Diagnostic & Monitoring Suite
**Duration:** Spread across Week 2 evenings + Saturday  
**Business Problem:** Production incident at 2am — network is the suspect. You need a toolkit that any on-call engineer can run and get a diagnosis in 5 minutes, not 45.  
**Deliverables:**

```bash
network-toolkit/
├── diagnostics/
│   ├── quick_diagnosis.sh         # 5-min network health check
│   ├── latency_tracker.sh         # RTT trends to key services
│   ├── dns_checker.sh             # DNS propagation + consistency
│   ├── ssl_checker.sh             # Certificate expiry + chain
│   └── bandwidth_test.sh          # Throughput measurement
├── capture/
│   ├── capture_session.sh         # tcpdump with filters + rotation
│   └── packet_analyser.py         # Parse and summarize pcap files
├── haproxy/
│   ├── haproxy.cfg                # Production HAProxy config
│   └── stats_monitor.sh           # Real-time stats parsing
└── runbooks/
    ├── high-latency.md            # On-call runbook
    ├── dns-failure.md             # DNS incident runbook
    └── packet-loss.md             # Packet loss runbook
```

**Must include:** Every script has `--help`, structured logging, exit codes  
**Tech:** bash, Python, tcpdump, HAProxy, WireGuard, iptables, dig, ss, netstat

---

### Project 3: Enterprise Git Workflow System
**Duration:** Week 3 project work  
**Business Problem:** Engineering org of 50 devs has no consistent branching strategy, no automated quality gates, secrets leak into commits, code reviews are inconsistent.  

```bash
git-workflow-system/
├── hooks/
│   ├── pre-commit                 # Secret detection, lint, format
│   ├── commit-msg                 # Conventional commits enforcer
│   ├── pre-push                   # Run tests, check branch naming
│   └── install-hooks.sh           # One-command setup for all devs
├── workflows/
│   ├── trunk-based/               # Trunk-based dev setup guide
│   ├── gitflow/                   # Gitflow implementation
│   └── github-flow/               # GitHub flow for SaaS
├── templates/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── CODEOWNERS
└── automation/
    ├── changelog_generator.py     # Auto-generate CHANGELOG from commits
    └── release_tagger.sh          # Semantic versioning automation
```

---

### Project 4: Infrastructure Automation Suite
**Duration:** Week 4  
**Business Problem:** Ops team spends 3 hours/day on repetitive tasks — user provisioning, log rotation, backup verification, capacity alerts.  

```bash
infra-automation/
├── user_management/
│   ├── provision_user.sh          # Create user + SSH key + sudo policy
│   ├── offboard_user.sh           # Revoke access + archive home dir
│   └── audit_users.sh             # Find orphaned/inactive accounts
├── backup_management/
│   ├── backup_verify.sh           # Test restores, not just backups
│   └── backup_report.py           # Daily backup health report
├── capacity/
│   ├── capacity_alert.sh          # Predict disk full X days out
│   └── cleanup_advisor.sh         # Find large/old files
├── api_tools/
│   ├── slack_notifier.py          # Send alerts to Slack
│   └── pagerduty_trigger.py       # PagerDuty incident creation
└── scheduler/
    └── crontab.example            # Production cron setup template
```

---

## 📋 Labs (Daily 45-Minute Sessions)

### Week 1 Labs

**Lab 1.1 — Permission Hardening (Mon evening)**
```bash
# Objective: Find and fix all SUID/SGID binaries + world-writable dirs
find / -perm -4000 -type f 2>/dev/null | tee suid_files.txt
find / -perm -2000 -type f 2>/dev/null | tee sgid_files.txt
find / -perm -o+w -type d 2>/dev/null | grep -v /proc | tee world_writable.txt

# Your task: script that checks these on boot and alerts if new entries appear
# Output: report with risk classification (high/med/low)
# Time box: 45 minutes. Push to GitHub.
```

**Lab 1.2 — Systemd Service (Tue evening)**
```bash
# Objective: Convert a bash script into a proper systemd service
# The service: runs a health check every 30s and logs to journald
# Must have: Restart=on-failure, proper After= dependencies, User= (non-root)
# Bonus: socket activation
```

**Lab 1.3 — Production Bash Script (Wed evening)**
```bash
#!/usr/bin/env bash
# Objective: Write a disk space monitor that:
# 1. Takes threshold as argument (default 80%)
# 2. Sends Slack webhook if threshold exceeded
# 3. Logs structured JSON to /var/log/disk-monitor.log
# 4. Has proper set -euo pipefail, trap ERR, exit codes
# 5. Works idempotently (can run from cron safely)
```

**Lab 1.4 — Network Troubleshooting (Thu evening)**
```bash
# Scenario: Production app is slow. Could be network.
# Your toolkit to build:
# 1. Check DNS resolution time for 10 endpoints
# 2. Test TCP connectivity to all service dependencies  
# 3. Capture 30s of traffic on port 443 and summarise top talkers
# 4. Check for TIME_WAIT accumulation (common in high-traffic apps)
# 5. Output: structured report with pass/fail for each check
```

**Lab 1.5 — Kernel Tuning (Fri morning)**
```bash
# Objective: Tune a server for a high-traffic web application
# Parameters to research and set:
# - net.core.somaxconn (connection queue)
# - net.ipv4.tcp_fin_timeout
# - net.ipv4.ip_local_port_range
# - vm.swappiness
# - fs.file-max
# Document: what each does, why you set it, how to verify it worked
```

### Week 2 Labs

**Lab 2.1 — TCP/IP Wireshark (Mon evening)**
```bash
# Objective: Capture and analyse a complete HTTP/HTTPS session
# Install: tcpdump or Wireshark
tcpdump -i eth0 -w capture.pcap 'host api.github.com' &
curl -v https://api.github.com/zen
# Analyse: 3-way handshake, TLS negotiation, HTTP request/response
# Write: 1-page summary of what you observed
```

**Lab 2.2 — DNS Deep Dive (Tue evening)**
```bash
# Objective: Trace full DNS resolution from root to answer
# Tools: dig, dnstracer, tcpdump
dig +trace github.com
dig +trace github.com @8.8.8.8
# Compare: recursive vs iterative resolution
# Build: DNS health checker that tests all record types (A, AAAA, MX, TXT, CNAME)
```

**Lab 2.3 — HAProxy Load Balancer (Wed evening)**
```bash
# Objective: Set up HAProxy with 3 backend servers (use Docker)
# Must have:
# - Health checks (every 2s, 3 failures = down)
# - Stats page on :8404
# - Rate limiting (50 req/s per IP)
# - ACL-based routing (api.* vs www.*)
# - Access logging in JSON format
```

**Lab 2.4 — iptables Firewall (Thu evening)**
```bash
# Objective: Implement a production firewall ruleset
# Requirements:
# - Default DROP all INPUT and FORWARD
# - Allow: established connections, SSH (rate limited), HTTP/HTTPS
# - Block: port scans (SYN flood protection), ping floods
# - Log: dropped packets to syslog
# - Make persistent: iptables-persistent
```

**Lab 2.5 — WireGuard VPN (Fri evening)**
```bash
# Objective: Set up a WireGuard VPN server
# - Server on a VPS or VM
# - 3 client configs (your laptop, phone simulation, remote server)
# - Route all traffic through VPN
# - Add DNS leak prevention
```

*(Labs continue in `/labs/` directory with full scripts)*

---

## 🎤 Interview Preparation

See `interview-prep/` folder for full Q&A. Quick reference:

### Week 1 — Linux (Top 5 Must-Know)

**Q: A production server is at 99% CPU. Walk me through your diagnosis.**
> Start: `top` / `htop` — identify PID. Then `ps aux --sort=-%cpu | head`. Check if it's a single process or system-wide. Run `perf top` or `strace -p <PID>` to see what it's doing. Check `/proc/<PID>/status` for memory. Look at `vmstat 1 5` — is CPU or I/O wait high? Check logs: `journalctl -u <service> --since "5 minutes ago"`. **Always establish a timeline first — when did it start?**

**Q: Explain the difference between a hard link and a symbolic link.**
> Hard link: another directory entry pointing to the same inode. Same file, two names. Cannot cross filesystems. Deleting original doesn't affect hard link. Symbolic link: a file that contains a path to another file. Can cross filesystems. If original is deleted, symlink breaks. `ls -i` shows inode numbers — hard links share one.

**Q: How does the Linux kernel schedule processes?**
> CFS (Completely Fair Scheduler) since kernel 2.6.23. Uses a red-black tree ordered by vruntime (virtual runtime). Process with smallest vruntime runs next. Nice values adjust weight. Real-time processes (SCHED_FIFO, SCHED_RR) preempt CFS. `chrt` to set RT priority, `nice`/`renice` for CFS priority.

**Q: What is a cgroup and how does Kubernetes use it?**
> Control groups (cgroups) limit and account for resource usage by groups of processes. Kubernetes uses cgroups to enforce `requests` and `limits` on containers — CPU shares map to cgroup cpu.shares, memory limits map to cgroup memory.limit_in_bytes. CRI (containerd) creates a cgroup per container. `systemd-cgls` to see the hierarchy.

**Q: A disk is 100% full. What are the exact steps you take?**
> 1. Don't panic. 2. `df -h` — which filesystem. 3. `du -sh /* 2>/dev/null | sort -rh | head` — find top offenders. 4. `lsof | grep deleted` — large deleted files held open by processes (common!). 5. Check log directories: `/var/log`. 6. Check for large core dumps: `find / -name "core" -size +100M`. 7. Temporary relief: clear journal (`journalctl --vacuum-size=500M`). 8. Root cause: add alerting so this never happens again.

See `interview-prep/week1-linux.md` for all 20 questions with full answers.

---

## 📚 Resources

### Week 1 Reading List
- **The Linux Command Line** — William Shotts (free online)
- **Linux Kernel Development** — Robert Love (Ch 1-4)
- `/proc` and `/sys` filesystem: `man proc`
- **CIS Benchmarks for Linux** — free download from cisecurity.org

### Week 2 Reading List  
- **Computer Networks** — Tanenbaum (Ch 1-6)
- **TCP/IP Illustrated Vol 1** — Stevens (Ch 1, 2, 17, 18)
- RFC 793 (TCP), RFC 1035 (DNS), RFC 2818 (HTTPS)
- **High Performance Browser Networking** — Ilya Grigorik (free online)

### Week 3 Reading List
- **Pro Git** — Scott Chacon (free: git-scm.com/book)
- **Trunk Based Development** — trunkbaseddevelopment.com
- Conventional Commits spec: conventionalcommits.org

### Week 4 Reading List
- **Python for DevOps** — Noah Gift
- **The Art of Unix Programming** — Eric S. Raymond (free online)
- **Google Shell Style Guide** — google.github.io/styleguide/shellguide.html

---

## 🔗 CNCF Tools Introduced This Phase

| Tool | Why It Matters | Learn More |
|------|---------------|------------|
| None yet (CNCF comes Phase 2) | Build the foundation first | - |

*The discipline you build in Phase 1 determines how fast you move in Phase 2.*
