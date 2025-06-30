
# Devolv GitHub Action  

✅ Run **Devolv DevOps Toolkit** tools (drift detection, IAM validation) directly in GitHub workflows.  

## 📌 Inputs  

| Input          | Description                             | Required |
|----------------|-----------------------------------------|----------|
| `tool`         | Which tool to run (`drift` or `validate`)| ✅ yes |
| `policy-name`  | IAM policy name (required for drift)     | ❌ no (✅ yes if `drift`) |
| `path`         | Path to local policy file or folder      | ✅ yes |

## 🚀 Example usage  

### 🛡️ Drift detection  

```yaml
- name: Run Devolv Drift Detection  
  uses: devolvdev/devolv-actions@v1  
  with:  
    tool: drift  
    policy-name: DevolvTestPolicyHuge  
    path: ./test-devolv-policy.json  
```  

### 🔍 IAM validation  

```yaml
- name: Run Devolv IAM Validation  
  uses: devolvdev/devolv-actions@v1  
  with:  
    tool: validate  
    path: ./sample_policies  
```  

## ⚡ Notes  

- ✅ **Supports both drift detection and validator** (use `tool: drift` or `tool: validate`)  
- ✅ Output is colorized and console-friendly (when run locally)  
- ✅ Works great in CI/CD pipelines  
- The action installs Devolv at runtime with pip (silent install)  
