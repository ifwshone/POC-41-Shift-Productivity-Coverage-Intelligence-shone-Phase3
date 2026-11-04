// /frontend/__tests__/DataIntelligencePage.test.tsx
import '@testing-library/jest-dom';
import { render, screen, waitFor } from '@testing-library/react';
import DataIntelligencePage from '../app/intelligence/page';
import * as loader from '../lib/intelligenceLoader';

// Mock the static loader
jest.mock('../lib/intelligenceLoader', () => ({
  loadIntelligenceResults: jest.fn(),
  loadIntelligenceSummary: jest.fn()
}));

describe('Data Intelligence Page UI', () => {
  it('renders loading state initially', () => {
    render(<DataIntelligencePage />);
    expect(screen.getByText(/Validating Contract & Loading Intelligence/i)).toBeInTheDocument();
  });

  it('renders intelligence components upon successful load', async () => {
    (loader.loadIntelligenceSummary as jest.Mock).mockResolvedValue({
      decision_to_be_supported: "Supervisor coverage review",
      approved_track: "Track A",
      method_version: "1.0.0",
      data_version: "1.0.0",
      generated_at: "2026-11-04T10:00:00Z",
      key_findings: ["Node A needs review"],
      priority_items: ["facility_a_night_watch"],
      important_limitations: ["Synthetic only"],
      validation_result: "PASS"
    });

    (loader.loadIntelligenceResults as jest.Mock).mockResolvedValue([{
      result_id: "1",
      entity_id: "facility_a_night_watch",
      priority_rank: 1,
      result_value: -25.8,
      result_category: "low",
      finding: "facility_a_night_watch ranks 1",
      evidence: [{ factor: "record_count", value: 5 }]
    }]);

    render(<DataIntelligencePage />);

    await waitFor(() => {
      expect(screen.getByText("Data Intelligence")).toBeInTheDocument();
      expect(screen.getByText("Node A needs review")).toBeInTheDocument();
      expect(screen.getByText("facility_a_night_watch")).toBeInTheDocument();
      expect(screen.getByText("Synthetic only")).toBeInTheDocument();
    });
  });
});