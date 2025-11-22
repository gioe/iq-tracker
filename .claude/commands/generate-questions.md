---
description: Trigger question generation on Railway (production)
---

Trigger the question generation service on Railway.

Use the following endpoint:
- URL: https://question-service-production-9946.up.railway.app/trigger
- Admin Token: unXs8f54HzMA21B37PQ9AmqQ5c94n_4HlBfbRN1ax4Q

Ask the user:
1. How many questions to generate? (default: 50)
2. Should this be a dry run? (default: no)

Then execute a curl command to trigger the job:

```bash
curl -X POST https://question-service-production-9946.up.railway.app/trigger \
  -H "X-Admin-Token: unXs8f54HzMA21B37PQ9AmqQ5c94n_4HlBfbRN1ax4Q" \
  -H "Content-Type: application/json" \
  -d '{"count": <count>, "dry_run": <dry_run>}'
```

After triggering, inform the user:
- Show the response from the service
- Remind them they can check logs at: https://railway.app (question-service-production)
- Mention that the job runs in the background
