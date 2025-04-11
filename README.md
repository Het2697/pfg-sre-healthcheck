# PFG SRE Healthcheck Script

## Description
This Python script collects endpoint health info every minute for 1 hour. It logs internal IP, external IP, endpoint DNS IP, HTTP status, response latency, and certificate expiration.

## How to Run

```bash
python3 healthcheck.py
```

## Output
Results saved in `health_data.csv`. Columns:
- Timestamp
- Endpoint URL
- Internal IP
- External IP
- Endpoint IP
- Latency (ms)
- HTTP Status
- SSL Expiration Date

## Ansible Deployment (Optional)
```bash
ansible-playbook -i inventory deploy_healthcheck.yml
```
