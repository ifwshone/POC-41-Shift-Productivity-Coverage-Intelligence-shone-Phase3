// /frontend/__tests__/intelligenceLoader.test.ts
import { loadIntelligenceSummary } from '../lib/intelligenceLoader';

// Mock fetch API globally
global.fetch = jest.fn();

describe('Intelligence Static Loader', () => {
  afterEach(() => {
    jest.resetAllMocks();
  });

  it('loads and validates the static JSON summary', async () => {
    const mockSummary = {
      approved_track: "Track A - Comparative",
      key_findings: ["Finding 1"]
    };
    
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockSummary
    });

    const summary = await loadIntelligenceSummary();
    expect(summary.approved_track).toEqual("Track A - Comparative");
    expect(global.fetch).toHaveBeenCalledWith("/data/intelligence/intelligence_summary.json", { cache: "no-store" });
  });

  it('throws an error on failed network request', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 404
    });

    await expect(loadIntelligenceSummary()).rejects.toThrow("Unable to load intelligence summary: 404");
  });
});