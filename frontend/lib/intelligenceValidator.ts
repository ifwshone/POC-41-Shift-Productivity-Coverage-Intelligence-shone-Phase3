import { IntelligenceResult, IntelligenceSummary } from "../types/intelligence";

const QUALITY_STATUSES = new Set(["validated", "conditional", "rejected"]);

export function validateIntelligenceResult(value: unknown): asserts value is IntelligenceResult {
  if (!value || typeof value !== "object") throw new Error("Intelligence result must be an object");
  
  const item = value as Record<string, unknown>;
  const requiredStrings = ["result_id", "result_type", "metric_name", "finding", "method_version", "data_version", "generated_at", "quality_status", "limitation"];
  
  for (const field of requiredStrings) {
    if (typeof item[field] !== "string" || !item[field]) {
      throw new Error(`Invalid required field: ${field}`);
    }
  }

  if (typeof item.result_value !== "number") throw new Error("Invalid required field: result_value must be a number");
  if (typeof item.priority_rank !== "number") throw new Error("Invalid required field: priority_rank must be a number");
  
  if (!QUALITY_STATUSES.has(String(item.quality_status))) throw new Error("Unsupported quality_status");
  if (!Array.isArray(item.evidence)) throw new Error("evidence must be an array");
  if (Number.isNaN(Date.parse(String(item.generated_at)))) throw new Error("generated_at is invalid");
}

export function validateIntelligenceSummary(value: unknown): asserts value is IntelligenceSummary {
  if (!value || typeof value !== "object") throw new Error("Intelligence summary must be an object");
  const item = value as Record<string, unknown>;
  if (typeof item.approved_track !== "string" || !item.approved_track) throw new Error("Invalid summary: missing approved_track");
  if (!Array.isArray(item.key_findings)) throw new Error("Invalid summary: key_findings must be an array");
  if (typeof item.result_count !== "number") throw new Error("Invalid summary: missing result_count");
}

export function validateIntelligenceCollection(results: IntelligenceResult[], summary: IntelligenceSummary) {
  if (results.length !== summary.result_count) {
    throw new Error(`Result count mismatch: expected ${summary.result_count}, got ${results.length}`);
  }
  const ids = new Set();
  for (const r of results) {
    if (ids.has(r.result_id)) throw new Error(`Duplicate result_id detected: ${r.result_id}`);
    ids.add(r.result_id);
  }
}

export function checkDataFreshness(summary: IntelligenceSummary, results: IntelligenceResult[]) {
  const isVersionMismatch = results.some(r => r.data_version !== summary.data_version || r.method_version !== summary.method_version);
  
  const summaryDate = new Date(summary.generated_at).getTime();
  const now = Date.now();
  // Flag as stale if older than 7 days
  const isStaleTime = (now - summaryDate) > 7 * 24 * 60 * 60 * 1000; 
  
  return { isVersionMismatch, isStaleTime };
}