# B12 Application Submission

This repository contains a small Python script and GitHub Actions workflow used to submit my application to B12, as specified in the application instructions.

The submission is executed via continuous integration and performs a signed POST request to the B12 application endpoint.

## What this demonstrates

- Canonical JSON payload construction (sorted keys, compact encoding)
- HMAC-SHA256 request signing
- Secure header-based authentication
- CI-driven execution with observable logs
- Minimal, deterministic implementation

## How it works

A GitHub Actions workflow triggers the Python script, which:

1. Constructs the required JSON payload with an ISO 8601 timestamp
2. Canonicalizes the payload (UTF-8, compact separators, sorted keys)
3. Computes an HMAC-SHA256 signature of the request body
4. Sends the signed POST request to the B12 submission endpoint
5. Prints the submission receipt returned by the API

The workflow run itself serves as the verifiable execution record for the submission.

## Repository scope

This repository exists solely for the purpose of the B12 application exercise and is intentionally minimal.

AI assistance was used in accordance with the application guidelines.
