// /frontend/__tests__/intelligenceValidator.test.ts
import { validateIntelligenceResult, validateIntelligenceSummary, isStale } from '../lib/intelligenceValidator';

describe('Intelligence Contract Validator', () => {
  const validResult = {
    result_id: "RES-COMP-001",
    result_type: "ranking",
    metric_name: "output_gap_vs_baseline",
    finding: "Valid finding",
    method_version: "1.0.0",
    data_version: "1.0.0",
    generated_at: "2026-11-04T10:00:00Z",
    quality_status: "validated",
    limitation: "Synthetic data only",
    evidence: [{ factor: "record_count", value: 5 }]
  };

  it('passes a valid intelligence result', () => {
    expect(() => validateIntelligenceResult(validResult)).not.toThrow();
  });

  it('rejects missing mandatory fields', () => {
    const invalidResult = { ...validResult, finding: undefined };
    expect(() => validateIntelligenceResult(invalidResult)).toThrow("Invalid required field: finding");
  });

  it('rejects unsupported quality_status', () => {
    const invalidResult = { ...validResult, quality_status: "draft" };
    expect(() => validateIntelligenceResult(invalidResult)).toThrow("Unsupported quality_status");
  });

  it('detects stale versions between summary and results', () => {
    const summary = { data_version: "1.0.0", method_version: "1.0.0" } as any;
    const staleResult = { ...validResult, data_version: "0.9.0" } as any;
    expect(isStale(summary, [staleResult])).toBe(true);
  });
});