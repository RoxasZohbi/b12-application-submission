#!/usr/bin/env python3
"""
B12 Application Submission Script

Constructs a canonical JSON payload, signs it with HMAC-SHA256,
and submits it to the B12 application endpoint via POST request.
"""

import os
import sys
import json
import hmac
import hashlib
from datetime import datetime, timezone
import requests


def get_env_variable(name):
    """Get environment variable or exit with error."""
    value = os.environ.get(name)
    if not value:
        print(f"Error: {name} environment variable is not set", file=sys.stderr)
        sys.exit(1)
    return value.strip() 


def generate_timestamp():
    """Generate ISO 8601 timestamp in UTC."""
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def create_payload(timestamp, name, email, resume_link, repository_link, action_run_link):
    """Create the canonical JSON payload with sorted keys."""
    payload = {
        "timestamp": timestamp,
        "name": name,
        "email": email,
        "resume_link": resume_link,
        "repository_link": repository_link,
        "action_run_link": action_run_link
    }
    # Canonicalize: UTF-8, compact separators, sorted keys
    return json.dumps(payload, ensure_ascii=False, separators=(',', ':'), sort_keys=True)


def compute_signature(payload, secret):
    """Compute HMAC-SHA256 signature of the payload."""
    payload_bytes = payload.encode('utf-8')
    secret_bytes = secret.encode('utf-8')
    signature = hmac.new(secret_bytes, payload_bytes, hashlib.sha256)
    return signature.hexdigest()


def submit_application(payload, signature):
    """Submit the signed payload to B12 application endpoint."""
    url = "https://b12.io/apply/submission"
    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={signature}"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error submitting application: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main execution function."""
    print("=== B12 Application Submission ===\n")
    
    # Get configuration from environment variables
    secret = get_env_variable("B12_SECRET")
    print(f"Secret length: {len(secret)} characters")
    print(f"Secret starts with: {secret[:4]}...")
    
    name = get_env_variable("B12_NAME")
    email = get_env_variable("B12_EMAIL")
    resume_link = get_env_variable("B12_RESUME_LINK")
    repository_link = get_env_variable("B12_REPOSITORY_LINK")
    action_run_link = get_env_variable("B12_ACTION_RUN_LINK")
    
    # Generate timestamp
    timestamp = generate_timestamp()
    print(f"Timestamp: {timestamp}")
    
    # Create canonical payload
    payload = create_payload(timestamp, name, email, resume_link, repository_link, action_run_link)
    print(f"\nCanonical Payload:\n{payload}\n")
    
    # Compute HMAC-SHA256 signature
    signature = compute_signature(payload, secret)
    print(f"HMAC-SHA256 Signature: {signature}\n")
    
    # Submit application
    print("Submitting application to B12...")
    response = submit_application(payload, signature)
    
    # Print response
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nSubmission Receipt:\n{response.text}")
    
    print("\n=== Submission Complete ===")


if __name__ == "__main__":
    main()
