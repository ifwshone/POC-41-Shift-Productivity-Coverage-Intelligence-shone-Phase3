// /frontend/__tests__/intelligenceValidator.test.ts
import { validateIntelligenceResult, validateIntelligenceSummary, validateIntelligenceCollection, checkDataFreshness } from '../lib/intelligenceValidator';

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
    evidence: [{ factor: "record_count", value: 5 }],
    result_value: -10.5,
    priority_rank: 1
  };

  it('passes a valid intelligence result', () => {
    expect(() => validateIntelligenceResult(validResult)).not.toThrow();
  });

  it('rejects missing mandatory fields', () => {
    const invalidResult = { ...validResult, finding: undefined };
    expect(() => validateIntelligenceResult(invalidResult)).toThrow("Invalid required field: finding");
  });

  it('rejects missing numeric fields', () => {
    const invalidResult = { ...validResult, result_value: undefined };
    expect(() => validateIntelligenceResult(invalidResult)).toThrow("Invalid required field: result_value must be a number");
  });

  it('rejects unsupported quality_status', () => {
    const invalidResult = { ...validResult, quality_status: "draft" };
    expect(() => validateIntelligenceResult(invalidResult)).toThrow("Unsupported quality_status");
  });

  it('detects version mismatch', () => {
    const summary = { data_version: "1.0.0", method_version: "1.0.0", generated_at: "2026-11-04T10:00:00Z" } as any;
    const staleResult = { ...validResult, data_version: "0.9.0" } as any;
    
    const freshness = checkDataFreshness(summary, [staleResult]);
    expect(freshness.isVersionMismatch).toBe(true);
  });
  
  it('validates collection size and duplicates', () => {
    const summary = { result_count: 2 } as any;
    const results = [validResult, { ...validResult, result_id: "RES-COMP-002" }] as any;
    
    // Should pass
    expect(() => validateIntelligenceCollection(results, summary)).not.toThrow();
    
    // Should fail on duplicate ID
    const dupResults = [validResult, validResult] as any;
    expect(() => validateIntelligenceCollection(dupResults, summary)).toThrow("Duplicate result_id detected: RES-COMP-001");
  });
});