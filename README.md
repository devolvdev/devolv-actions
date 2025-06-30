
# Devolv GitHub Action

✅ Run Devolv DevOps Toolkit tools (drift detection, IAM validation) easily inside GitHub workflows.

## 📌 Inputs

| Input        | Description                           | Required |
|--------------|---------------------------------------|----------|
| `tool`       | Which tool to run (drift, validate)   | ✅ yes |
| `policy-name`| IAM policy name (needed for drift)    | ❌ no |
| `file`       | Path to local policy file             | ✅ yes |

## 🚀 Example usage

```yaml
- uses: devolvdev/devolv-action@v1
  with:
    tool: drift
    policy-name: my-policy
    file: ./policy.json

- uses: devolvdev/devolv-action@v1
  with:
    tool: validate
    file: ./policy.json
```

## 🔑 Notes

- The action installs Devolv at runtime using pip.
- Supports both `validate` and `drift` tools.
