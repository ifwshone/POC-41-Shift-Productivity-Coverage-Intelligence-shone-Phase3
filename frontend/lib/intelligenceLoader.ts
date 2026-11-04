// /frontend/lib/intelligenceLoader.ts
import { IntelligenceResult, IntelligenceSummary } from "../types/intelligence";
import { validateIntelligenceResult, validateIntelligenceSummary } from "./intelligenceValidator";

export async function loadIntelligenceResults(): Promise<IntelligenceResult[]> {
  const response = await fetch("/data/intelligence/intelligence_results.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`Unable to load intelligence results: ${response.status}`);
  const values: unknown = await response.json();
  if (!Array.isArray(values)) throw new Error("Intelligence results must be an array");
  values.forEach(validateIntelligenceResult);
  return values.filter(v => v.quality_status !== "rejected");
}

export async function loadIntelligenceSummary(): Promise<IntelligenceSummary> {
  const response = await fetch("/data/intelligence/intelligence_summary.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`Unable to load intelligence summary: ${response.status}`);
  const value: unknown = await response.json();
  validateIntelligenceSummary(value);
  return value;
}