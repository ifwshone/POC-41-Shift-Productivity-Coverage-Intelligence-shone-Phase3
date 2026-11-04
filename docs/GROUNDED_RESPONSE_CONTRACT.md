# Grounded Response Contract
| Field | Purpose | Required |
|---|---|---|
| answer_id | Unique answer identifier (ANS-UUID) | Yes |
| status | answered, unsupported, unsafe, unavailable, error | Yes |
| intent | Approved intent string | Yes |
| answer | User-readable grounded LLM explanation | Yes |
| evidence_references | Traceable approved evidence arrays | Yes |
| key_values | Numbers exactly matching evidence | Yes |
| metadata | data_version, method_version, quality_status | Yes |
| limitation | Approved limitation string | Yes |
| suggested_follow_ups | 2-3 approved supported alternatives | Yes |