# Interview Preparation — Phase 1: Foundations
## 80 Questions Across 4 Weeks | With Full Model Answers

> Strategy: Read the answer. Close the file. Say it out loud. Record yourself. Review. Repeat.  
> Target: Each answer delivered confidently in 90–120 seconds.

---

# WEEK 1 — Linux Mastery (20 Questions)

## Technical Deep-Dive

**Q1. A production server has a memory leak. How do you find and fix it?**

Model Answer:
```
First, confirm it's a leak: watch -n1 'free -h' over 10 minutes — is available 
memory consistently dropping? Then identify the process: ps aux --sort=-%mem | head -20.

For Java apps: jmap -heap <PID> to see heap usage. For native: use valgrind 
(staging only) or check /proc/<PID>/maps for growing anonymous mappings.

Quick mitigation: if it's a managed service, restart with proper health checks.
Long-term: enable core dumps, collect heap dump before OOM kills it, 
give to devs. Add memory alerting: alert at 80%, page at 90%.

Root cause always gets documented in a postmortem — memory leaks in prod mean 
someone's process for load testing needs fixing too.
```

**Q2. Explain inodes. What happens when you run out of inodes but still have disk space?**

Model Answer:
```
An inode is a data structure storing file metadata: permissions, owner, timestamps, 
block pointers — everything except the filename (that's in the directory entry).

Every file uses one inode. df -i shows inode usage. When inodes are exhausted:
- You cannot create new files even with free disk space
- Classic symptom: "No space left on device" but df -h shows space available

Diagnosis: df -i to find full filesystem. Find inodes hog: find / -xdev -printf 
'%h\n' | sort | uniq -c | sort -rn | head — usually /tmp or a log directory 
with millions of tiny files.

Fix: delete small files (temp files, empty logs, pid files). Prevention: 
mount with explicit inode count in /etc/fstab, or move high-file-count 
directories to dedicated filesystems.
```

**Q3. What is the difference between a process and a thread? How does the kernel manage them?**

Model Answer:
```
A process is an independent execution unit with its own virtual address space, 
file descriptors, and resources. A thread shares address space with sibling 
threads in the same process but has its own stack and registers.

Linux kernel treats both via the task_struct — there's no fundamental difference 
at the kernel level. A thread is created with clone() instead of fork(), 
sharing specific resources via flags (CLONE_VM, CLONE_FS, CLONE_FILES).

Context switching between threads in the same process is cheaper — no page table 
swap. Between processes, the kernel flushes TLB and switches page tables.

In a container: each container PID 1 is a process. Kubernetes sets CPU limits 
via cgroups — this limits the entire cgroup, so thread-heavy apps can still 
hit limits even with one "process".
```

**Q4. How does the Linux boot process work from power-on to shell?**

Model Answer:
```
1. BIOS/UEFI: POST, finds bootable device, loads bootloader from MBR/ESP
2. GRUB: loads kernel image (vmlinuz) and initramfs into RAM
3. Kernel init: decompresses, initialises hardware, mounts initramfs as /
4. initramfs: contains minimal tools to find real root filesystem
5. Real root: kernel pivots to real /, hands off to init (PID 1)
6. systemd: reads unit files, resolves dependency graph, starts target units
7. getty: starts on TTYs, login prompt appears

For containers: steps 1-5 don't happen. The container runtime provides 
an already-running kernel. The container starts at PID 1 with whatever 
binary is ENTRYPOINT — often bash or the app itself.

Troubleshooting boot issues: GRUB → kernel params → systemd-analyze blame 
→ journalctl -b to see boot logs.
```

**Q5. What are file descriptors? How many can a process have? How do you fix "too many open files"?**

Model Answer:
```
File descriptors are integer handles to open files, sockets, pipes. 
0=stdin, 1=stdout, 2=stderr. Every open() call returns a new FD.

Limits: soft limit (ulimit -n), hard limit (ulimit -Hn), system-wide 
(fs.file-max in sysctl). Default soft limit is typically 1024.

"Too many open files" → lsof -p <PID> | wc -l to count. lsof -p <PID> 
to see what they are — often unclosed socket connections.

Fix immediately: raise limit in /etc/security/limits.conf:
  myapp soft nofile 65536
  myapp hard nofile 65536
For systemd services: LimitNOFILE=65536 in [Service]

Root cause: almost always a bug — unclosed connections, no connection pooling,
FD leak. Don't just raise the limit — fix the leak.
```

**Q6. Explain cgroups v2. How does Kubernetes use them?**

Model Answer:
```
Cgroups v2 (unified hierarchy) replaced the split v1 hierarchy. 
Single tree at /sys/fs/cgroup. Controllers: cpu, memory, io, pids, cpuset.

Kubernetes maps:
- resources.requests.cpu → cpu.shares (relative weight)  
- resources.limits.cpu → cpu.max (throttling period)
- resources.limits.memory → memory.max (OOM killer threshold)

When a container exceeds memory.max: OOM killer fires, kills process, 
Pod restarts. You see: OOMKilled in kubectl describe pod.

For CPU limits: linux throttles via quota. If cpu.max = 100000 250000, 
process gets 100ms per 250ms period = 40% of one core. 
This is why high CPU limits ≠ unlimited — the quota mechanism adds latency.

Best practice: always set requests (for scheduling) and limits (for safety).
Never set CPU limits without understanding quota implications.
```

**Q7. What is the difference between SIGTERM and SIGKILL? How should applications handle them?**

Model Answer:
```
SIGTERM (15): graceful termination request. Process can catch it, 
run cleanup code, finish in-flight requests, close connections, flush buffers.
SIGKILL (9): unconditional kill by kernel. Cannot be caught or ignored. 
Process dies immediately — no cleanup.

Best practice:
1. Always try SIGTERM first: kill <PID>
2. Wait 30 seconds for graceful shutdown
3. If still running: kill -9 <PID>

Applications MUST handle SIGTERM:
- Close database connections
- Finish processing current request
- Flush write buffers
- Exit with code 0

Kubernetes sends SIGTERM → waits terminationGracePeriodSeconds (default 30s) 
→ then SIGKILL. If your app takes longer than 30s to shut down, increase 
terminationGracePeriodSeconds or fix your shutdown logic.

Signal-deaf containers (often zombie PID 1s) is a common K8s issue.
Solution: use tini as PID 1 or Docker's --init flag.
```

**Q8. How does virtual memory work? Explain swap.**

Model Answer:
```
Virtual memory gives each process its own address space (64-bit = 128TB virtual).
The kernel maps virtual pages to physical frames via page tables. 
MMU handles the translation with TLB caching.

When physical RAM fills:
1. LRU page replacement — kernel evicts least-recently-used pages
2. Clean pages (already on disk) → simply discarded
3. Dirty pages → written to swap, then freed

Swap is disk space used as memory overflow. vm.swappiness controls tendency 
to swap (0 = avoid swap, 100 = swap aggressively). For databases: set to 1-10.
For web servers: 10-20. Never 0 — you still want swap available for emergencies.

In containers: swap is usually disabled. Pod OOM is cleaner than swap 
(swap hides memory pressure until too late). 

Production sign of trouble: high swap IO (vmstat si/so columns) = 
memory pressure → add RAM or investigate leaks.
```

**Q9. What is the Linux scheduler and how do nice values work?**

Model Answer:
```
CFS (Completely Fair Scheduler): maintains a red-black tree sorted by vruntime.
Picks process with lowest vruntime to run next. Tracks "fair share" — 
if you ran too little, your vruntime is low → you get scheduled sooner.

Nice values: -20 (highest priority) to +19 (lowest priority).
Nice 0 is default. Each nice step = ~10% more/less CPU share.
Set with: nice -n 10 ./myapp or renice -n 5 -p <PID>

For real-time tasks: SCHED_FIFO or SCHED_RR (preempts CFS entirely).
Set with: chrt -f -p 50 <PID> (FIFO, priority 50)

Production relevance: 
- Set background jobs to nice 19 so they don't compete with app
- Database with nice -5 gets more CPU than default
- Never give RT priority to untested code — can starve all other processes
```

**Q10. Explain SELinux/AppArmor. Why do they matter in production?**

Model Answer:
```
Mandatory Access Control (MAC) on top of DAC (normal permissions).
Even root can't do things not permitted by MAC policy.

SELinux (RHEL/CentOS): label-based. Every file, process, port has a security 
context (user:role:type:level). Policy defines what types can talk to what.
AppArmor (Ubuntu/Debian): path-based. Profiles define what files a program 
can access and what system calls it can make.

Why it matters: if an app is compromised, the attacker is confined to 
what that process's MAC policy allows. A web server shouldn't be able 
to read /etc/shadow — SELinux enforces that even if the app is running as root.

In containers: Kubernetes PSP → PodSecurity → seccomp + AppArmor profiles.
docker run --security-opt apparmor=docker-default

Common mistake: setting setenforce 0 (permissive mode) to fix errors 
instead of fixing the policy. This is a security failure.

Interview tip: say "I troubleshoot AVC denials with audit2allow and 
fix the policy rather than disabling SELinux."
```

## Behavioral Questions

**Q11. Describe a Linux production incident you handled under pressure.**
> Use STAR. Include: exact commands you ran, your communication with stakeholders, 
> what you learned, and what monitoring you added after. Numbers matter: 
> "We were down for 23 minutes, I reduced that to 4 minutes on the next similar incident."

**Q12. How do you approach performance tuning on a Linux server you've never seen before?**
> "I follow a methodology: establish baseline (vmstat, iostat, top, netstat for 5 minutes), 
> identify bottleneck type (CPU/IO/memory/network), correlate with application metrics, 
> make one change at a time, measure, document. Never tune blindly."

**Q13. A junior engineer asks you to explain what 'everything is a file' means in Linux. How do you explain it?**
> "I'd say: in Linux, the kernel exposes almost everything through the file interface — 
> regular files, directories, devices (/dev/sda), network sockets, process info (/proc/1234), 
> hardware config (/sys), named pipes, and more. This means you can use the same tools 
> (cat, echo, read, write) on all of them. For example, cat /proc/cpuinfo gives you CPU info, 
> echo 1 > /proc/sys/net/ipv4/ip_forward enables routing. This is the Unix philosophy 
> made concrete."

**Q14. How would you set up a new Linux server in a production environment from scratch?**
> Systematic answer covering: initial hardening (SSH keys, disable root, fail2ban), 
> update packages, configure firewall, set up monitoring agent, configure log shipping, 
> apply CIS benchmarks, document in CMDB, peer review before opening to traffic.

**Q15–20: See `week1-linux.md` for remaining 5 questions**

---

# WEEK 2 — Networking (20 Questions)

**Q1. What happens when you type google.com in a browser? Full technical answer.**

Model Answer:
```
1. DNS Resolution:
   - Browser checks cache → OS cache → resolv.conf for recursive resolver
   - Recursive resolver checks cache → queries root servers → TLD (.com) → 
     Google's authoritative NS → returns A record (142.250.x.x)
   - TTL cached at each level

2. TCP Connection:
   - Browser picks ephemeral source port (32768-60999)
   - SYN → server (port 443) → SYN-ACK → ACK (3-way handshake)
   - ~1 RTT to establish

3. TLS Handshake (TLS 1.3):
   - Client Hello (cipher suites, SNI for google.com)
   - Server Certificate + Key Exchange
   - Session keys derived via ECDHE
   - 0-RTT or 1-RTT depending on session resumption
   - ~1 RTT for TLS 1.3 (was 2 RTT for TLS 1.2)

4. HTTP/2 or HTTP/3 Request:
   - GET / HTTP/2 with headers
   - Server responds with 301 or 200
   - HPACK header compression reduces overhead
   - H/3 over QUIC = UDP-based, no head-of-line blocking

5. Rendering: HTML parsed, CSS/JS fetched (often parallel), DOM built.

Interview tip: depth on DNS and TLS shows senior understanding.
```

**Q2. Explain the TCP three-way handshake. What is TIME_WAIT and why does it matter?**

Model Answer:
```
3-way handshake:
- Client → Server: SYN (seq=x)
- Server → Client: SYN-ACK (seq=y, ack=x+1)  
- Client → Server: ACK (ack=y+1)
Connection established after ACK sent.

TIME_WAIT: after connection close (4-way FIN exchange), the initiator 
enters TIME_WAIT for 2×MSL (Maximum Segment Lifetime, typically 60s).
Purpose: ensure all packets from this connection are gone before 
the port/IP pair is reused.

Production problem: high-throughput services can exhaust ephemeral ports 
(32768-60999 = ~28k ports) if TIME_WAIT accumulates. 
Each outbound connection to same {src_ip, src_port, dst_ip, dst_port} 
leaves a TIME_WAIT socket.

Fixes:
- SO_REUSEADDR: allow port reuse while in TIME_WAIT (apps must set this)
- net.ipv4.tcp_tw_reuse=1: kernel-level reuse for outbound connections
- Increase ephemeral port range: net.ipv4.ip_local_port_range = 1024 65535
- Connection pooling: reuse connections rather than closing

This is a real problem with microservices making many short-lived connections.
```

**Q3. How does HTTPS work? Explain the TLS handshake.**

Model Answer:
```
TLS 1.3 (current standard):

1. ClientHello: client sends supported cipher suites, TLS version, 
   random bytes, and key_share (public key for ECDHE key exchange)
   
2. ServerHello + Certificate: server picks cipher suite, sends its 
   certificate (signed by CA), its ECDHE public key, 
   and a signature proving it has the private key
   
3. Key derivation: both sides independently compute the same 
   session key using ECDHE (Elliptic Curve Diffie-Hellman Ephemeral)
   
4. Finished: server sends Finished message encrypted with session key.
   Client verifies, sends its own Finished.

Certificate chain validation:
- Server cert signed by Intermediate CA
- Intermediate CA signed by Root CA
- Client has Root CA in trust store
- Client verifies signature chain bottom-up

Perfect Forward Secrecy (PFS): ECDHE generates new ephemeral keys 
per session. Even if server's private key is stolen later, 
past sessions cannot be decrypted.

Production relevance: certificate expiry monitoring, SNI for multi-tenant,
HSTS (force HTTPS), certificate pinning for mobile apps.
```

**Q4. What is the difference between L4 and L7 load balancing?**

Model Answer:
```
L4 (Transport Layer):
- Routes based on IP + port only
- No visibility into HTTP headers, URLs, cookies
- Very fast, low overhead, handles TCP/UDP
- Example: AWS NLB, HAProxy TCP mode
- Use case: non-HTTP protocols (databases, MQTT, custom TCP)

L7 (Application Layer):  
- Reads HTTP headers, URLs, body content
- Can route based on path (/api → backend-a, / → backend-b)
- Can terminate TLS, modify requests/responses, add headers
- Can implement rate limiting, WAF, JWT validation
- Slightly more overhead than L4
- Example: AWS ALB, nginx, HAProxy HTTP mode, Envoy

Session affinity (sticky sessions):
- L7: cookie-based (more reliable, doesn't break with NAT)
- L4: source IP hash (breaks with proxies and CGNAT)

Health checks:
- L4: TCP connect success
- L7: HTTP 200 response to /health (much more meaningful)

In Kubernetes: Service = L4 (kube-proxy), Ingress = L7.
```

**Q5. How does DNS work? What is the difference between authoritative and recursive resolvers?**

Model Answer:
```
DNS hierarchy:
Root (.) → TLD (.com, .io, .in) → Second Level (github.com) → Subdomains

Recursive resolver (your DNS server, e.g., 8.8.8.8):
- Receives query from client
- Does the full lookup: asks root, then TLD, then authoritative
- Caches results by TTL
- Returns answer to client

Authoritative NS (e.g., ns1.github.com):
- Holds the actual zone records
- Returns definitive answers for its zone
- Does NOT recurse — only answers for its zone

Resolution flow:
1. App → OS resolver → /etc/resolv.conf → recursive resolver
2. Recursive → root NS (which NS for .com?)
3. Recursive → .com TLD NS (which NS for github.com?)
4. Recursive → github.com auth NS (A record for github.com?)
5. Recursive → client (caches result for TTL seconds)

TTL strategy: short TTL (60s) for services that change IPs (failover).
Long TTL (86400s) for stable records (reduces resolver load).

Negative caching: NXDOMAIN also cached (per negative TTL in SOA).
This is why DNS propagation 'delay' exists even after you fix a record.
```

*(Remaining 15 networking questions in `interview-prep/week2-networking.md`)*

---

# WEEK 3 — Git & Workflow (15 Questions)

**Q1. Explain git rebase vs git merge. When do you use each?**

Model Answer:
```
Merge: creates a merge commit. Preserves full history including branch point.
Non-destructive — existing commits unchanged.
Use when: integrating shared/public branches, wanting to preserve history.

Rebase: replays commits on top of another branch. Linear history.
Rewrites commits (new SHAs). 
Use when: local feature branches before PR, cleaning up commit history.

Golden rule: Never rebase public/shared branches.
If you rebase a branch others have pulled, their history diverges.
You get the dreaded "diverged histories" error.

Interactive rebase (git rebase -i HEAD~5):
- squash: combine commits into one (clean up WIP commits)
- fixup: like squash but discard commit message
- reword: change commit message
- drop: remove a commit entirely

In practice: on a feature branch, rebase onto main before PR 
to get a clean linear history. Use merge to integrate PRs into main.
```

**Q2. What is git bisect and when would you use it?**

Model Answer:
```
git bisect uses binary search to find which commit introduced a bug.

Usage:
git bisect start
git bisect bad                    # current commit is bad
git bisect good v1.2.0            # this version was good
# Git checks out middle commit
# You test: is this good or bad?
git bisect good                   # or: git bisect bad
# Repeat until Git identifies the exact commit
git bisect reset                  # restore HEAD

Automation: git bisect run ./test.sh
Git runs your test script on each candidate. test.sh returns 0=good, 1=bad.

Real scenario: "Something between v2.1 and v2.5 (200 commits) broke 
authentication. Binary search finds it in ~8 checks instead of 200."

This is a senior skill — most engineers don't know it exists.
```

*(Remaining 13 Git questions in `interview-prep/week3-git.md`)*

---

# WEEK 4 — Scripting & Automation (15 Questions)

**Q1. How do you write production-quality bash scripts?**

Model Answer:
```
Production bash has these non-negotiables:

#!/usr/bin/env bash
set -euo pipefail          # exit on error, unset var, pipe fail
IFS=$'\n\t'                # safe word splitting

trap 'cleanup' EXIT ERR    # always run cleanup
trap 'echo "Signal received"; exit 1' INT TERM

cleanup() {
    local exit_code=$?
    # Remove temp files, release locks, etc.
    rm -f "$TMPFILE"
    exit "$exit_code"
}

# Logging
log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" >&2; }
die() { log "ERROR: $*"; exit 1; }

# Input validation
[[ $# -lt 1 ]] && die "Usage: $0 <argument>"

# Atomic file writes (never partial writes)
tmpfile=$(mktemp)
echo "data" > "$tmpfile"
mv "$tmpfile" /final/path    # mv is atomic on same filesystem

# Test scripts with: shellcheck, bash -n (syntax), bash -x (debug)
```

*(Remaining 14 scripting questions in `interview-prep/week4-scripting.md`)*

---

## 🎭 Behavioral Bank — Phase 1

Use these 10 STAR stories across all interviews. Adapt the details.

1. **Time you found a critical security vulnerability** → your Linux audit lab work
2. **Time you improved system performance** → kernel tuning + benchmark results
3. **Time you had to explain a technical issue to a non-technical stakeholder** → impact-first framing
4. **Time you prevented an incident before it happened** → proactive monitoring
5. **Time you had to learn something quickly under pressure** → first principles approach
6. **Time you disagreed with a technical decision** → data-driven pushback
7. **Time you made a mistake in production** → blameless, systematic, fixed permanently
8. **Time you mentored someone** → teach by doing, not by telling
9. **Time you had to prioritise competing demands** → business impact ranking
10. **Time you automated a manual process** → time saved × frequency = ROI

---

*Next: `phase-02-core-devops/interview-prep/` — Docker, K8s, CI/CD questions*
