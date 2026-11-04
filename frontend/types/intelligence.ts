// /frontend/types/intelligence.ts
export interface IntelligenceEvidence {
    factor: string;
    value: string | number | boolean | null;
    contribution?: number | null;
    source_record_id?: string | null;
  }
  
  export interface IntelligenceResult {
    result_id: string;
    result_type: string;
    record_id: string | null;
    entity_id: string | null;
    group_key: string | null;
    period_start: string | null;
    period_end: string | null;
    metric_name: string;
    result_value: number | null;
    result_unit: string | null;
    result_category: string | null;
    priority_rank: number | null;
    finding: string;
    evidence: IntelligenceEvidence[];
    method_version: string;
    data_version: string;
    generated_at: string;
    quality_status: "validated" | "conditional" | "rejected";
    limitation: string;
  }
  
  export interface IntelligenceSummary {
    project_id: string;
    project_title: string;
    approved_track: string;
    primary_analytical_question: string;
    decision_to_be_supported: string;
    data_version: string;
    method_version: string;
    result_count: number;
    key_findings: string[];
    priority_items: string[];
    validation_result: string;
    important_limitations: string[];
    generated_at: string;
  }