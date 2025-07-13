
# Devolv GitHub Action

✅ Run **Devolv DevOps Toolkit** tools directly in GitHub workflows to secure, validate, and fix your [IAM](https://aws.amazon.com/iam/?trk=858d3377-dc99-4b71-b7d9-dfbd53b3fb6c&sc_channel=ps&ef_id=Cj0KCQjwss3DBhC3ARIsALdgYxM3CrKbApAwBEnURXGAMfU784VxuM2UW0KdgDrMMBbjhdDy7fIjiRUaAro9EALw_wcB:G:s&s_kwcid=AL!4422!3!651612429263!p!!g!!iam!19836375022!146902912293&gad_campaignid=19836375022&gbraid=0AAAAADjHtp_rqCPIKwRXZ8uS4oWzACCtv&gclid=Cj0KCQjwss3DBhC3ARIsALdgYxM3CrKbApAwBEnURXGAMfU784VxuM2UW0KdgDrMMBbjhdDy7fIjiRUaAro9EALw_wcB) policies — automatically.

---

## 🌟 What This Action Can Do

👉 **Devolv Drift**
- Detect IAM drift between your local files and deployed AWS policies
- Auto-create GitHub PRs to fix detected drift
- Open GitHub issues to track misalignments
- Keep your AWS environment in sync with your source of truth

👉 **Devolv Validate**
- Validate IAM JSON/YAML files for security issues (e.g., wildcards, risky permissions)
- Catch policy misconfigurations before they go live
- Block PRs with unsafe changes

---

## 🚀 Example Use Cases

✅ **Keep IAM policies aligned:** Stop worrying about manual AWS changes breaking your security posture — Devolv Drift finds and fixes them via PRs.

✅ **Prevent bad policies from merging:** Devolv Validate ensures only safe IAM policies land in main.

✅ **Automate governance:** Replace manual policy reviews with automatic CI/CD checks.

✅ **No more surprise misconfigurations:** Everything is caught at PR time — before deployment.

✅ **Zero-touch fixes:** Devolv creates issues and PRs so your team can focus on code, not IAM drift.

---

## 📌 Inputs

| Input          | Description                             | Required |
|----------------|-----------------------------------------|----------|
| `tool`         | Which tool to run (`drift` or `validate`)| ✅ yes |
| `policy-name`  | IAM policy name (required for drift)     | ❌ no (✅ yes if `drift`) |
| `path`         | Path to local policy file or folder      | ✅ yes |

---

## ⚡ Example usage

### 🛡️ Drift detection

```yaml
- name: Run Devolv Drift Detection
  uses: devolvdev/devolv-actions@v2
  with:
    tool: drift
    policy-name: DevolvTestPolicyHuge
    path: ./test-devolv-policy.json
    approvers: ""  # Empty by default; pass comma-separated list if needed
    github-token: ${{ secrets.GITHUB_TOKEN }}
    approval-anyway: false
```

### 🔍 IAM validation

```yaml
- name: Run Devolv IAM Validation
  uses: devolvdev/devolv-actions@v2
  with:
    tool: validate
    path: ./sample_policies
```

---

## 🔗 Further resources

➡ [Devolv Drift Onboarding + CI/CD Guide](https://extraordinary-cobbler-1d9612.netlify.app/)  
➡ [Devolv Validate Docs](https://devolvdev.github.io/devolv/validator.html)  
➡ [Devolv Project on GitHub](https://github.com/devolvdev)

---

Built with ❤️ to make IAM security effortless.
