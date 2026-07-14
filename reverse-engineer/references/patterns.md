# Detection Pattern Library

Concrete search patterns for the code-level review. These are **starting points, not verdicts** — every hit must be confirmed by tracing whether attacker-controllable data actually reaches it (a `subprocess(shell=True)` on a hardcoded string is fine; on a value from an API response, it's a finding). Use ripgrep (`rg -n`); adapt to the project's languages.

## Table of contents
1. Command / shell injection
2. Arbitrary code execution & unsafe deserialization
3. SQL / query injection
4. Secrets & credentials in code
5. Weak crypto, randomness & TLS
6. Path traversal & unsafe file/archive handling
7. Server-side request forgery (SSRF) & outbound requests
8. Web / browser-extension specific
9. Error handling & stability
10. Config, logging & misc

---

## 1. Command / shell injection
```
rg -n "shell=True|os\.system|os\.popen|subprocess\.(call|run|Popen|check_output)" 
rg -n "\bsystem\(|\bexec[lv]p?\(|`.*`" 
```
Confirm: is any argument built from untrusted input (API data, file contents, args, env)? Prefer list-form `subprocess.run([...])` without `shell=True`. Windows `.bat`/PowerShell launchers count — check interpolated params.

## 2. Arbitrary code execution & unsafe deserialization
```
rg -n "\beval\(|\bexec\(|__import__\(|compile\("
rg -n "pickle\.loads?|cPickle|marshal\.loads|jsonpickle|dill\.loads"
rg -n "yaml\.load\((?!.*Loader=yaml\.SafeLoader)"
rg -n "\.load\(|\.loads\(" --glob "*.py"
```
`pickle`/`marshal`/`yaml.load` on any data that could be attacker-influenced = remote code execution. Fix: `yaml.safe_load`, avoid pickle for untrusted data (use JSON), never `eval`/`exec` on external strings.

## 3. SQL / query injection
```
rg -n "execute\(.*(%|\+| f\"| f')|executemany\(.*(%|\+)"
rg -n "f\"(SELECT|INSERT|UPDATE|DELETE|DROP)|\"\s*\+\s*"
```
Fix: parameterized queries / bound parameters, never string-built SQL.

## 4. Secrets & credentials in code
```
rg -ni "(api[_-]?key|secret|token|passwd|password|private[_-]?key|client[_-]?secret)\s*[:=]"
rg -n "AKIA[0-9A-Z]{16}|xox[baprs]-[0-9A-Za-z-]+|ghp_[0-9A-Za-z]{36}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
rg -n "eyJ[A-Za-z0-9_-]{10,}\."   # JWTs
```
Also: is `.env` / credentials file committed? `git log --all --full-history -- .env` and check `.gitignore`. **Never print the secret value into the report** — reference `file:line` and redact. Any real key found = rotate it.

## 5. Weak crypto, randomness & TLS
```
rg -n "verify=False|ssl\._create_unverified_context|check_hostname\s*=\s*False|CERT_NONE"
rg -n "hashlib\.(md5|sha1)|\bDES\b|\bECB\b|Random\(\)"
rg -n "random\.(random|randint|choice|shuffle|getrandbits)"   # if used for tokens/keys
```
`random` is not cryptographically secure — use `secrets` for tokens. MD5/SHA1 unfit for security. `verify=False` disables TLS validation (MITM). 

## 6. Path traversal & unsafe file/archive handling
```
rg -n "open\(|os\.path\.join\(|send_file|send_from_directory|shutil\.(copy|move)"
rg -n "\.extractall\(|zipfile|tarfile"
```
Confirm no user-influenced path escapes an intended dir (`..`, absolute paths). `extractall` on untrusted archives = zip-slip. Fix: validate/normalize paths, restrict to a base dir.

## 7. SSRF & outbound requests
```
rg -n "requests\.(get|post|put|delete)\(|urlopen\(|httpx\.|aiohttp|urllib"
```
Confirm the target host/URL isn't derived from untrusted input (which could point at internal services/metadata endpoints). Add timeouts on every network call (also a stability fix).

## 8. Web / browser-extension specific
```
rg -n "innerHTML|outerHTML|document\.write|dangerouslySetInnerHTML|insertAdjacentHTML"
rg -n "\beval\(|new Function\(|setTimeout\(\s*[\"']|setInterval\(\s*[\"']"
rg -n "onMessageExternal|postMessage|addEventListener\(\s*[\"']message"
rg -n "debug\s*=\s*True|DEBUG\s*=\s*True|app\.run\(.*debug=True"
```
For browser extensions / message bridges: **validate `sender`/`origin`** on every incoming message (an unvalidated `onMessage`/`postMessage` handler lets any page drive it); review `manifest` permissions and host permissions for over-broad grants; avoid `innerHTML` with dynamic data (XSS). For web frameworks: no `debug=True` in production.

## 9. Error handling & stability
```
rg -n "except\s*:|except (BaseException|Exception)\s*:\s*(pass|\.\.\.)"
rg -n "requests\.(get|post)\((?!.*timeout)"   # network calls missing timeout
```
Bare/blanket excepts that `pass` hide failures (including security-relevant ones) and cause silent instability. Network calls without timeouts hang. Also look for `/ 0` risks, unchecked `None`/empty data, unbounded loops/queues, unclosed resources (prefer `with`).

## 10. Config, logging & misc
```
rg -ni "print\(.*(key|secret|token|password)|log(ger)?\.\w+\(.*(key|secret|token|password)"
rg -n "0\.0\.0\.0|allow_origins=\[?\s*[\"']\*|CORS\(.*\*"
rg -n "tempfile\.mktemp|chmod\(.*0o?777|umask"
```
Secrets in logs leak them. `0.0.0.0` binds to all interfaces (exposure). Wildcard CORS. World-writable files/temp races. Overly broad file permissions.
