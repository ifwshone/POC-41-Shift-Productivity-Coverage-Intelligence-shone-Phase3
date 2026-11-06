// /frontend/lib/intelligenceLoader.ts
import { IntelligenceResult, IntelligenceSummary } from "../types/intelligence";
import { validateIntelligenceResult, validateIntelligenceSummary } from "./intelligenceValidator";

export async function loadIntelligenceResults(): Promise<IntelligenceResult[]> {
  try {
    // 1. Direct Bundle Strategy: Bypasses Next.js SSR relative fetch 404 bugs in Docker
    const values = require("../public/data/intelligence/intelligence_results.json");
    
    if (!Array.isArray(values)) throw new Error("Intelligence results must be an array");
    values.forEach(validateIntelligenceResult);
    return values.filter((v: any) => v.quality_status !== "rejected");
    
  } catch (error) {
    console.error("Local require failed, attempting browser fallback fetch...", error);
    
    // 2. Client-side fallback
    const response = await fetch("/data/intelligence/intelligence_results.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`Unable to load intelligence results: ${response.status}`);
    const values: unknown = await response.json();
    
    if (!Array.isArray(values)) throw new Error("Intelligence results must be an array");
    values.forEach(validateIntelligenceResult);
    return values.filter((v: any) => v.quality_status !== "rejected");
  }
}

export async function loadIntelligenceSummary(): Promise<IntelligenceSummary> {
  try {
    // 1. Direct Bundle Strategy
    const value = require("../public/data/intelligence/intelligence_summary.json");
    
    validateIntelligenceSummary(value);
    return value as IntelligenceSummary;
    
  } catch (error) {
    console.error("Local require failed, attempting browser fallback fetch...", error);
    
    // 2. Client-side fallback
    const response = await fetch("/data/intelligence/intelligence_summary.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`Unable to load intelligence summary: ${response.status}`);
    const value: unknown = await response.json();
    
    validateIntelligenceSummary(value);
    return value as IntelligenceSummary;
  }
}